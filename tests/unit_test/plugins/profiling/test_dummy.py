import pytest

from nefertem.plugins.profiling.dummy import ProfileBuilderDummy, ProfilePluginDummy
from nefertem.utils.commons import DUMMY, FILE_READER, PROFILE
from tests.unit_test.plugins.utils_plugin_tests import (
    correct_execute,
    correct_plugin_build,
    correct_render_artifact,
    correct_render_nefertem,
)


class TestProfilePluginDummy:
    def test_profile(self, setted_plugin):
        output = setted_plugin.profile()
        correct_execute(output)
        assert isinstance(output.artifact, dict)

    def test_render_nefertem(self, setted_plugin):
        result = setted_plugin.profile()
        output = setted_plugin.render_nefertem(result)
        correct_render_nefertem(output, PROFILE)

    def test_render_artifact_method(self, setted_plugin):
        result = setted_plugin.profile()
        output = setted_plugin.render_artifact(result)
        filename = setted_plugin._fn_profile.format(f"{DUMMY}.json")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, dict)
        assert output.artifact[0].filename == filename

    def test_get_lib_name(self, plugin):
        assert plugin().get_lib_name() == DUMMY

    def test_get_lib_version(self, plugin):
        assert plugin().get_lib_version() == DUMMY


class TestProfileBuilderDummy:
    def test_build(self, plugin_builder, plugin_builder_non_val_args):
        plugins = plugin_builder.build(*plugin_builder_non_val_args)
        correct_plugin_build(plugins, ProfilePluginDummy)


@pytest.fixture
def plugin():
    return ProfilePluginDummy


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return ProfileBuilderDummy(**config_plugin_builder)


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
