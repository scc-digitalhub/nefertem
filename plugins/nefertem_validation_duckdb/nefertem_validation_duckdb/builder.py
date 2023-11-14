from __future__ import annotations

import typing
from copy import deepcopy
from pathlib import Path

import duckdb
from nefertem_validation.plugins.builder import ValidationPluginBuilder
from nefertem_validation_duckdb.constraint import ConstraintDuckDB
from nefertem_validation_duckdb.plugin import ValidationPluginDuckDB

from nefertem.readers import reader_registry
from nefertem.readers.builder import build_reader
from nefertem.utils.utils import build_uuid, flatten_list, listify

if typing.TYPE_CHECKING:
    from nefertem_validation_duckdb.reader import PandasDataFrameDuckDBReader
    from nefertem.stores.input.objects._base import InputStore
    from nefertem.resources.data_resource import DataResource


PANDAS_READER = "pandas_df_duckdb_reader"


class ValidationBuilderDuckDB(ValidationPluginBuilder):
    """
    DuckDB validation plugin builder.
    """

    def __init__(self, stores: list[InputStore], exec_args: dict) -> None:
        """
        Constructor.
        """
        super().__init__(stores, exec_args)

        # Register new reader in the reader registry
        reader_registry.register(PANDAS_READER, "nefertem_validation_duckdb.reader", "PandasDataFrameDuckDBReader")

    def build(
        self,
        resources: list[DataResource],
        constraints: list[dict],
        error_report: str,
    ) -> list[ValidationPluginDuckDB]:
        """
        Build a plugin for every resource and every constraint.

        Parameters
        ----------
        resources : list[DataResource]
            List of resources.
        constraints : list[dict]
            List of constraints.
        error_report : str
            Error report modality.

        Returns
        -------
        list[ValidationPluginDuckDB]
            List of plugins.
        """

        # Create a new db for all validation
        # Use the temporary directory from one store (all stores share the same tmp dir)
        tmp_path = self.stores[resources[0].store].temp_dir
        self._setup_connection(tmp_path)

        # Filter resources and constraints
        f_constraint = self._validate_constraints(constraints)
        f_resources = self._filter_resources(resources, f_constraint)
        for res in f_resources:
            self._register_resources(res)

        # Close connection to db
        self._tear_down_connection()

        plugins = []
        for const in f_constraint:
            # Get data reader for the resource
            data_reader = build_reader(PANDAS_READER, None)

            # Build and setup plugin
            plugin = ValidationPluginDuckDB()
            plugin.setup(data_reader, str(self.tmp_db), const, error_report)
            plugins.append(plugin)
        return plugins

    def _setup_connection(self, tmp_path: str) -> None:
        """
        Create a new db for all validation.

        Parameters
        ----------
        tmp_path : str
            Path to tmp folder.

        Returns
        -------
        None
        """
        # Build a duckdb on temporary path and create a connection
        self.tmp_db = Path(tmp_path, build_uuid(), "tmp.duckdb")
        self.tmp_db.parent.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(database=str(self.tmp_db), read_only=False)

    @staticmethod
    def _validate_constraints(constraints: list[dict]) -> list[ConstraintDuckDB]:
        """
        Build constraints.

        Parameters
        ----------
        constraints : list[dict]
            List of constraints.

        Returns
        -------
        list[ConstraintDuckDB]
            List of constraints.
        """
        return [ConstraintDuckDB(**c) for c in constraints if c["type"] == "duckdb"]

    @staticmethod
    def _filter_resources(resources: list[DataResource], constraints: list[ConstraintDuckDB]) -> list[DataResource]:
        """
        Filter resources used by validator.

        Parameters
        ----------
        resources : list[DataResource]
            List of resources.
        constraints : list[ConstraintDuckDB]
            List of constraints.

        Returns
        -------
        list[DataResource]
            List of resources mentioned in constraints.
        """
        res_names = flatten_list([deepcopy(const.resources) for const in constraints])
        return [res for res in resources if res.name in res_names]

    def _register_resources(self, resource: DataResource) -> None:
        """
        Register resource in duckdb.

        Parameters
        ----------
        resource : DataResource
            Resource to register.

        Returns
        -------
        None
        """
        # Fetch data resource
        data_reader: PandasDataFrameDuckDBReader = build_reader(PANDAS_READER, self.stores[resource.store])

        # Read data and register it in duckdb
        paths = listify(resource.path)
        df = data_reader.fetch_local_data(paths)  # noqa pylint: disable=no-member
        self.con.execute(f"CREATE TABLE IF NOT EXISTS {resource.name} AS SELECT * FROM df;")

    def _tear_down_connection(self) -> None:
        """
        Close connection to duckdb.

        Returns
        -------
        None
        """
        self.con.close()
