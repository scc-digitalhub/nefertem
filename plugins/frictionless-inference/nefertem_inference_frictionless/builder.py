"""
Frictionless inference plugin builder module.
"""
from __future__ import annotations

import typing
from copy import deepcopy

from nefertem_core.readers.builder import build_reader
from nefertem_core.utils.commons import FILE_READER
from nefertem_inference.plugins.builder import InferencePluginBuilder
from nefertem_inference_frictionless.plugin import InferencePluginFrictionless

if typing.TYPE_CHECKING:
    from nefertem_core.resources.data_resource import DataResource


class InferenceBuilderFrictionless(InferencePluginBuilder):
    """
    Inference plugin builder.
    """

    def build(self, resources: list[DataResource]) -> list[InferencePluginFrictionless]:
        """
        Build a plugin for each resource.

        Parameters
        ----------
        resources : list[DataResource]
            List of resources.

        Returns
        -------
        list[InferencePluginFrictionless]
            List of plugins.
        """
        plugins = []
        for res in resources:
            # Get data reader for the resource
            data_reader = build_reader(FILE_READER, self.stores[res.store])

            # Build and setup plugin with a copy of the resource to avoid
            # resource modification
            plugin = InferencePluginFrictionless()
            plugin.setup(data_reader, deepcopy(res), self.exec_args)
            plugins.append(plugin)
        return plugins
