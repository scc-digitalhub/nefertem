"""
Run handler module.
"""
from __future__ import annotations

import concurrent.futures
import typing
from typing import Any

from nefertem.plugins.factory import builder_factory
from nefertem.readers.utils import build_reader
from nefertem.utils.commons import (
    BASE_FILE_READER,
    INFER,
    PROFILE,
    RESULT_LIBRARY,
    RESULT_NEFERTEM,
    RESULT_RENDERED,
    RESULT_WRAPPED,
    VALIDATE,
)
from nefertem.utils.exceptions import RunError
from nefertem.utils.file_utils import get_absolute_path
from nefertem.utils.uri_utils import get_name_from_uri
from nefertem.utils.utils import flatten_list, listify

if typing.TYPE_CHECKING:
    from nefertem.client.store_handler import StoreHandler
    from nefertem.metadata.reports.profile import NefertemProfile
    from nefertem.metadata.reports.report import NefertemReport
    from nefertem.metadata.reports.schema import NefertemSchema
    from nefertem.plugins.base import Plugin, PluginBuilder
    from nefertem.plugins.profiling.base import Metric
    from nefertem.plugins.validation.base import Constraint
    from nefertem.resources.data_resource import DataResource
    from nefertem.run.run_config import RunConfig


class RunHandlerRegistry:
    """
    Generic registry object to store objects
    based on operations.
    """

    def __init__(self) -> None:
        self.registry = {}
        self._setup()

    def _setup(self):
        """
        Setup the run handler registry.
        """
        for ops in [INFER, VALIDATE, PROFILE]:
            self.registry[ops] = {}
            for res in [
                RESULT_WRAPPED,
                RESULT_NEFERTEM,
                RESULT_RENDERED,
                RESULT_LIBRARY,
            ]:
                self.registry[ops][res] = []

    def register(self, ops: str, _type: str, _object: Any) -> None:
        """
        Register an object on the registry based on
        operation and result typology.
        """
        if isinstance(_object, list):
            self.registry[ops][_type].extend(_object)
        else:
            self.registry[ops][_type].append(_object)

    def get_object(self, ops: str, _type: str) -> list:
        """
        Return object from registry.
        """
        try:
            return self.registry[ops][_type]
        except KeyError:
            return []


class RunHandler:
    """
    Run handler.

    This class create a layer of abstraction between the Run
    and its plugins.

    """

    def __init__(self, config: RunConfig, store_handler: StoreHandler) -> None:
        self._config = config
        self._store_handler = store_handler
        self._registry = RunHandlerRegistry()

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
            self._store_handler.get_all_art_stores(),
        )
        plugins = self._create_plugins(builders, resources)
        self._scheduler(plugins, INFER, parallel, num_worker)
        self._destroy_builders(builders)

    def validate(
        self,
        resources: list[DataResource],
        constraints: list[Constraint],
        error_report: str,
        parallel: bool = False,
        num_worker: int = 10,
    ) -> None:
        """
        Wrapper for plugins validate methods.
        """
        self._parse_report_arg(error_report)
        constraints = listify(constraints)
        builders = builder_factory(
            self._config.validation,
            VALIDATE,
            self._store_handler.get_all_art_stores(),
        )
        plugins = self._create_plugins(builders, resources, constraints, error_report)
        self._scheduler(plugins, VALIDATE, parallel, num_worker)
        self._destroy_builders(builders)

    @staticmethod
    def _parse_report_arg(error_report: str) -> None:
        """
        Check error_report argument and raise
        if differs from options.
        """
        if error_report not in ("count", "partial", "full"):
            raise RunError("Available options for error_report are 'count', 'partial', 'full'.")

    def profile(
        self,
        resources: list[DataResource],
        metrics: list[Metric] | None = None,
        parallel: bool = False,
        num_worker: int = 10,
    ) -> None:
        """
        Wrapper for plugins profile methods.
        """
        metrics = listify(metrics)
        builders = builder_factory(
            self._config.profiling,
            PROFILE,
            self._store_handler.get_all_art_stores(),
        )
        plugins = self._create_plugins(builders, resources, metrics)
        self._scheduler(plugins, PROFILE, parallel, num_worker)
        self._destroy_builders(builders)

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
        distributed = []
        sequential = []
        for plugin in plugins:
            if plugin.exec_multiprocess and parallel:
                multiprocess.append(plugin)
            elif plugin.exec_multithread and parallel:
                multithreading.append(plugin)
            elif plugin.exec_distributed and parallel:
                distributed.append(plugin)
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

    def _register_results(
        self,
        operation: str,
        result: dict,
    ) -> None:
        """
        Register results.
        """
        for key, value in result.items():
            self._registry.register(operation, key, value)

    @staticmethod
    def _destroy_builders(builders: list[PluginBuilder]) -> None:
        """
        Destroy builders.
        """
        for builder in builders:
            builder.destroy()

    def get_item(self, operation: str, _type: str) -> list[Any]:
        """
        Get item from registry.
        """
        return self._registry.get_object(operation, _type)

    def get_artifact_schema(self) -> list[Any]:
        """
        Get a list of schemas produced by inference libraries.
        """
        return [obj.artifact for obj in self.get_item(INFER, RESULT_WRAPPED)]

    def get_artifact_report(self) -> list[Any]:
        """
        Get a list of reports produced by validation libraries.
        """
        return [obj.artifact for obj in self.get_item(VALIDATE, RESULT_WRAPPED)]

    def get_artifact_profile(self) -> list[Any]:
        """
        Get a list of profiles produced by profiling libraries.
        """
        return [obj.artifact for obj in self.get_item(PROFILE, RESULT_WRAPPED)]

    def get_nefertem_schema(self) -> list[NefertemSchema]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.artifact for obj in self.get_item(INFER, RESULT_NEFERTEM)]

    def get_nefertem_report(self) -> list[NefertemReport]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.artifact for obj in self.get_item(VALIDATE, RESULT_NEFERTEM)]

    def get_nefertem_profile(self) -> list[NefertemProfile]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.artifact for obj in self.get_item(PROFILE, RESULT_NEFERTEM)]

    def get_rendered_schema(self) -> list[Any]:
        """
        Get a list of schemas ready to be persisted.
        """
        return listify(flatten_list([obj.artifact for obj in self.get_item(INFER, RESULT_RENDERED)]))

    def get_rendered_report(self) -> list[Any]:
        """
        Get a list of reports ready to be persisted.
        """
        return listify(flatten_list([obj.artifact for obj in self.get_item(VALIDATE, RESULT_RENDERED)]))

    def get_rendered_profile(self) -> list[Any]:
        """
        Get a list of profiles ready to be persisted.
        """
        return listify(flatten_list([obj.artifact for obj in self.get_item(PROFILE, RESULT_RENDERED)]))

    def get_libraries(self) -> list[dict]:
        """
        Return libraries used by run.
        """
        libs = {}
        for ops in [INFER, PROFILE, VALIDATE]:
            libs[ops] = []
            for i in self.get_item(ops, RESULT_LIBRARY):
                if dict(**i) not in libs[ops]:
                    libs[ops].append(i)
        return libs

    def log_metadata(self, src: dict, dst: str, src_type: str, overwrite: bool) -> None:
        """
        Method to log metadata in the metadata store.
        """
        store = self._store_handler.get_md_store()
        store.log_metadata(src, dst, src_type, overwrite)

    def persist_artifact(self, src: Any, dst: str, src_name: str, metadata: dict) -> None:
        """
        Method to persist artifacts in the default artifact store.
        """
        store = self._store_handler.get_def_store()
        store.persist_artifact(src, dst, src_name, metadata)

    def persist_data(self, resources: list[DataResource], dst: str) -> None:
        """
        Persist input data as artifact.
        """
        for res in resources:
            store = self._store_handler.get_art_store(res.store)
            data_reader = build_reader(BASE_FILE_READER, store)
            for path in listify(res.path):
                tmp_pth = data_reader.fetch_data(path)
                tmp_pth = get_absolute_path(tmp_pth)
                filename = get_name_from_uri(tmp_pth)
                self.persist_artifact(tmp_pth, dst, filename, {})

    def clean_all(self) -> None:
        """
        Clean up.
        """
        self._store_handler.clean_all()
