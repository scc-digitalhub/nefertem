from __future__ import annotations

import shutil
import typing
from copy import deepcopy
from pathlib import Path
from typing import Any

import duckdb

from nefertem.plugins.validation.base import Constraint, ValidationPluginBuilder
from nefertem.plugins.validation.duckdb.constraints import ConstraintDuckDB
from nefertem.plugins.validation.duckdb.plugin import ValidationPluginDuckDB
from nefertem.utils.commons import (
    DEFAULT_DIRECTORY,
    PANDAS_DATAFRAME_DUCKDB_READER,
    PANDAS_DATAFRAME_FILE_READER,
    POLARS_DATAFRAME_FILE_READER,
)
from nefertem.utils.utils import build_uuid, flatten_list, listify

if typing.TYPE_CHECKING:
    from nefertem.readers.file.native import NativeReader
    from nefertem.resources.data_resource import DataResource
    from nefertem.stores.input.objects.base import InputStore


class ValidationBuilderDuckDB(ValidationPluginBuilder):
    """
    DuckDB validation plugin builder.
    """

    def build(
        self,
        resources: list[DataResource],
        constraints: list[dict],
        error_report: str,
    ) -> list[ValidationPluginDuckDB]:
        """
        Build a plugin for every resource and every constraint.
        """
        self._setup_connection()
        f_constraint = self._filter_constraints(constraints)
        f_resources = self._filter_resources(resources, f_constraint)
        for res in f_resources:
            self._register_resources(res)
        self._tear_down_connection()

        plugins = []
        for const in f_constraint:
            data_reader = self._get_data_reader(PANDAS_DATAFRAME_DUCKDB_READER, None)
            plugin = ValidationPluginDuckDB()
            plugin.setup(data_reader, str(self.tmp_db), const, error_report, self.exec_args)
            plugins.append(plugin)

        return plugins

    def _setup_connection(self) -> None:
        """
        Setup db connection.
        """
        self.tmp_db = Path(DEFAULT_DIRECTORY, build_uuid(), "tmp.duckdb")
        self.tmp_db.parent.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(database=str(self.tmp_db), read_only=False)

    @staticmethod
    def _filter_constraints(constraints: list[dict]) -> list[ConstraintDuckDB]:
        """
        Build constraints.
        """
        const = []
        for c in constraints:
            if c.get("type") == "duckdb":
                const.append(ConstraintDuckDB(**c))
        return const

    @staticmethod
    def _filter_resources(resources: list[DataResource], constraints: list[Constraint]) -> list[DataResource]:
        """
        Filter resources used by validator.
        """
        res_names = set(flatten_list([deepcopy(const.resources) for const in constraints]))
        return [res for res in resources if res.name in res_names]

    def _register_resources(self, resource: DataResource) -> None:
        """
        Register resource in db.
        """
        store = self._get_resource_store(resource)
        data_reader = self._get_reader(store)
        df = self._get_data(data_reader, listify(resource.path))  # noqa pylint: disable=no-member
        self.con.execute(f"CREATE TABLE IF NOT EXISTS {resource.name} AS SELECT * FROM df;")

    def _get_reader(self, store: InputStore) -> NativeReader:
        """
        Get reader. Preference goes to polars, otherwise, use pandas.
        """
        try:
            return self._get_data_reader(POLARS_DATAFRAME_FILE_READER, store)
        except KeyError:
            self.logger.info("Polars not installed, using pandas.")
            return self._get_data_reader(PANDAS_DATAFRAME_FILE_READER, store)

    @staticmethod
    def _get_data(data_reader: NativeReader, paths: list) -> Any:
        """
        Fetch data from paths.
        """
        dfs = [data_reader.fetch_data(pth) for pth in paths]
        return data_reader.concat_data(dfs)

    def _tear_down_connection(self) -> None:
        """
        Close connection.
        """
        self.con.close()

    def destroy(self) -> None:
        """
        Destory db.
        """
        shutil.rmtree(self.tmp_db.parent, ignore_errors=True)
