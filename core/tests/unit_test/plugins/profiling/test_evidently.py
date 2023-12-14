import io

import evidently
import pytest
from evidently.report import Report
from nefertem.plugins.profiling.evidently.builder import ProfileBuilderEvidently
from nefertem.plugins.profiling.evidently.plugin import ProfilePluginEvidently
from nefertem.utils.commons import LIBRARY_EVIDENTLY, PANDAS_DATAFRAME_FILE_READER, PROFILE
from tests.conftest import METRIC_EVIDENTLY_01
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


class TestProfilePluginEvidently:
    def test_setup(self, plugin):
        plg = plugin()
        plg.setup("test", "test", "test", "test", "test")
        correct_setup(plg)

    def test_profile(self, setted_plugin):
        # Correct execution
        output = setted_plugin.profile()
        correct_execute(output)
        assert isinstance(output.artifact, Report)

        # Error execution
        setted_plugin.data_reader = "error"
        output = setted_plugin.profile()
        incorrect_execute(output)

    def test_render_nefertem(self, setted_plugin):
        # Correct execution
        result = setted_plugin.profile()
        output = setted_plugin.render_nefertem(result)
        correct_render_nefertem(output, PROFILE)

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.profile()
        output = setted_plugin.render_nefertem(result)
        incorrect_render_nefertem(output, PROFILE)

    def test_render_artifact_method(self, setted_plugin):
        # Correct execution
        result = setted_plugin.profile()
        output = setted_plugin.render_artifact(result)
        filename1 = setted_plugin._fn_profile.format("evidently.json")
        filename2 = setted_plugin._fn_profile.format(f"{LIBRARY_EVIDENTLY}.html")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, io.BytesIO)
        assert output.artifact[0].filename == filename2
        assert isinstance(output.artifact[1].object, io.BytesIO)
        assert output.artifact[1].filename == filename1

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.profile()
        output = setted_plugin.render_artifact(result)
        incorrect_render_artifact(output)
        assert output.artifact[0].filename == filename1

    def test_get_framework_name(self, plugin):
        assert plugin().get_framework_name() == evidently.__name__

    def test_get_framework_version(self, plugin):
        assert plugin().get_framework_version() == evidently.__version__


class TestProfileBuilderEvidently:
    def test_build(self, plugin_builder, plugin_builder_metric_val_args):
        plugins = plugin_builder.build(*plugin_builder_metric_val_args)
        correct_plugin_build(plugins, ProfilePluginEvidently)


@pytest.fixture
def plugin():
    return ProfilePluginEvidently


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return ProfileBuilderEvidently(**config_plugin_builder)


@pytest.fixture
def config_plugin(reader, metric, resource):
    return [reader, resource, metric, {}, reader, resource]


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture
def resource(local_resource):
    return local_resource


@pytest.fixture
def data_reader():
    return PANDAS_DATAFRAME_FILE_READER


@pytest.fixture(params=[METRIC_EVIDENTLY_01])
def metric(request):
    return request.param
