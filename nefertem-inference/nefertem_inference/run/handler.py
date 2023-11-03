from __future__ import annotations

import typing

from nefertem.plugins.factory import builder_factory
from nefertem.run.handler import RunHandler
from nefertem.stores.builder import get_all_input_stores

if typing.TYPE_CHECKING:
    from nefertem.resources.data_resource import DataResource
    from nefertem.run.config import RunConfig


class RunHandlerInference(RunHandler):
    def __init__(self, config: RunConfig) -> None:
        """
        Constructor.
        """
        super().__init__(config)

    #############################
    # Execution methods
    #############################

    def infer(self, resources: list[DataResource]) -> None:
        """
        Wrapper for plugins infer methods.
        """
        builders = builder_factory(self._config, get_all_input_stores())
        plugins = self._create_plugins(builders, resources)
        self._scheduler(plugins, self._config.parallel, self._config.num_worker)
