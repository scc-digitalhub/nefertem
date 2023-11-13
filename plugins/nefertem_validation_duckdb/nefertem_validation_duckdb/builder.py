from __future__ import annotations

import typing
from copy import deepcopy
from pathlib import Path
from typing import Any

import duckdb
from nefertem_validation.plugins.builder import ValidationPluginBuilder
from nefertem_validation.plugins.constraint import Constraint
from nefertem_validation_duckdb.constraint import ConstraintDuckDB
from nefertem_validation_duckdb.plugin import ValidationPluginDuckDB

from nefertem.readers import reader_registry
from nefertem.readers.builder import build_reader
from nefertem.utils.utils import build_uuid, flatten_list, listify

if typing.TYPE_CHECKING:
    from nefertem.readers.objects.native import NativeReader
    from nefertem.resources.data_resource import DataResource


PANDAS_READER = "pandas_df_duckdb_reader"


class ValidationBuilderDuckDB(ValidationPluginBuilder):
    """
    DuckDB validation plugin builder.
    """

    def __init__(self, stores: dict[str, str], exec_args: dict) -> None:
        super().__init__(stores, exec_args)
        reader_registry.register(PANDAS_READER, "nefertem_validation_duckdb.reader", "PandasDataFrameDuckDBReader")

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
        f_constraint = self._validate_constraints(constraints)
        f_resources = self._filter_resources(resources, f_constraint)
        for res in f_resources:
            self._register_resources(res)
        self._tear_down_connection()

        plugins = []
        for const in f_constraint:
            data_reader = build_reader(PANDAS_READER, None)
            plugin = ValidationPluginDuckDB()
            plugin.setup(data_reader, str(self.tmp_db), const, error_report, self.exec_args)
            plugins.append(plugin)
        return plugins

    def _setup_connection(self) -> None:
        """
        Setup db connection.
        """
        tmp_path = self.stores[0].temp_dir
        self.tmp_db = Path(tmp_path, build_uuid(), "tmp.duckdb")
        self.tmp_db.parent.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(database=str(self.tmp_db), read_only=False)

    @staticmethod
    def _validate_constraints(constraints: list[dict]) -> list[ConstraintDuckDB]:
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
        store = self.stores[resource.store]
        data_reader = build_reader(PANDAS_READER, store)
        df = self._get_data(data_reader, listify(resource.path))  # noqa pylint: disable=no-member
        self.con.execute(f"CREATE TABLE IF NOT EXISTS {resource.name} AS SELECT * FROM df;")

    @staticmethod
    def _get_data(data_reader: NativeReader, paths: list) -> Any:
        """
        Fetch data from paths.
        """
        dfs = [data_reader.fetch_local_data(pth) for pth in paths]
        return data_reader.concat_data(dfs)

    def _tear_down_connection(self) -> None:
        """
        Close connection.
        """
        self.con.close()
