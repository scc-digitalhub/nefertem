# content of test_inference_plugin_frictionless.py

import frictionless
import pytest
from frictionless import Schema
from nefertem_core.plugins.inference.frictionless.builder import InferenceBuilderFrictionless
from nefertem_core.plugins.inference.frictionless.plugin import InferencePluginFrictionless
from nefertem_core.utils.commons import FILE_READER, INFER
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


class TestInferencePluginFrictionless:
    def test_setup(self, plugin):
        plg = plugin()
        plg.setup("test", "test", "test")
        correct_setup(plg)

    def test_infer(self, setted_plugin):
        # Correct execution
        output = setted_plugin.infer()
        correct_execute(output)
        assert isinstance(output.artifact, Schema)

        # Error execution
        setted_plugin.data_reader = "error"
        output = setted_plugin.infer()
        incorrect_execute(output)

    def test_render_nefertem(self, setted_plugin):
        # Correct execution
        result = setted_plugin.infer()
        output = setted_plugin.render_nefertem(result)
        correct_render_nefertem(output, INFER)

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.infer()
        output = setted_plugin.render_nefertem(result)
        incorrect_render_nefertem(output, INFER)

    def test_render_artifact_method(self, setted_plugin):
        # Correct execution
        result = setted_plugin.infer()
        output = setted_plugin.render_artifact(result)
        filename = setted_plugin._fn_schema.format("frictionless.json")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, dict)
        assert output.artifact[0].filename == filename

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.infer()
        output = setted_plugin.render_artifact(result)
        incorrect_render_artifact(output)
        assert output.artifact[0].filename == filename

    def test_get_framework_name(self, plugin):
        assert plugin().get_framework_name() == frictionless.__name__

    def test_get_framework_version(self, plugin):
        assert plugin().get_framework_version() == frictionless.__version__


class TestInferenceBuilderFrictionless:
    def test_build(self, plugin_builder, plugin_builder_non_val_args):
        plugins = plugin_builder.build(*plugin_builder_non_val_args)
        correct_plugin_build(plugins, InferencePluginFrictionless)


@pytest.fixture
def plugin():
    return InferencePluginFrictionless


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return InferenceBuilderFrictionless(**config_plugin_builder)


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
