from __future__ import annotations

import typing
from unittest.mock import Mock

import pytest
from nefertem_core.plugins.builder import PluginBuilder
from nefertem_core.plugins.plugin import Plugin
from nefertem_core.resources.data_resource import DataResource
from nefertem_core.utils.exceptions import StoreError

if typing.TYPE_CHECKING:
    from nefertem_core.plugins.utils import Result


class SamplePlugin(Plugin):
    """
    Sample concrete plugin implementation for testing.
    """

    def setup(self, *args, **kwargs) -> None:
        ...

    def execute(self) -> dict:
        return {"result": "success"}

    def render_nefertem(self, obj: Result) -> Result:
        return obj  # dummy implementation for testing

    def render_artifact(self, obj: Result) -> Result:
        return obj  # dummy implementation for testing

    @staticmethod
    def framework_name() -> str:
        return "SamplePlugin"

    @staticmethod
    def framework_version() -> str:
        return "1.0"


class SampleBuilder(PluginBuilder):
    """
    Sample concrete builder implementation for testing.
    """

    def build(self, *args, **kwargs) -> list[Plugin]:
        return [SamplePlugin()]

    def destroy(self) -> None:
        ...


def test_plugin_setup():
    plugin = SamplePlugin()
    plugin.setup()
    # add assertions here


def test_plugin_execute():
    plugin = SamplePlugin()
    output = plugin.execute()
    assert isinstance(output, dict)
    assert "result" in output


def test_plugin_render_nefertem():
    plugin = SamplePlugin()
    input_obj = Mock()
    output_obj = plugin.render_nefertem(input_obj)
    assert input_obj == output_obj


def test_plugin_render_artifact():
    plugin = SamplePlugin()
    input_obj = Mock()
    output_obj = plugin.render_artifact(input_obj)
    assert input_obj == output_obj


def test_plugin_get_library():
    plugin = SamplePlugin()
    library_info = plugin.get_framework()
    assert isinstance(library_info, dict)
    assert "libraryName" in library_info
    assert "libraryVersion" in library_info


def test_builder_build():
    store_mock = Mock(name="store")
    builder = SampleBuilder([store_mock], {})
    plugins = builder.build()
    assert isinstance(plugins, list)
    assert len(plugins) == 1
    assert isinstance(plugins[0], Plugin)


def test_builder_destroy():
    builder = SampleBuilder([], {})
    builder.destroy()
    # add assertions here


def test_plugin_get_render_tuple():
    obj_mock = Mock()
    filename_mock = Mock()
    render_tuple = Plugin._get_render_tuple(obj_mock, filename_mock)
    assert isinstance(render_tuple, tuple)
    assert len(render_tuple) == 2
    assert render_tuple[0] == obj_mock
    assert render_tuple[1] == filename_mock


def test_plugin_get_framework_name():
    name = SamplePlugin.framework_name()
    assert isinstance(name, str)
    assert name == "SamplePlugin"


def test_plugin_get_framework_version():
    version = SamplePlugin.framework_version()
    assert isinstance(version, str)
    assert version == "1.0"


@pytest.fixture
def resource():
    return DataResource(name="test", path="s3://test", store="test")


def test_builder_get_resource_deepcopyresource(resource):
    copied_resource = SampleBuilder._get_resource_deepcopy(resource)
    assert isinstance(copied_resource, DataResource)
    assert copied_resource == resource


def test_builder_get_resource_store(resource):
    store_mock = Mock()
    store_mock.name = "test"
    builder = SampleBuilder([store_mock], {})
    fetched_store = builder._get_resource_store(resource)
    assert fetched_store == store_mock

    builder = SampleBuilder([], {})
    with pytest.raises(StoreError):
        builder._get_resource_store(resource)
