"""
SQLAlchemy implementation of validation plugin.
"""
from __future__ import annotations

import typing
from copy import deepcopy
from typing import Any

import sqlalchemy
from pydantic import Field
from typing_extensions import Literal

from nefertem.metadata.reports.report import NefertemReport
from nefertem.plugins.utils.plugin_utils import ValidationReport, exec_decorator
from nefertem.plugins.utils.sql_checks import evaluate_validity
from nefertem.plugins.validation.base import Constraint, Validation, ValidationPluginBuilder
from nefertem.utils.commons import PANDAS_DATAFRAME_SQL_READER
from nefertem.utils.exceptions import ValidationError
from nefertem.utils.utils import flatten_list

if typing.TYPE_CHECKING:
    from nefertem.plugins.utils.plugin_utils import Result
    from nefertem.readers.base.native import NativeReader
    from nefertem.resources.data_resource import DataResource


####################
# PLUGIN
####################


class ValidationPluginSqlAlchemy(Validation):
    """
    SQLAlchemy implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: NativeReader,
        constraint: ConstraintSqlAlchemy,
        error_report: str,
        exec_args: dict,
    ) -> None:
        """
        Set plugin resource.
        """
        self.data_reader = data_reader
        self.constraint = constraint
        self.error_report = error_report
        self.exec_args = exec_args

    @exec_decorator
    def validate(self) -> dict:
        """
        Validate a Data Resource.
        """
        try:
            data = self.data_reader.fetch_data(self.constraint.name, self.constraint.query)
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
        if self.constraint.check == "value":
            return self.data_reader.return_first_value(data)
        elif self.constraint.check == "rows":
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
        filename = self._fn_report.format("sqlalchemy.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return sqlalchemy.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return sqlalchemy.__version__


####################
# BUILDER
####################


class ValidationBuilderSqlAlchemy(ValidationPluginBuilder):
    """
    SqlAlchemy validation plugin builder.
    """

    def build(
        self,
        resources: list[DataResource],
        constraints: list[Constraint],
        error_report: str,
    ) -> list[ValidationPluginSqlAlchemy]:
        """
        Build a plugin for every resource and every constraint.
        """
        self._setup()

        f_constraint = self._filter_constraints(constraints)
        f_resources = self._filter_resources(resources, f_constraint)
        grouped_constraints = self._regroup_constraint_resources(f_constraint, f_resources)

        plugins = []
        for pack in grouped_constraints:
            store = pack["store"]
            const = pack["constraint"]
            data_reader = self._get_data_reader(PANDAS_DATAFRAME_SQL_READER, store)
            plugin = ValidationPluginSqlAlchemy()
            plugin.setup(data_reader, const, error_report, self.exec_args)
            plugins.append(plugin)

        return plugins

    def _setup(self) -> None:
        """
        Filter builder store to keep only SQLStores and set 'native' mode for
        reading data to return a connection string to a db.
        """
        self.stores = [store for store in self.stores if store.store_type == "sql"]
        if not self.stores:
            raise ValidationError("There must be at least a SQLStore to use sqlalchemy validator.")

    @staticmethod
    def _filter_constraints(
        constraints: list[Constraint],
    ) -> list[ConstraintSqlAlchemy]:
        """
        Filter out ConstraintSqlAlchemy.
        """
        return [const for const in constraints if const.type == "sqlalchemy"]

    def _filter_resources(self, resources: list[DataResource], constraints: list[Constraint]) -> list[DataResource]:
        """
        Filter resources used by validator.
        """
        res_names = set(flatten_list([deepcopy(const.resources) for const in constraints]))
        res_to_validate = [res for res in resources if res.name in res_names]
        st_names = [store.name for store in self.stores]
        res_in_db = [res for res in res_to_validate if res.store in st_names]
        return res_in_db

    def _regroup_constraint_resources(self, constraints: list[Constraint], resources: list[DataResource]) -> list:
        """
        Check univocity of resources location and return connection
        string for db access. Basically, all resources must be in
        the same database.
        """
        constraint_connection = []

        for const in constraints:
            res_stores = [res.store for res in resources]

            store_num = len(set(res_stores))
            if store_num > 1:
                raise ValidationError(f"Resources for constraint '{const.name}' are not in the same database.")
            if store_num == 0:
                raise ValidationError(f"No resources for constraint '{const.name}' are in a configured store.")

            constraint_connection.append(
                {
                    "constraint": const,
                    "store": [s for s in self.stores if s.name == res_stores[0]][0],
                }
            )

        return constraint_connection

    def destroy(self) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """


####################
# CONSTRAINT
####################


class ConstraintSqlAlchemy(Constraint):
    """
    SqlAlchemy constraint.
    """

    type: str = Field("sqlalchemy", Literal=True)
    """Constraint type ("sqlalchemy")."""

    query: str
    """SQL query to execute over resources."""

    expect: Literal["empty", "non-empty", "exact", "range", "minimum", "maximum"]
    """SQL constraint type to check."""

    value: Any | None = None
    """Value of the constraint."""

    check: Literal["value", "rows"] = "rows"
    """Modality of constraint checking (On rows or single value)."""