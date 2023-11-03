"""
Run handler module.
"""
from __future__ import annotations

import concurrent.futures
import typing
from typing import Any

from nefertem.plugins.factory import builder_factory
from nefertem.stores.builder import get_all_input_stores
from nefertem.utils.commons import (
    INFER,
    PROFILE,
    RESULT_ARTIFACT,
    RESULT_LIBRARY,
    RESULT_NEFERTEM,
    RESULT_RENDERED,
    VALIDATE,
)
from nefertem.utils.exceptions import RunError
from nefertem.utils.utils import flatten_list, listify

if typing.TYPE_CHECKING:
    from nefertem.plugins.base import Plugin, PluginBuilder
    from nefertem.resources.data_resource import DataResource
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
        self._config = config
        self._registry = {}

        self._setup()

    #############################
    # Setup
    #############################

    def _setup(self) -> None:
        """
        Setup registry.

        Returns
        -------
        None
        """
        for ops in [INFER, VALIDATE, PROFILE]:
            self._registry[ops] = {}
            for res in [RESULT_ARTIFACT, RESULT_NEFERTEM, RESULT_RENDERED, RESULT_LIBRARY]:
                self._registry[ops][res] = []

    #############################
    # Run methods
    #############################

    def infer(
        self,
        resources: list[DataResource],
        parallel: bool = False,
        num_worker: int = 10,
    ) -> None:
        """
        Wrapper for plugins infer methods.
        """
        builders = builder_factory(
            self._config.inference,
            INFER,
            get_all_input_stores(),
        )
        plugins = self._create_plugins(builders, resources)
        self._scheduler(plugins, INFER, parallel, num_worker)

    def validate(
        self,
        resources: list[DataResource],
        constraints: list[dict],
        error_report: str,
        parallel: bool = False,
        num_worker: int = 10,
    ) -> None:
        """
        Wrapper for plugins validate methods.
        """
        if error_report not in ("count", "partial", "full"):
            raise RunError("Available options for error_report are 'count', 'partial', 'full'.")
        builders = builder_factory(
            self._config.validation,
            VALIDATE,
            get_all_input_stores(),
        )
        plugins = self._create_plugins(builders, resources, constraints, error_report)
        self._scheduler(plugins, VALIDATE, parallel, num_worker)
        for builder in builders:
            builder.destroy()

    def profile(
        self,
        resources: list[DataResource],
        metrics: list[dict],
        parallel: bool = False,
        num_worker: int = 10,
    ) -> None:
        """
        Wrapper for plugins profile methods.
        """
        builders = builder_factory(
            self._config.profiling,
            PROFILE,
            get_all_input_stores(),
        )
        plugins = self._create_plugins(builders, resources, metrics)
        self._scheduler(plugins, PROFILE, parallel, num_worker)

    #############################
    # Execution methods
    #############################

    @staticmethod
    def _create_plugins(builders: PluginBuilder, *args) -> list[Plugin]:
        """
        Return a list of plugins.
        """
        return flatten_list([builder.build(*args) for builder in builders])

    def _scheduler(self, plugins: list[Plugin], ops: str, parallel: bool, num_worker: int) -> None:
        """
        Schedule execution to avoid multiprocessing issues.
        """
        multiprocess = []
        multithreading = []
        sequential = []
        for plugin in plugins:
            if plugin.exec_multiprocess and parallel:
                multiprocess.append(plugin)
            elif plugin.exec_multithread and parallel:
                multithreading.append(plugin)
            else:
                sequential.append(plugin)

        # Revisite this
        self._sequential_execute(sequential, ops)
        self._pool_execute_multithread(multithreading, ops, num_worker)
        self._pool_execute_multiprocess(multiprocess, ops, num_worker)

    def _sequential_execute(self, plugins: list[Plugin], ops: str) -> None:
        """
        Execute operations in sequence.
        """
        for plugin in plugins:
            data = self._execute(plugin)
            self._register_results(ops, data)

    def _pool_execute_multiprocess(self, plugins: list[Plugin], ops: str, num_worker: int) -> None:
        """
        Instantiate a concurrent.future.ProcessPoolExecutor pool to
        execute operations in multiprocessing.
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_worker) as pool:
            for data in pool.map(self._execute, plugins):
                self._register_results(ops, data)

    def _pool_execute_multithread(self, plugins: list[Plugin], ops: str, num_worker: int) -> None:
        """
        Instantiate a concurrent.future.ThreadPoolExecutor pool to
        execute operations in multithreading.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_worker) as pool:
            for data in pool.map(self._execute, plugins):
                self._register_results(ops, data)

    @staticmethod
    def _execute(plugin: Plugin) -> dict:
        """
        Wrap plugins main execution method. The handler create
        builders to build plugins. Once the plugin are built,
        the handler execute the main plugin operation
        (inference, validation or profiling), produce a nefertem
        report, render the execution artifact ready to be stored
        and save some library infos.
        """
        return plugin.execute()

    #############################
    # Registry methods
    #############################

    def _register_results(self, operation: str, result: dict) -> None:
        """
        Register results.

        Returns
        -------
        None
        """
        for key, value in result.items():
            if isinstance(value, list):
                self._registry[operation][key].extend(value)
            else:
                self._registry[operation][key].append(value)

    def get_item(self, operation: str, item_type: str) -> list[Any]:
        """
        Get item from registry.

        Parameters
        ----------
        ops : str
            Operation.
        item_type : str
            Item type.

        Returns
        -------
        list[Any]
            List of object.
        """
        objects = self._registry.get(operation).get(item_type, [])

        # Get artifacts and nefertem report
        if item_type in [RESULT_ARTIFACT, RESULT_NEFERTEM]:
            return [obj.artifact for obj in objects]

        # Get rendered
        return listify(flatten_list([obj.artifact for obj in objects]))

    def get_libs(self) -> dict:
        """
        Get libraries used by operations.

        Returns
        -------
        dict
            Dictionary of libraries.
        """
        libs = {}
        for ops in [INFER, PROFILE, VALIDATE]:
            libs[ops] = []
            for i in self._registry.get(ops).get(RESULT_LIBRARY, []):
                if dict(**i) not in libs[ops]:
                    libs[ops].append(i)
        return libs
