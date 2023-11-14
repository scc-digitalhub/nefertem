import pytest

from nefertem.plugins.inference.dummy import InferenceBuilderDummy, InferencePluginDummy
from nefertem.utils.commons import DUMMY, FILE_READER, INFER
from tests.unit_test.plugins.utils_plugin_tests import (
    correct_execute,
    correct_plugin_build,
    correct_render_artifact,
    correct_render_nefertem,
)


class TestInferencePluginDummy:
    def test_infer(self, setted_plugin):
        output = setted_plugin.infer()
        correct_execute(output)
        assert isinstance(output.artifact, dict)

    def test_render_nefertem(self, setted_plugin):
        result = setted_plugin.infer()
        output = setted_plugin.render_nefertem(result)
        correct_render_nefertem(output, INFER)

    def test_render_artifact_method(self, setted_plugin):
        result = setted_plugin.infer()
        output = setted_plugin.render_artifact(result)
        filename = setted_plugin._fn_schema.format(f"{DUMMY}.json")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, dict)
        assert output.artifact[0].filename == filename

    def test_get_framework_name(self, plugin):
        assert plugin().get_framework_name() == DUMMY

    def test_get_framework_version(self, plugin):
        assert plugin().get_framework_version() == DUMMY


class TestInferenceBuilderDummy:
    def test_build(self, plugin_builder, plugin_builder_non_val_args):
        plugins = plugin_builder.build(*plugin_builder_non_val_args)
        correct_plugin_build(plugins, InferencePluginDummy)


@pytest.fixture
def plugin():
    return InferencePluginDummy


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return InferenceBuilderDummy(**config_plugin_builder)


@pytest.fixture
def config_plugin(reader, resource):
    return [reader, resource, {}]


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture
def resource(local_resource):
    return local_resource


@pytest.fixture
def data_reader():
    return FILE_READER
