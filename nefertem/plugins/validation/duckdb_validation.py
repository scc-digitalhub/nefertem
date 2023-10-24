"""
DuckDB implementation of validation plugin.
"""
from __future__ import annotations

import shutil
import typing
from copy import deepcopy
from pathlib import Path
from typing import Any

import duckdb

from nefertem.metadata.reports.report import NefertemReport
from nefertem.plugins.utils.plugin_utils import ValidationReport, exec_decorator
from nefertem.plugins.utils.sql_checks import evaluate_validity
from nefertem.plugins.validation.validation_plugin import Validation, ValidationPluginBuilder
from nefertem.utils.commons import (
    CONSTRAINT_SQL_CHECK_ROWS,
    CONSTRAINT_SQL_CHECK_VALUE,
    DEFAULT_DIRECTORY,
    LIBRARY_DUCKDB,
    PANDAS_DATAFRAME_DUCKDB_READER,
    PANDAS_DATAFRAME_FILE_READER,
    POLARS_DATAFRAME_FILE_READER,
)
from nefertem.utils.utils import build_uuid, flatten_list, listify

if typing.TYPE_CHECKING:
    from nefertem.models.constraints.base import Constraint
    from nefertem.models.constraints.duckdb import ConstraintDuckDB
    from nefertem.plugins.utils.plugin_utils import Result
    from nefertem.readers.base.native import NativeReader
    from nefertem.resources.data_resource import DataResource
    from nefertem.stores.artifact.objects.base import ArtifactStore


class ValidationPluginDuckDB(Validation):
    """
    DuckDB implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.db = None
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: NativeReader,
        db: str,
        constraint: ConstraintDuckDB,
        error_report: str,
        exec_args: dict,
    ) -> None:
        """
        Set plugin resource.
        """
        self.data_reader = data_reader
        self.db = db
        self.constraint = constraint
        self.error_report = error_report
        self.exec_args = exec_args

    @exec_decorator
    def validate(self) -> dict:
        """
        Validate a Data Resource.
        """
        try:
            data = self.data_reader.fetch_data(self.db, self.constraint.query)
            value = self._filter_result(data)
            valid, errors = evaluate_validity(value, self.constraint.expect, self.constraint.value)
            result = self._shorten_data(data)
            return ValidationReport(result, valid, errors)
        except Exception as ex:
            raise ex

    def _filter_result(self, data: Any) -> Any:
        """
        Return value or size of DataFrame for SQL checks.
        """
        if self.constraint.check == CONSTRAINT_SQL_CHECK_VALUE:
            return self.data_reader.return_first_value(data)
        elif self.constraint.check == CONSTRAINT_SQL_CHECK_ROWS:
            return self.data_reader.return_length(data)

    def _shorten_data(self, data: Any) -> Any:
        """
        Return a short version of data.
        """
        return self.data_reader.return_head(data)

    @exec_decorator
    def render_nefertem(self, result: Result) -> NefertemReport:
        """
        Return a NefertemReport.
        """
        exec_err = result.errors
        duration = result.duration
        constraint = self.constraint.dict()
        errors = {}

        if exec_err is None:
            valid = result.artifact.valid
            if not valid:
                total_count = 1
                errors_list = [self._render_error_type("sql-check-error")]
                parsed_error_list = self._parse_error_report(errors_list)
                errors = self._get_errors(total_count, parsed_error_list)
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            valid = False

        return NefertemReport(
            self.get_lib_name(),
            self.get_lib_version(),
            duration,
            constraint,
            valid,
            errors,
        )

    @exec_decorator
    def render_artifact(self, result: Result) -> list[tuple]:
        """
        Return a rendered report ready to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = result.artifact.to_dict()
        filename = self._fn_report.format(f"{LIBRARY_DUCKDB}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return duckdb.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return duckdb.__version__


class ValidationBuilderDuckDB(ValidationPluginBuilder):
    """
    DuckDB validation plugin builder.
    """

    def build(
        self,
        resources: list[DataResource],
        constraints: list[Constraint],
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
    def _filter_constraints(
        constraints: list[Constraint],
    ) -> list[ConstraintDuckDB]:
        """
        Filter out ConstraintDuckDB.
        """
        return [const for const in constraints if const.type == LIBRARY_DUCKDB]

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

    def _get_reader(self, store: ArtifactStore) -> NativeReader:
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
