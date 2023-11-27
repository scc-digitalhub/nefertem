"""
Run handler module.
"""
from __future__ import annotations

import concurrent.futures
import typing
from typing import Any

from nefertem.plugins.factory import builder_factory
from nefertem.plugins.utils import ResultType
from nefertem.stores.builder import get_all_input_stores
from nefertem.utils.utils import flatten_list, listify

if typing.TYPE_CHECKING:
    from nefertem.plugins.builder import PluginBuilder
    from nefertem.plugins.plugin import Plugin
    from nefertem.run.config import RunConfig


class RunHandler:
    """
    Run handler.

    This class create a layer of abstraction between the Run and its plugins.

    Attributes
    ----------
    _config : RunConfig
        Run configuration.
    _tmp_dir : str
        Temporary directory to store artifacts.
    _registry : dict
        Resul registry.
    """

    def __init__(self, config: RunConfig) -> None:
        """
        Constructor.
        """
        self._config = config
        self._registry = {}

    #############################
    # Execution methods
    #############################

    def run(self, *args, **kwargs) -> None:
        """
        Run plugins.

        Args and kwargs are passed to plugins, so if you use a plugin that require
        resources, you can pass them as arguments or keyword arguments.

        E.g.:
        ```
        run_handler.run(resources)
        run_handler.run(resources=resources)
        ```

        Parameters
        ----------
        args : Any
            Arguments.
        kwargs : Any
            Keyword arguments.
        """
        builders = self._get_builder()
        plugins = self._create_plugins(builders, *args, **kwargs)
        self._scheduler(plugins)

    def _get_builder(self) -> list[PluginBuilder]:
        """
        Return a list of builders.

        Returns
        -------
        list[PluginBuilder]
            List of builders.
        """
        return builder_factory(self._config, get_all_input_stores())

    @staticmethod
    def _create_plugins(builders: PluginBuilder, *args, **kwargs) -> list[Plugin]:
        """
        Return a list of plugins.
        """
        return flatten_list([builder.build(*args, **kwargs) for builder in builders])

    def _scheduler(self, plugins: list[Plugin]) -> None:
        """
        Schedule execution to avoid multiprocessing issues.
        """
        multiprocess = []
        multithreading = []
        sequential = []

        for plugin in plugins:
            # Concurrent execution
            if self._config.parallel:
                if plugin.exec_multiprocess:
                    multiprocess.append(plugin)
                elif plugin.exec_multithread:
                    multithreading.append(plugin)
            # Sequential execution
            else:
                sequential.append(plugin)

        self._sequential_execute(sequential)
        self._pool_execute_multithread(multithreading)
        self._pool_execute_multiprocess(multiprocess)

    def _sequential_execute(self, plugins: list[Plugin]) -> None:
        """
        Execute operations in sequence.
        """
        for plugin in plugins:
            data = self._execute(plugin)
            self._register_results(data)

    def _pool_execute_multiprocess(self, plugins: list[Plugin]) -> None:
        """
        Instantiate a concurrent.future.ProcessPoolExecutor pool to execute operations in
        multiprocessing.
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=self._config.num_worker) as pool:
            for data in pool.map(self._execute, plugins):
                self._register_results(data)

    def _pool_execute_multithread(self, plugins: list[Plugin]) -> None:
        """
        Instantiate a concurrent.future.ThreadPoolExecutor pool to execute operations in
        multithreading.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._config.num_worker) as pool:
            for data in pool.map(self._execute, plugins):
                self._register_results(data)

    @staticmethod
    def _execute(plugin: Plugin) -> dict:
        """
        Wrap plugins main execution method. The handler create builders to build plugins.
        Once the plugin are built, the handler execute the main plugin operation, produce
        a nefertem report, render the execution artifact ready to be stored and save some
        library infos.
        """
        return plugin.execute()

    #############################
    # Registry methods
    #############################

    def _register_results(self, result: dict) -> None:
        """
        Register results.

        Parameters
        ----------
        result : dict
            Result dictionary.

        Returns
        -------
        None
        """
        for key, value in result.items():
            if key not in self._registry:
                self._registry[key] = []
            if isinstance(value, list):
                self._registry[key].extend(value)
            else:
                self._registry[key].append(value)

    def get_item(self, item_type: str) -> list[Any]:
        """
        Get item from registry.

        Parameters
        ----------
        item_type : str
            Item type.

        Returns
        -------
        list[Any]
            List of object.
        """
        objects = self._registry.get(item_type, [])

        # Get artifacts and nefertem report
        if item_type in [ResultType.FRAMEWORK.value, ResultType.NEFERTEM.value]:
            return [obj.artifact for obj in objects]

        # Get rendered
        return listify(flatten_list([obj.artifact for obj in objects]))

    def get_libraries(self) -> list[dict]:
        """
        Get libraries used by operations.

        Returns
        -------
        list[dict]
            List of libraries.
        """
        libs = []
        for i in self._registry.get(ResultType.LIBRARY.value, []):
            if dict(**i) not in libs:
                libs.append(i)
        return libs
