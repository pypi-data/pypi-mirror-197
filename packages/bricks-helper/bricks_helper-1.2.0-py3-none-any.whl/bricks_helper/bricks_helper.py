from pyspark.sql import SparkSession, DataFrame
from dataclasses import dataclass, field

try:
    from pyspark.dbutils import DBUtils
except Exception:
    pass

import base64
import os
import json
import pendulum
import requests
import time
from pathlib import Path
from enum import Enum


class NotebookAction(Enum):
    IMPORT = "import"
    DELETE = "delete"
    LIST = "list"


class DatabricksConfig:
    """
    A class to configure various databricks helper attributes

    Parameters
    ----------
    spark : SparkSession
        A spark session object

    profile_alias : str
        The name of the profile (alias name) for executing against
        Default:  FS

    return_rows : int
        The number of rows to return for the executed query
        Default: 250

    max_columns : int
        If the number of columns for a query exceeds this, data will be output\
            vertically
        Default: 10

    select_query_only : bool
        If true, only select statements will be executed
        Default: False

    sort_alpha : bool
        If true, sort entity columns alphabetically
        Default: False

    append_comma: bool
        If true, commas will be appended to column list
        Default: False
    """

    def __init__(
        self,
        spark: SparkSession,
        profile_alias: str = "FS",
        return_rows: int = 250,
        max_columns: int = 10,
        select_query_only: bool = False,
        print_query: bool = False,
        sort_alpha=False,
        append_comma=False,
    ):
        self.spark = spark
        self.profile_alias = profile_alias if _profile_exists(profile_alias) else None
        self.return_rows = return_rows
        self.max_columns = max_columns
        self.select_query_only = select_query_only
        self.print_query = print_query
        self.sort_alpha = sort_alpha
        self.append_comma = append_comma


@dataclass
class OSPaths:
    hadoop_home: str = field(default=r"C:\Files\ScoopApps\apps\hadoop-winutils\current")
    pyspark_python: str = field(
        default=r"C:\Files\ScoopApps\apps\python\current\python.exe"
    )
    java_home: str = field(default=r"C:\Files\ScoopApps\apps\temurin8-jdk\current")


def jupyter_support_config() -> None:
    from IPython.core.magic import line_cell_magic, Magics, magics_class

    @magics_class
    class DatabricksConnectMagics(Magics):
        @line_cell_magic
        def sql(self, line, cell=None):
            if cell and line:
                raise ValueError("Line must be empty for cell magic", line)
            try:
                from autovizwidget.widget.utils import display_dataframe
            except ImportError:
                pass

                def display_dataframe(x):
                    return x

            return display_dataframe(self.get_spark().sql(cell or line).toPandas())

        def get_spark(self):
            user_ns = get_ipython().user_ns  # noqa: F821
            if "spark" in user_ns:
                return user_ns["spark"]
            else:
                from pyspark.sql import SparkSession

                user_ns["spark"] = SparkSession.builder.getOrCreate()
                return user_ns["spark"]

    ip = get_ipython()  # noqa: F821
    ip.register_magics(DatabricksConnectMagics)


def set_root_path(input_root_path: str) -> None:
    """A function to set the root path of the databricks project"""
    global root_path
    root_path = input_root_path


def get_root_path() -> str:
    """A function to return root path of the databricks project"""
    if root_path is None:
        print("root_path not set; execute the function set_root_path")
    else:
        return root_path


def __read_files_profiles() -> str:
    """A helper function, to read profiles from local config file"""
    databricks_config = f"{get_root_path()}\\config\\configs.json"
    with open(databricks_config, "r") as _databricks_config:
        configs = json.load(_databricks_config)

    return configs


def __get_profile_key_value() -> str:
    """A helper function to return all profiles"""

    profiles = {value["alias"]: key for (key, value) in __read_files_profiles().items()}

    return profiles


def __get_profile_name(profile_alias: str) -> str:
    """
    A helper function to return profile attributes for a passed profile alias

    Parameters
    ----------
        profile_alias : str
    """

    profiles = __get_profile_key_value()
    try:
        return profiles[profile_alias] or profile_alias
    except KeyError:
        return profile_alias


def print_env(profile_alias: str) -> None:
    """
    A function to print the current profile that is set

    Parameters
    ----------
    profile_alias : str
        The profile alias for identifying the active profile
    """

    print(f"Profile => {__get_profile_name(profile_alias)}\n")


def __print_error_msg(msg: str) -> None:
    """
    A function to print a standardized error message

    Parameters
    ----------
    msg : str
        The error message to print
    """
    print("\n========================> ERROR <========================\n")
    print(f"{msg}")
    print("========================> ERROR <========================\n")


def _profile_exists(profile_alias: str) -> bool:
    """
    A helper function to determine if a profile with given alias exists
    Parameters
    ----------
    profile_alias : str
        The profile alias for identifying the active profile
    """
    profile_name = __get_profile_name(profile_alias)

    return not (profile_name == profile_alias)


def set_env(spark: SparkSession, profile_alias: str) -> None:
    """
    A function to set a variety of spark related settings

    Parameters
    ----------
    spark : SparkSession
        A spark session object

    profile_alias : str
        The profile alias for identifying the active profile
    """

    configs = __read_files_profiles()
    profile_name = __get_profile_name(profile_alias)

    if _profile_exists(profile_alias):
        host = configs[profile_name]["host"]
        token = configs[profile_name]["token"]
        cluster_id = configs[profile_name]["cluster_id"]
        org_id = configs[profile_name]["org_id"]

        spark.conf.set("spark.databricks.service.address", host)
        spark.conf.set("spark.databricks.service.token", token)
        spark.conf.set("spark.databricks.service.clusterId", cluster_id)
        spark.conf.set("spark.databricks.service.orgId", org_id)
        spark.conf.set("spark.databricks.service.profile", profile_name)
        spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
        spark.conf.set("spark.sql.shuffle.partitions", 960),

        print_env(profile_alias)
    else:
        msg = f"Profile with alias {profile_alias} does not exist\n"
        __print_error_msg(msg)


def set_os_paths(
    hadoop_home: str = "", java_home: str = "", pyspark_python: str = ""
) -> None:
    osp = OSPaths(
        hadoop_home=hadoop_home, java_home=java_home, pyspark_python=pyspark_python
    )

    """A function for setting OS environment variables, required by spark"""
    hadoop_home = osp.hadoop_home
    if not (Path(hadoop_home).exists()):
        print(f"HADOOP_HOME was not set - the path {hadoop_home} was not found")
        hadoop_home = input("Enter an alternative path: ")
        print(f"HADOOP_HOME set to {hadoop_home}")

    pyspark_python = osp.pyspark_python
    if not (Path(pyspark_python).exists()):
        print(f"PYSPARK_PYTHON was not set - the path {pyspark_python} was not found")
        pyspark_python = input("Enter an alternative path: ")
        print(f"PYSPARK_PYTHON set to {pyspark_python}")

    java_home = osp.java_home
    if not (Path(java_home).exists()):
        print(f"JAVA_HOME was not set - the path {java_home} was not found")
        java_home = input("Enter an alternative path: ")
        print(f"JAVA_HOME set to {java_home}")

    os.environ["HADOOP_HOME"] = hadoop_home
    os.environ["PYSPARK_PYTHON"] = pyspark_python
    os.environ["JAVA_HOME"] = java_home


def get_entity_columns(databricks_config: DatabricksConfig, df: DataFrame) -> None:
    """
    A function for capturing and printing columns, for a given entity

    Parameters
    ----------
    databricks_config : DBConfig
        A databricks config object

    entity : string
        An entity path to query against
    """
    if not (databricks_config.profile_alias):
        msg = "Profile not properly set; quitting\n"
        __print_error_msg(msg)
        return

    print_env(databricks_config.profile_alias)

    sort_alpha = databricks_config.sort_alpha
    append_comma = databricks_config.append_comma

    print(f"Row count: {df.count()}\n")

    try:
        names = df.schema.names
        if names:
            if sort_alpha:
                names.sort()

            for name in names:
                if append_comma:
                    name += ","
                print(name)
    except Exception as ex:
        __print_error_msg(ex)


def __get_childitem_old(
    databricks_config: DatabricksConfig,
    path: str,
    depth: int = 1,
    verbose: bool = False,
    __current_depth: int = 0,
) -> None:
    """
    A function for printing entity folders

    Parameters
    ----------
    databricks_config : DatabricksConfig
        A databricks config object

    path : string
        An entity path to query against

    depth : int
        The max number of child folders, to traverse

    verbose : bool
        If set to true, when an exception occurs, the exception
        message will be printed
    """

    if not (databricks_config.profile_alias):
        msg = "Profile not properly set; quitting\n"
        __print_error_msg(msg)

    if path and path[0:1] == "/":
        path += "/"
        path = path.replace("//", "/")

    spark = databricks_config.spark

    if __current_depth == 0:
        print_env(databricks_config.profile_alias)

    if path[0:1] == "/" and not (__entity_exists(spark, path)):
        msg = f"Path: {path} not found\n"
        __print_error_msg(msg)
        return

    if __current_depth <= depth:
        dbutils = DBUtils(spark)

        path = path.replace("dbfs:", "")
        print(path.rjust(len(path) + (__current_depth * 4)))
        i_depth = __current_depth + 1

        try:
            current_paths = dbutils.fs.ls(path)
        except Exception as ex:
            error_message = f"\n** ERROR ** reading {path}"
            if verbose:
                error_message += f" -> {ex}"

            print(error_message.rjust(len(error_message) + (__current_depth * 4)))
            return

        current_paths_filtered = []
        for current_path in current_paths:
            if current_path.path[-1] == "/" or current_path.name[-4:] == "json":
                current_paths_filtered.append(current_path.path)

        for current_path in current_paths_filtered:
            if path[-1] == "/":
                get_childitem(databricks_config, current_path, depth, verbose, i_depth)


def get_views(databricks_config: DatabricksConfig, database_name: str):
    """
    A function that will list all views, contained in a provided database

    Parameters
    ----------
    databricks_config : DatabricksConfig
        A databricks config object

    database_name : str
        The name of the containing database
    """

    if not (databricks_config.profile_alias):
        msg = "Profile not properly set; quitting\n"
        __print_error_msg(msg)
        return

    spark = databricks_config.spark

    print_env(databricks_config.profile_alias)

    sql = f"SHOW VIEWS IN {database_name}"

    try:
        df = spark.sql(sqlQuery=sql)
        data_rows = df.sort("viewName", ascending=True).collect()

        print(f"Database: {database_name}\n")

        for index, data_row in enumerate(data_rows):
            view_name = data_row["viewName"]
            # print(f"{view_name} - {index}")
            print(f"    {view_name}")

        print(f"\nView count: {df.count():,}")
    except Exception as ex:
        __print_error_msg(f"{ex}\n")


def get_view_definition(
    databricks_config: DatabricksConfig, database_name: str, view_name: str
) -> None:
    """
    A function that will print the definition of a provided view

    Parameters
    ----------
    databricks_config : DatabricksConfig
        A databricks config object

    database_name : str
        The name of the containing database

    view_name : str
        The name of the view
    """

    if not (databricks_config.profile_alias):
        msg = "Profile not properly set; quitting\n"
        __print_error_msg(msg)
        return

    spark = databricks_config.spark

    print_env(databricks_config.profile_alias)

    sql = f"DESCRIBE TABLE EXTENDED {database_name}.{view_name}"

    try:
        df = spark.sql(sqlQuery=sql)
        view_def = [
            row.data_type for row in df.rdd.collect() if row.col_name == "View Text"
        ]

        print(f"Database: {database_name}\nView: {view_name}\n\n{view_def[0]}\n")
    except Exception as ex:
        __print_error_msg(f"{ex}\n")


def __entity_exists(spark: SparkSession, entity: str) -> bool:
    """
    A helper function that will return a true if a file exists, otherwise false

    entity : string
        An entity path (file or folder)
    """
    dbutils = DBUtils(spark)

    try:
        dbutils.fs.ls(entity)
        return True
    except Exception:
        return False


def __entity_exists_api(databricks_config: DatabricksConfig, entity: str) -> bool:
    profile_alias = databricks_config.profile_alias

    profile = __get_profile_name(profile_alias)
    configs = __read_files_profiles()

    host = configs[profile]["host"]
    token = configs[profile]["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {"path": f"{entity}"}

    uri = f"{host}api/2.0/dbfs/get-status"
    resp = requests.get(url=uri, headers=headers, json=data)
    if resp.status_code == 200:
        return True
    else:
        msg = json.loads(resp.content)
        if msg["error_code"] == "RESOURCE_DOES_NOT_EXIST":
            return False
        else:
            return True


def delete_entity(databricks_config: DatabricksConfig, entity: str) -> None:
    """
    A function for deleting a file/folder

    Parameters
    ----------
    databricks_config : DBCongig
        A databricks config object

    entity : string
        An entity path (file or folder) to delete
    """

    if not (databricks_config.profile_alias):
        msg = "Profile not properly set; quitting\n"
        __print_error_msg(msg)
        return

    if entity and entity[0:1] == "/":
        entity += "/"
        entity = entity.replace("//", "/")

    spark = databricks_config.spark
    dbutils = DBUtils(spark)

    print_env(databricks_config.profile_alias)

    print(f"Entity: {entity}\n")

    entity_exists = __entity_exists(spark, entity)

    resp = (input("Are you sure you wish to delete (y/N)?") or "N").lower()
    if resp == "n":
        print("** Delete canceled; quitting **")
        return

    if entity_exists:
        check_count = 0
        while entity_exists and check_count < 6:
            dbutils.fs.rm(entity, recurse=True)

            check_count += 1
            time.sleep(5)

            entity_exists = __entity_exists(spark, entity)

        if check_count > 0 and entity_exists:
            msg = f"Entity: {entity} was **NOT** deleted in a timely manner\n"
            __print_error_msg(msg)
            return

        print(f"Entity: {entity} was deleted\n")
    else:
        msg = f"Entity: {entity} not found\n"
        __print_error_msg(msg)


def __workspace_folder_exists(
    databricks_config: DatabricksConfig, publish_location: str
) -> bool:
    """
    A helper function for determining if a workspace folder exists.  A return of True,\
    means the folder(s) was created

    Parameters
    ----------
    databricks_config : DatabricksConfig
        A databricks config object

    publish_location : str
        The location to publish the notebook file
    """
    profile_alias = databricks_config.profile_alias
    profile = __get_profile_name(profile_alias)
    configs = __read_files_profiles()

    host = configs[profile]["host"]
    token = configs[profile]["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    req = {"path": publish_location}

    uri = f"{host}api/2.0/workspace/get-status"
    resp = requests.get(url=uri, headers=headers, json=req)

    return resp.status_code == 200


def __workspace_create_folder(
    databricks_config: DatabricksConfig, publish_location: str
) -> bool:
    """
    A helper function for create a workspace folder.  A return of True, means the\
    folder(s) was created

    Parameters
    ----------
    databricks_config : DatabricksConfig
        A databricks config object

    publish_location : str
        The location to publish the notebook file
    """
    profile_alias = databricks_config.profile_alias
    profile = __get_profile_name(profile_alias)
    configs = __read_files_profiles()

    host = configs[profile]["host"]
    token = configs[profile]["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    req = {"path": publish_location}

    uri = f"{host}api/2.0/workspace/mkdirs"
    resp = requests.post(url=uri, headers=headers, json=req)

    return resp.status_code == 200


def __execute_notebook_action(
    databricks_config: DatabricksConfig,
    publish_location: str,
    notebook_path: str = None,
    action: NotebookAction = NotebookAction.IMPORT,
) -> None:
    """
    A helper function for deleting/importing notebook files

    Parameters
    ----------
    databricks_config : DatabricksConfig
        A databricks config object

    notebook_path : str
        The path to the notebrick file

    publish_location : str
        The location to publish the notebook file

    action : NotebookAction
        The enumerable action to perform
    """

    profile_alias = databricks_config.profile_alias
    profile = __get_profile_name(profile_alias)
    configs = __read_files_profiles()

    host = configs[profile]["host"]
    token = configs[profile]["token"]

    if action == NotebookAction.IMPORT:
        if not (__workspace_folder_exists(databricks_config, publish_location)):
            if not (__workspace_create_folder(databricks_config, publish_location)):
                msg = f"Could not create workspace folder {publish_location}\n"
                __print_error_msg(msg)
                return

        language = (
            Path(notebook_path).suffix.replace(".", "").upper().replace("PY", "PYTHON")
        )
        with open(notebook_path, "r") as f:
            fileContents = f.readlines()
            fileContentsJoined = "".join(fileContents)
            b64FileContents = base64.b64encode(
                fileContentsJoined.encode("utf8")
            ).decode("utf8")

        notebook_path = f"{publish_location}{Path(notebook_path).stem}"
    elif action != NotebookAction.IMPORT:
        if action == NotebookAction.LIST:
            notebook_path = f"/{publish_location}"
        else:
            notebook_path = f"/{publish_location}/{notebook_path}"

        if not (__workspace_folder_exists(databricks_config, notebook_path)):
            msg = f"Object {notebook_path} not found\n"
            __print_error_msg(msg)
            return

        language = None
        b64FileContents = None

    notebook_path = notebook_path.replace("//", "/")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    req = {
        "path": notebook_path,
        "format": "SOURCE",
        "language": language,
        "content": b64FileContents,
        "overwrite": True,
    }

    uri = f"{host}api/2.0/workspace/{action.value}"
    if action != NotebookAction.LIST:
        resp = requests.post(url=uri, headers=headers, json=req)
    else:
        resp = requests.get(url=uri, headers=headers, json=req)

    if resp.status_code != 200:
        print(f"**ERROR** {resp.content}")
    else:
        if action == NotebookAction.DELETE:
            print(f"Object deleted: {notebook_path}\n")
        elif action == NotebookAction.IMPORT:
            print(f"Notebook imported: {notebook_path}\n")
        else:
            content = json.loads(resp.content)
            if content:
                for notebook in content["objects"]:
                    print(
                        f"Type: {notebook.get('object_type', 'N/A')} :: Path:\
                        {notebook.get('path', 'N/A')} :: Language:\
                        {notebook.get('language', 'N/A')}"
                    )
            else:
                print(f"{publish_location.replace('//', '/')} is empty\n")


def manage_notebook(
    databricks_config: DatabricksConfig,
    publish_location: str,
    notebook_path: str = None,
    action: NotebookAction = NotebookAction.IMPORT,
) -> None:
    """
    A function for managing databrick notebooks

    Parameters
    ----------
    databricks_config : DatabricksConfig
        A databricks config object

    notebook_path : str
        The path to the notebrick file/directory of notebooks

    publish_location : str
        The location to publish the notebook file

    action : NotebookAction
        The enumerable action to perform
    """

    if not (databricks_config.profile_alias):
        msg = "Profile not properly set; quitting\n"
        __print_error_msg(msg)
        return

    print_env(databricks_config.profile_alias)

    if action == NotebookAction.IMPORT and Path(notebook_path).is_dir():
        notebook_files = (
            list(Path(notebook_path).glob("*.sql"))
            + list(Path(notebook_path).glob("*.py"))
            + list(Path(notebook_path).glob("*.scala"))
        )

        for notebook_file in notebook_files:
            __execute_notebook_action(
                databricks_config, publish_location, notebook_file, action
            )
    else:
        __execute_notebook_action(
            databricks_config, publish_location, notebook_path, action
        )


def get_last_file_update(databricks_config: DatabricksConfig, entity: str) -> None:
    """
    A function for printing the last update of an entity
    The basis for last update, is based on the newest file in the provided entity folder

    Parameters
    ----------
    databricks_config : DatabricksConfig
        A databricks config object

    entity : str
        The path of the entity
    """

    if not (databricks_config.profile_alias):
        msg = "Profile not properly set; quitting\n"
        __print_error_msg(msg)
        return

    if entity and entity[0:1] == "/":
        entity += "/"
        entity = entity.replace("//", "/")

    profile_alias = databricks_config.profile_alias
    print_env(profile_alias)

    if entity[0:1] == "/" and not (__entity_exists_api(databricks_config, entity)):
        msg = f"Entity  : {entity} not found\n"
        __print_error_msg(msg)
        return

    profile = __get_profile_name(profile_alias)
    configs = __read_files_profiles()

    host = configs[profile]["host"]
    token = configs[profile]["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {"path": f"{entity}"}

    uri = f"{host}api/2.0/dbfs/list"
    resp = requests.get(url=uri, headers=headers, json=data)

    resp_json = json.loads(resp.text)

    max_mod_epochtime = max(item["modification_time"] for item in resp_json["files"])

    max_mod_time = pendulum.from_timestamp(
        max_mod_epochtime / 1000, tz="America/Vancouver"
    )
    max_mod_time = max_mod_time.strftime("%m/%d/%Y %H:%M:%S-%Z")

    print(f"Entity: {entity}\n")
    print(f"    Last Modified: {max_mod_time}")


def get_childitem(
    databricks_config: DatabricksConfig,
    path: str,
    depth: int = 1,
    __current_depth: int = 0,
) -> None:
    """
    A function for printing entity folders

    Parameters
    ----------
    databricks_config : DatabricksConfig
        A databricks config object

    path : string
        An entity path to query against

    depth : int
        The max number of child folders, to traverse
    """
    if not (databricks_config.profile_alias):
        msg = "Profile not properly set; quitting\n"
        __print_error_msg(msg)
        return

    profile_alias = databricks_config.profile_alias
    print_env(profile_alias)

    profile = __get_profile_name(profile_alias)
    configs = __read_files_profiles()

    host = configs[profile]["host"]
    token = configs[profile]["token"]

    uri = f"{host}api/2.0/dbfs/list"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = {"path": f"{path}"}

    if __current_depth <= depth:
        i_depth = __current_depth + 1
        resp = requests.get(url=uri, headers=headers, json=data)

        if resp.status_code == 200:
            text_resp = json.loads(resp.text)
            if "files" in text_resp:
                for file in text_resp["files"]:
                    sub_path = file["path"]
                    if file["is_dir"]:
                        print(sub_path.rjust(len(sub_path) + (__current_depth * 4)))
                        get_childitem(databricks_config, sub_path, depth, i_depth)
