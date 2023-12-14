import evidently
import pytest
from evidently.test_suite import TestSuite
from nefertem.plugins.validation.evidently.builder import ValidationBuilderEvidently
from nefertem.plugins.validation.evidently.plugin import ValidationPluginEvidently
from nefertem.utils.commons import PANDAS_DATAFRAME_FILE_READER, VALIDATE
from tests.conftest import CONST_EVIDENTLY_01, mock_c_evidently, mock_c_generic
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


class TestValidationPluginEvidently:
    def test_setup(self, plugin):
        plg = plugin()
        plg.setup("test", "test", "test", "test", "test")
        correct_setup(plg)

    def test_validate(self, setted_plugin):
        # Correct execution
        output = setted_plugin.validate()
        correct_execute(output)
        assert isinstance(output.artifact, TestSuite)

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
        filename = setted_plugin._fn_report.format("evidently.json")
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
        assert plugin().get_framework_name() == evidently.__name__

    def test_get_framework_version(self, plugin):
        assert plugin().get_framework_version() == evidently.__version__


class TestValidationBuilderEvidently:
    def test_build(self, plugin_builder, plugin_builder_val_args):
        plugins = plugin_builder.build(*plugin_builder_val_args)
        correct_plugin_build(plugins, ValidationPluginEvidently)

    # fmt: off
    @pytest.mark.parametrize(
        "const_list,len_list",
        [
            ([mock_c_evidently, mock_c_evidently,], 2),
            ([mock_c_evidently, mock_c_generic,], 1),
            ([mock_c_generic,], 0),
            ([mock_c_generic, mock_c_generic,], 0),
        ]
    )
    # fmt: on
    def test_filter_constraints(self, plugin_builder, const_list, len_list):
        assert len(plugin_builder._filter_constraints(const_list)) == len_list


@pytest.fixture
def plugin():
    return ValidationPluginEvidently


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return ValidationBuilderEvidently(**config_plugin_builder)


@pytest.fixture
def config_plugin(reader, constraint, resource, error_report):
    return [reader, resource, constraint, error_report, {}, reader, resource]


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture
def resource(local_resource):
    return local_resource


@pytest.fixture
def data_reader():
    return PANDAS_DATAFRAME_FILE_READER


@pytest.fixture(params=[CONST_EVIDENTLY_01])
def constraint(request):
    return request.param
