import csv
import os
import shutil
import sqlite3
from io import BytesIO, StringIO
from unittest.mock import MagicMock

import boto3
import duckdb
import pytest
from moto import mock_s3

from nefertem.plugins.utils import Result
from nefertem.plugins.validation.duckdb.constraints import ConstraintDuckDB
from nefertem.plugins.validation.evidently.constraints import ConstraintEvidently, EvidentlyElement, MetricEvidently
from nefertem.plugins.validation.frictionless.constraints import ConstraintFrictionless, ConstraintFullFrictionless
from nefertem.plugins.validation.sqlalchemy.constraints import ConstraintSqlAlchemy
from nefertem.readers.builder import build_reader
from nefertem.resources.data_resource import DataResource
from nefertem.run.run_config import RunConfig
from nefertem.stores.builder import StoreBuilder
from nefertem.utils.commons import LIBRARY_DUCKDB, LIBRARY_EVIDENTLY, LIBRARY_GREAT_EXPECTATIONS, LIBRARY_SQLALCHEMY
from nefertem.utils.utils import listify

##############################
# VARIABLES
##############################

TEST_FILENAME = "test.txt"
S3_BUCKET = "test"
S3_FILENAME = "file.csv"


##############################
# DATA
##############################


# Tmp root
@pytest.fixture(scope="session")
def temp_folder(tmp_path_factory):
    return tmp_path_factory.mktemp("data")


@pytest.fixture(scope="session")
def temp_data(temp_folder):
    return str(temp_folder)


# Sample csv
@pytest.fixture(scope="session")
def data_path_csv(temp_folder):
    tmp = str(temp_folder / "test_csv_file.csv")
    shutil.copy("tests/synthetic_data/test_csv_file.csv", tmp)
    return tmp


# Sample parquet
@pytest.fixture(scope="session")
def data_path_parquet(temp_folder):
    tmp = str(temp_folder / "test_parquet_file.parquet")
    shutil.copy("tests/synthetic_data/test_parquet_file.parquet", tmp)
    return tmp


# Sample sqlite database
# Readapted from https://stackoverflow.com/a/2888042/13195227
@pytest.fixture(scope="session")
def sqlitedb(temp_folder, data_path_csv):
    tmp = str(temp_folder / "test.db")
    con = sqlite3.connect(tmp)
    cur = con.cursor()
    cur.execute("CREATE TABLE test (col1, col2, col3, col4);")
    with open(data_path_csv, "r") as fin:
        dr = csv.DictReader(fin)
        to_db = [(i["col1"], i["col2"], i["col3"], i["col4"]) for i in dr]
    cur.executemany("INSERT INTO test (col1, col2, col3, col4) VALUES (?, ?, ?, ?);", to_db)
    con.commit()
    con.close()
    return f"sqlite:///{tmp}"


# Sample duckdb database
@pytest.fixture(scope="session")
def tmpduckdb(temp_folder, data_path_csv):
    tmp = str(temp_folder / "duckdb.db")
    con = duckdb.connect(tmp)
    sql = f"CREATE TABLE test AS SELECT * FROM read_csv_auto('{data_path_csv}');"
    con.execute(sql)
    con.close()
    return tmp


@pytest.fixture(scope="session")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["MOTO_S3_CUSTOM_ENDPOINTS"] = "http://localhost:9000"


@pytest.fixture(scope="session")
def s3(aws_credentials):
    with mock_s3():
        client = boto3.client("s3", region_name="us-east-1")
        client.create_bucket(Bucket=S3_BUCKET)
        client.upload_file("tests/synthetic_data/test_csv_file.csv", S3_BUCKET, S3_FILENAME)
        yield client


# Sample Result object
@pytest.fixture(scope="session")
def result_obj():
    return Result("test", "test", "test", "test")


# Temporary file
@pytest.fixture(scope="session")
def temp_file(temp_folder):
    file = temp_folder / TEST_FILENAME
    file.write_text("test")
    return file


# StringIO sample
@pytest.fixture
def stringio():
    io = StringIO()
    io.write("test")
    io.seek(0)
    return io


# BytesIO sample
@pytest.fixture
def bytesio():
    io = BytesIO()
    io.write(b"test")
    io.seek(0)
    return io


# Dict sample
@pytest.fixture
def dictionary():
    return {"a": 1, "b": 2}


##############################
# FIXTURES & CONFIGS
##############################

# ---------------
# RUNS
# ---------------


@pytest.fixture
def run_empty():
    return RunConfig()


# ---------------
# STORES
# ---------------


@pytest.fixture
def store_builder():
    return StoreBuilder()


@pytest.fixture
def store(store_cfg, store_builder):
    return store_builder.build_artifact_store(store_cfg)


# ---------------
# Artifact Stores
# ---------------


# Local 1
@pytest.fixture
def local_store_cfg(temp_data):
    return {
        "title": "Local Store",
        "name": "local",
        "type": "local",
        "uri": temp_data,
        "isDefault": True,
    }


# Local 2
@pytest.fixture
def local_store_cfg_2(temp_folder):
    return {
        "title": "Local Store 2",
        "name": "local_2",
        "type": "local",
        "uri": str(temp_folder),
        "isDefault": False,
    }


# SQL
@pytest.fixture
def sql_store_cfg(sqlitedb):
    return {
        "title": "SQLite Store",
        "name": "sql",
        "type": "sql",
        "uri": "sql://test",
        "isDefault": True,
        "config": {"connection_string": sqlitedb},
    }


# S3
@pytest.fixture
def s3_store_cfg():
    return {
        "title": "S3 Store",
        "name": "s3",
        "type": "s3",
        "uri": "s3://test",
        "isDefault": True,
        "config": {
            "aws_access_key_id": "test",
            "aws_secret_access_key": "test",
            "endpoint_url": "http://localhost:9000/",
            "bucket_name": "test",
        },
    }


# ----------------
# Metadata Stores
# ----------------


# Local
@pytest.fixture
def local_md_store_cfg(tmp_path):
    return tmp_path


# ----------------
# DATA READER
# ----------------


@pytest.fixture
def reader(data_reader, store):
    return build_reader(data_reader, store)


# ----------------
# DATA RESOURCES
# ----------------


@pytest.fixture
def local_resource(data_path_csv):
    return DataResource(path=data_path_csv, name="res_test_01", store="local")


@pytest.fixture
def local_resource_no_temp():
    return DataResource(path="tests/synthetic_data/test_csv_file.csv", name="res_test_01", store="local")


@pytest.fixture
def local_resource_2():
    return DataResource(
        path="tests/synthetic_data/test_csv_file_2.csv",
        name="res_test_02",
        store="local",
    )


@pytest.fixture
def sql_resource(sqlitedb):
    return DataResource(path=sqlitedb, name="res_test_01", store="sql")


# ----------------
# CONSTRAINTS
# ----------------

CONST_FRICT_01 = ConstraintFrictionless(
    title="Test frictionless constraint",
    name="test-const-frict-01",
    resources=["res_test_01"],
    field="col1",
    fieldType="string",
    constraint="maxLength",
    value=1,
    weight=5,
)
CONST_FRICT_02 = ConstraintFrictionless(
    title="Test frictionless constraint",
    name="test-const-frict-02",
    resources=["res_test_01"],
    field="col1",
    fieldType="string",
    constraint="minLength",
    value=5,
    weight=5,
)
CONST_FRICT_FULL_01 = ConstraintFullFrictionless(
    title="Test frictionless constraint",
    name="test-const-frict-01",
    resources=["res_test_01"],
    tableSchema={
        "fields": [
            {"name": "col1", "type": "string"},
            {"name": "col2", "type": "number"},
            {"name": "col3", "type": "integer"},
            {"name": "col4", "type": "date"},
        ]
    },
    weight=5,
)
CONST_SQLALCHEMY_01 = ConstraintSqlAlchemy(
    name="const-sqlalc-01",
    title="Test sqlalchemy constraint",
    resources=["res_test_01"],
    query="select * from test",
    expect="non-empty",
    check="rows",
    weight=5,
)
CONST_DUCKDB_01 = ConstraintDuckDB(
    name="const-duckdb-01",
    title="Test duckdb constraint",
    resources=["res_test_01"],
    query="select * from test",
    expect="non-empty",
    check="rows",
    weight=5,
)

CONST_EVIDENTLY_01 = ConstraintEvidently(
    name="const-evidently-01",
    title="Test evidently constraint",
    resources=["res_test_01"],
    resource="res_test_01",
    reference_resource="res_test_01",
    tests=[
        EvidentlyElement(
            type="evidently.test_preset.DataQualityTestPreset",
            values={"columns": ["col1", "col2", "col3"]},
        )
    ],
    weight=5,
)

# ----------------
# METRICS
# ----------------

METRIC_EVIDENTLY_01 = MetricEvidently(
    name="metric-evidently-01",
    title="Test evidently metric",
    resources=["res_test_01"],
    resource="res_test_01",
    reference_resource="res_test_01",
    metrics=[
        EvidentlyElement(
            type="evidently.metric_preset.DataQualityPreset",
            values={"columns": ["col1", "col2", "col3"]},
        )
    ],
    weight=5,
)

# ----------------
# PLUGINS BUILDERS
# ----------------


@pytest.fixture
def config_plugin_builder(store):
    stores = listify(store)
    return {"stores": stores, "exec_args": {}}


@pytest.fixture
def plugin_builder_val_args(resource, constraint, error_report):
    resources = listify(resource)
    constraints = listify(constraint)
    return [resources, constraints, error_report]


@pytest.fixture
def plugin_builder_non_val_args(resource):
    resources = listify(resource)
    return [resources]


@pytest.fixture
def plugin_builder_metric_val_args(resource, metric):
    resources = listify(resource)
    metrics = listify(metric)
    return [resources, metrics]


# ----------------
# PLUGINS
# ----------------


@pytest.fixture
def setted_plugin(plugin, config_plugin):
    plg = plugin()
    plg.setup(*config_plugin)
    return plg


@pytest.fixture(params=["partial", "full", "count"])
def error_report(request):
    return request.param


##############################
# MOCKS
##############################

# ----------------
# Factory
# ----------------


def mock_object_factory(**kwargs):
    mock_obj = MagicMock()
    for k, v in kwargs.items():
        setattr(mock_obj, k, v)
    return mock_obj


# ----------------
# Mock constraints
# ----------------

mock_c_frict = mock_object_factory(type="frictionless")
mock_c_frict_full = mock_object_factory(type="frictionless_full")
mock_c_duckdb = mock_object_factory(type=LIBRARY_DUCKDB)
mock_c_gex = mock_object_factory(type=LIBRARY_GREAT_EXPECTATIONS)
mock_c_sqlalc = mock_object_factory(type=LIBRARY_SQLALCHEMY)
mock_c_evidently = mock_object_factory(type=LIBRARY_EVIDENTLY)

# ----------------
# Generic mock objects (c = constraint, r = resources, s = store)
# ----------------

mock_c_generic = mock_object_factory(type="generic", resources=["resource"])
mock_r_generic = mock_object_factory(name="resource", store="store")
mock_s_generic = mock_object_factory(name="store", type="generic")
mock_c_to_fail = mock_object_factory(type="generic", resources=["resource_fail"])
mock_r_to_fail = mock_object_factory(name="resource_fail", store="fail")
mock_s_to_fail = mock_object_factory(name="fail", type="fail")
