"""
Frictionless inference plugin builder module.
"""
from __future__ import annotations

import typing

from nefertem.plugins.inference.base import InferencePluginBuilder
from nefertem.plugins.inference.frictionless.plugin import InferencePluginFrictionless
from nefertem.utils.commons import BASE_FILE_READER

if typing.TYPE_CHECKING:
    from nefertem.resources.data_resource import DataResource


class InferenceBuilderFrictionless(InferencePluginBuilder):
    """
    Inference plugin builder.
    """

    def build(self, resources: list[DataResource]) -> list[InferencePluginFrictionless]:
        """
        Build a plugin.
        """
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = self._get_data_reader(BASE_FILE_READER, store)
            plugin = InferencePluginFrictionless()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins
