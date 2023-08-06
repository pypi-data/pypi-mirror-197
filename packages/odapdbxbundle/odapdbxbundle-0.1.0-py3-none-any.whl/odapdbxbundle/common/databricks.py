import IPython
from pyspark.dbutils import DBUtils
from pyspark.sql import SparkSession
from databricks_cli.workspace.api import WorkspaceApi
from databricks_cli.repos.api import ReposApi
from databricks_cli.sdk.api_client import ApiClient


def resolve_dbutils() -> DBUtils:
    ipython = IPython.get_ipython()

    if not hasattr(ipython, "user_ns") or "dbutils" not in ipython.user_ns:  # type: ignore
        raise Exception("dbutils cannot be resolved")

    return ipython.user_ns["dbutils"]  # type: ignore


def get_workspace_api() -> WorkspaceApi:
    api_client = ApiClient(host=get_host(), token=get_token())
    return WorkspaceApi(api_client)


def get_repos_api() -> ReposApi:
    api_client = ApiClient(host=get_host(), token=get_token())
    return ReposApi(api_client)


def get_host() -> str:
    spark = SparkSession.getActiveSession()
    return f"https://{spark.conf.get('spark.databricks.workspaceUrl')}"


def get_token() -> str:
    dbutils = resolve_dbutils()
    return dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()


def get_username() -> str:
    dbutils = resolve_dbutils()
    return dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()