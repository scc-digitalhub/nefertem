from copy import deepcopy

import frictionless
import pytest
from frictionless import Report, Schema
from frictionless.exception import FrictionlessException
from nefertem_core.plugins.validation.frictionless.builder import ValidationBuilderFrictionless
from nefertem_core.plugins.validation.frictionless.plugin import ValidationPluginFrictionless
from nefertem_core.utils.commons import FILE_READER, VALIDATE
from tests.conftest import CONST_FRICT_01, CONST_FRICT_FULL_01, mock_c_frict, mock_c_frict_full, mock_c_generic
from tests.unit_test.plugins.utils_plugin_tests import (
    correct_execute,
    correct_plugin_build,
    correct_render_artifact,
    correct_render_nefertem,
    correct_setup,
    incorrect_execute,
    incorrect_render_artifact,
    incorrect_render_nefertem,
)


class TestValidationPluginFrictionless:
    def test_setup(self, plugin):
        plg = plugin()
        plg.setup("test", "test", "test", "test", "test")
        correct_setup(plg)

    def test_validate(self, setted_plugin):
        # Correct execution
        output = setted_plugin.validate()
        correct_execute(output)
        assert isinstance(output.artifact, Report)

        # Error execution
        setted_plugin.data_reader = "error"
        output = setted_plugin.validate()
        incorrect_execute(output)

    def test_render_nefertem(self, setted_plugin):
        # Correct execution
        result = setted_plugin.validate()
        output = setted_plugin.render_nefertem(result)
        correct_render_nefertem(output, VALIDATE)

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.validate()
        output = setted_plugin.render_nefertem(result)
        incorrect_render_nefertem(output, VALIDATE)

    def test_render_artifact_method(self, setted_plugin):
        # Correct execution
        result = setted_plugin.validate()
        output = setted_plugin.render_artifact(result)
        filename = setted_plugin._fn_report.format("frictionless.json")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, dict)
        assert output.artifact[0].filename == filename

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.validate()
        output = setted_plugin.render_artifact(result)
        incorrect_render_artifact(output)
        assert output.artifact[0].filename == filename

    def test_get_framework_name(self, plugin):
        assert plugin().get_framework_name() == frictionless.__name__

    def test_get_framework_version(self, plugin):
        assert plugin().get_framework_version() == frictionless.__version__

    def test_rebuild_constraints(self, setted_plugin):
        # Correct execution
        path = setted_plugin.data_reader.fetch_data(setted_plugin.resource.path)
        schema = setted_plugin._rebuild_constraints(path)
        assert isinstance(schema, Schema)

        # Error execution (malformed table schema)
        if setted_plugin.constraint.type == "frictionless_full":
            with pytest.raises(FrictionlessException):
                # Deepcopy plugin, otherwise setting constraint
                # influence subsequent tests
                plg = deepcopy(setted_plugin)
                plg.constraint.table_schema = "error"
                plg._rebuild_constraints(None)

    def test_get_schema(self, plugin, data_path_csv, data_path_parquet):
        assert isinstance(plugin._get_schema(data_path_csv), dict)
        assert plugin._get_schema(data_path_parquet) == {"fields": []}
        with pytest.raises(FrictionlessException):
            plugin._get_schema("error")


class TestValidationBuilderFrictionless:
    def test_build(self, plugin_builder, plugin_builder_val_args):
        plugins = plugin_builder.build(*plugin_builder_val_args)
        correct_plugin_build(plugins, ValidationPluginFrictionless)

    # fmt: off
    @pytest.mark.parametrize(
        "const_list,len_list",
        [
            ([mock_c_frict, mock_c_frict, mock_c_frict_full,], 3),
            ([mock_c_frict, mock_c_frict,], 2),
            ([mock_c_frict_full, mock_c_frict_full,], 2),
            ([mock_c_frict, mock_c_frict_full, mock_c_generic,], 2),
            ([mock_c_frict, mock_c_generic,], 1),
            ([mock_c_frict_full, mock_c_generic,], 1),
            ([mock_c_generic,], 0),
            ([mock_c_generic, mock_c_generic,], 0),

        ]
    )
    # fmt: on
    def test_filter_constraints(self, plugin_builder, const_list, len_list):
        assert len(plugin_builder._filter_constraints(const_list)) == len_list


@pytest.fixture
def plugin():
    return ValidationPluginFrictionless


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return ValidationBuilderFrictionless(**config_plugin_builder)


@pytest.fixture
def config_plugin(reader, constraint, resource, error_report):
    return [reader, resource, constraint, error_report, {}]


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture
def resource(local_resource_no_temp):
    # Otherwise the plugin will give error for unsafe path
    return local_resource_no_temp


@pytest.fixture
def data_reader():
    return FILE_READER


@pytest.fixture(params=[CONST_FRICT_01, CONST_FRICT_FULL_01])
def constraint(request):
    return request.param
