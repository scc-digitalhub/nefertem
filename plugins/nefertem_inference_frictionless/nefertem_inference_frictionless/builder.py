"""
Frictionless inference plugin builder module.
"""
from __future__ import annotations

import typing
from copy import deepcopy

from nefertem_inference.plugins.builder import InferencePluginBuilder
from nefertem_inference_frictionless.plugin import InferencePluginFrictionless

from nefertem.readers.builder import build_reader
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
            resource = deepcopy(res)
            store = self.stores[resource.store]
            data_reader = build_reader(BASE_FILE_READER, store)
            plugin = InferencePluginFrictionless()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins
