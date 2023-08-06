import datetime as dt
import json
from urllib import parse
import uuid
import requests
import yaml
from delta.tables import DeltaTable
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import SQLContext
import pyspark.sql.functions as F
import pyspark.sql.types as T
from kbcstorage.files import Files
from kbcstorage.tables import Tables
from odapdbxbundle.common.databricks import resolve_dbutils
from odapdbxbundle.common.logger import logger

SECONDS_IN_HOUR = 3600


class NonexistingTable(Exception):
    pass


class MissingSchema(Exception):
    pass


class KeboolaExporter:
    def __init__(self, *args):
        self._spark = SparkSession.getActiveSession()
        if len(args) == 1:
            with open(args[0], "r", encoding="utf8") as yamlfile:
                config = yaml.load(yamlfile, Loader=yaml.FullLoader)
            self._kbc_url = config["kbc_url"]
            self._scope = config["scope"]
            self._logging_table_path = config["logging_table_path"]
        else:
            self._kbc_url = args[0]
            self._scope = args[1]
            self._logging_table_path = args[2]
        self._kbc_api = self._kbc_url + "/v2/storage/tables?include=columns,columnMetadata"
        self._dbutils = resolve_dbutils()

    @staticmethod
    def __extract_workspace_connection_detail(workspace: dict):
        container = workspace["connection"]["container"]
        raw_url, raw_sas = workspace["connection"]["connectionString"].split(";")
        url = raw_url.replace("BlobEndpoint=https://", "")
        sas = raw_sas.replace("SharedAccessSignature=", "")

        return container, url, sas

    @staticmethod
    def __add_schema_column(schema: T.StructType, name: str, column_type: str, doubles: list):
        """
        Add new column definition to StructType based on string name of the type.
        Storing doubles and booleans columns for conversion from string.
        """

        type_mapping = {
            "CHAR": T.StringType(),
            "INT": T.LongType(),
            "TIME": T.TimestampType(),
            "DATE": T.DateType(),
            "FLOAT": T.StringType(),
            "DOUBLE": T.StringType(),
            "NUMERIC": T.StringType(),
            "DECIMAL": T.StringType(),
            "BIT": T.ShortType(),
        }

        spark_type = T.StringType()
        for k, v in type_mapping.items():
            if k in column_type:
                spark_type = v
                break

        schema.add(name, spark_type, True)
        if column_type in ["FLOAT", "DOUBLE", "NUMERIC", "DECIMAL"]:
            doubles.append(name)
        return schema

    def __get_keboola_schema(self, table_id: str, kbc_token: str):
        response = requests.get(self._kbc_api, headers={"X-StorageApi-Token": kbc_token}, timeout=30)
        parsed = json.loads(response.content)
        for table in parsed:
            tbl_id = table["id"]
            if tbl_id == table_id:
                return table
        raise NonexistingTable(f"Table {table_id} does not exist.")

    def get_schema(self, table_id: str, kbc_token: str, scope: str):
        doubles = []
        kbc_token_src = self._dbutils.secrets.get(scope, kbc_token)
        table = self.__get_keboola_schema(table_id, kbc_token_src)
        schema = T.StructType()
        columns_metadata = (
            table["columnMetadata"] if "columnMetadata" in table and table["columnMetadata"]
            else table["sourceTable"]["columnMetadata"]
        )

        if not columns_metadata:
            raise MissingSchema(f"Table {table_id} does not have schema.")

        for column in columns_metadata.keys():
            for column_type in columns_metadata[column]:
                if column_type["key"] == "KBC.datatype.type" and column not in schema.names:
                    self.__add_schema_column(schema, column, column_type["value"], doubles)
        table_schema = {
            "schema": schema,
            "lastChange": table["lastChangeDate"],
            "primaryKey": table["primaryKey"],
        }
        return table_schema, doubles

    def __get_changed_since(self, table_path: str):
        if self._spark._jsparkSession.catalog().tableExists(table_path):  # pylint: disable=[protected-access]
            return self._spark.sql(f"SHOW TBLPROPERTIES {table_path}('lastChange')").collect()[0]["value"]
        return None

    def __get_path_to_exported_table(self, files_src: Files, file_id: str):
        manifest_detail = files_src.detail(file_id, federation_token=True)

        _, account_core, path, _, sas_token, _ = parse.urlparse(manifest_detail["url"])
        _, container, manifest = path.split("/")
        filename = manifest.replace("manifest", "")

        # Set the SAS token, so that we can access the exported table
        self._spark.conf.set(f"fs.azure.sas.{container}.{account_core}", sas_token)

        file_path = f"wasbs://{container}@{account_core}/{filename}"
        return file_path

    def __get_table_as_df(self, file_path: str, schema: T.StructType, doubles: list):
        chunks = [f.path for f in self._dbutils.fs.ls(file_path) if f.size != 0]
        df = (
            self._spark.read.schema(schema)
            .option("quote", '"')
            .option("escape", '"')
            .option("multiLine", True)
            .format("csv")
            .load(path=chunks)
        )

        return df.select(
            *(F.col(c).cast("double").alias(c) for c in doubles), *(x for x in df.columns if x not in doubles)
        )

    def __store_table_to_database(self, df: DataFrame, table_schema: dict, table_path: str, partition_by: str):
        catalog_name, database_name, _ = table_path.split(".")
        self._spark.sql(f"CREATE DATABASE IF NOT EXISTS {catalog_name}.{database_name}")

        # if table already exists and there are primary keys then upsert otherwise append
        if len(table_schema["primaryKey"]) == 0 or not self._spark._jsparkSession.catalog().tableExists(
                table_path):  # pylint: disable=[protected-access]
            self.__append(df, table_path, partition_by)
        else:
            self.__upsert(df, table_path, table_schema)

        # save information about last change to table properties
        last_change = table_schema["lastChange"]
        sql_context = SQLContext(self._spark.sparkContext)
        sql_context.sql(f"ALTER TABLE {table_path} SET TBLPROPERTIES('lastChange' = '{last_change}')")

    @staticmethod
    def __append(df: DataFrame, table_path: str, partition_by: str):
        df_writer = df.write.format("delta").mode("append").option("overwriteSchema", True)

        if partition_by:
            df_writer = df_writer.partitionBy(partition_by)

        df_writer.saveAsTable(table_path)

    def __upsert(self, df: DataFrame, table_path: str, table_schema: dict):
        primary_key = table_schema["primaryKey"]
        merge_cond = " AND ".join(f"oldData.{pk} = newData.{pk}" for pk in primary_key)

        insert_set = {col: f"newData.`{col}`" for col in df.columns}
        update_set = {col: f"newData.`{col}`" for col in df.columns if col not in table_schema["primaryKey"]}

        old_df = DeltaTable.forName(self._spark, table_path)

        missing_columns = list(set(df.columns) - set(old_df.toDF().columns))
        # Add the missing columns to the target dataframe, filling in with default values
        for col in missing_columns:
            self._spark.sql(f"ALTER TABLE {table_path} ADD COLUMNS ({col} string)")

        (
            old_df.alias("oldData")
            .merge(df.alias("newData"), merge_cond)
            .whenMatchedUpdate(set=update_set)
            .whenNotMatchedInsert(values=insert_set)
            .execute()
        )

    def export_table(self, table_id: str, table_path: str, token: str, scope=None, partition_by=""):
        retries = 3
        if scope is None:
            scope = self._scope
        while retries:
            try:
                kbc_token_src = self._dbutils.secrets.get(scope, token)
                files_src = Files(self._kbc_url, kbc_token_src)
                tables_src = Tables(self._kbc_url, kbc_token_src)
                table_schema, doubles = self.get_schema(table_id, token, scope)
                last_change = table_schema["lastChange"]

                file_id = tables_src.export(
                    table_id=table_id,
                    columns=None,
                    changed_since=self.__get_changed_since(table_path),
                    changed_until=last_change,
                    is_gzip=True,
                )

                file_path = self.__get_path_to_exported_table(files_src, file_id)
                df = self.__get_table_as_df(file_path, table_schema["schema"], doubles)
                logger.info(f"Exporting table: {table_id}, Last update: {last_change},  Rows: {df.count()}")

                if df.count() > 0:
                    self.__store_table_to_database(df, table_schema, table_path, partition_by)
                    if "DELETED_FLAG" in df.columns:
                        new_df = DeltaTable.forName(self._spark, table_path)
                        new_df.delete(F.col("DELETED_FLAG") == "Y")
                        new_df.vacuum()
                self.__write_export_log(table_id, table_path, df.count())
                return self._spark.read.table(table_path)
            except requests.ConnectionError:
                retries -= 1

    def export_tables(self, config_path: str):
        with open(config_path, "r", encoding="utf8") as yamlfile:
            tables = yaml.load(yamlfile, Loader=yaml.FullLoader)

        for table in tables["tables"]:
            try:
                self.export_table(table["table_id"], table["table_path"], table["token"], partition_by=table["partition_by"])
            except MissingSchema:
                logger.info(f"Missing schema in table {table['name']}")
            except NonexistingTable:
                logger.info(f"Table {table['name']} does not exist.")

    def __write_export_log(self, table_id: str, path: str, rows: int):
        spark = SparkSession.getActiveSession()
        catalog_name, database_name, _ = self._logging_table_path.split(".")
        self._spark.sql(f"CREATE DATABASE IF NOT EXISTS {catalog_name}.{database_name}")

        export_id = str(uuid.uuid4())
        timestamp = dt.datetime.now()
        logger.info(f"Writing export log '{export_id}'")
        (
            spark.createDataFrame([[export_id, timestamp, table_id, path, rows]], self.__get_logging_schema())
            .write.mode("append")
            .saveAsTable(self._logging_table_path)
        )

    @staticmethod
    def __get_logging_schema():
        return T.StructType(
            [
                T.StructField("export_id", T.StringType(), True),
                T.StructField("timestamp", T.TimestampType(), True),
                T.StructField("table_id", T.StringType(), True),
                T.StructField("table_path", T.StringType(), True),
                T.StructField("rows", T.IntegerType(), True),
            ]
        )
