import pytest

from nefertem.models.constraints.frictionless import ConstraintFrictionless
from nefertem.plugins.utils.frictionless_utils import describe_resource, frictionless_schema_converter


def test_frictionless_schema_converter():
    table_schema = {
        "fields": [
            {"name": "f1", "type": "integer", "format": "default"},
            {"name": "f2", "type": "string", "format": "email"},
            {"name": "f3", "type": "date", "format": "%d/%m/%y"},
        ]
    }
    const = frictionless_schema_converter(table_schema, "test")
    list_const = [
        ConstraintFrictionless(
            name="f1_0",
            title="f1_0",
            resources=["test"],
            weight=5,
            type="frictionless",
            field="f1",
            fieldType="integer",
            constraint="type",
            value="integer",
        ),
        ConstraintFrictionless(
            name="f1_1",
            title="f1_1",
            resources=["test"],
            weight=5,
            type="frictionless",
            field="f1",
            fieldType="integer",
            constraint="format",
            value="default",
        ),
        ConstraintFrictionless(
            name="f2_0",
            title="f2_0",
            resources=["test"],
            weight=5,
            type="frictionless",
            field="f2",
            fieldType="string",
            constraint="type",
            value="string",
        ),
        ConstraintFrictionless(
            name="f2_1",
            title="f2_1",
            resources=["test"],
            weight=5,
            type="frictionless",
            field="f2",
            fieldType="string",
            constraint="format",
            value="email",
        ),
        ConstraintFrictionless(
            name="f3_0",
            title="f3_0",
            resources=["test"],
            weight=5,
            type="frictionless",
            field="f3",
            fieldType="date",
            constraint="type",
            value="date",
        ),
        ConstraintFrictionless(
            name="f3_1",
            title="f3_1",
            resources=["test"],
            weight=5,
            type="frictionless",
            field="f3",
            fieldType="date",
            constraint="format",
            value="%d/%m/%y",
        ),
    ]
    for i, _ in enumerate(const):
        const[i].id = None
        list_const[i].id = None
        assert const[i] == list_const[i]


# fixture to create a temporary file for testing
@pytest.fixture(scope="function")
def tmp_file(tmp_path):
    temp_file = tmp_path / "test.csv"
    temp_file.write_text("name,age\nAlice,25\nBob,30\n")
    return str(temp_file)


# define test functions
def test_describe_resource_returns_dict(tmp_file):
    result = describe_resource(tmp_file)
    assert isinstance(result, dict)


def test_describe_resource_non_empty_dict(tmp_file):
    result = describe_resource(tmp_file)
    assert bool(result)


def test_describe_resource_raises_exception_for_invalid_path():
    with pytest.raises(Exception):
        describe_resource("invalid_path")
