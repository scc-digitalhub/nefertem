from __future__ import annotations

import typing

from nefertem_validation.plugins.builder import ValidationPluginBuilder
from nefertem_validation_sqlalchemy.constraint import ConstraintSqlAlchemy
from nefertem_validation_sqlalchemy.plugin import ValidationPluginSqlAlchemy

from nefertem.readers.builder import build_reader
from nefertem.utils.commons import PANDAS_DATAFRAME_SQL_READER
from nefertem.utils.utils import flatten_list
from operations.nefertem_validation.nefertem_validation.utils import ValidationError

if typing.TYPE_CHECKING:
    from nefertem.resources.data_resource import DataResource


class ValidationBuilderSqlAlchemy(ValidationPluginBuilder):
    """
    SqlAlchemy validation plugin builder.
    """

    def build(
        self,
        resources: list[DataResource],
        constraints: list[dict],
        error_report: str,
    ) -> list[ValidationPluginSqlAlchemy]:
        """
        Build a plugin for every resource and every constraint.
        """
        f_constraint = self._validate_constraints(constraints)
        f_resources = self._filter_resources(resources, f_constraint)
        g_constraint = self._check_unique_store(f_constraint, f_resources)

        plugins = []
        for i in g_constraint:
            data_reader = build_reader(PANDAS_DATAFRAME_SQL_READER, i["store"])
            plugin = ValidationPluginSqlAlchemy()
            plugin.setup(data_reader, i["constraint"], error_report, self.exec_args)
            plugins.append(plugin)

        return plugins

    @staticmethod
    def _validate_constraints(constraints: list[dict]) -> list[ConstraintSqlAlchemy]:
        """
        Build constraints.

        Parameters
        ----------
        constraints : list[dict]
            Constraints to validate.

        Returns
        -------
        list[ConstraintSqlAlchemy]
            List of constraints.
        """
        return [ConstraintSqlAlchemy(**c) for c in constraints if c.get("type") == "sqlalchemy"]

    def _filter_resources(
        self,
        resources: list[DataResource],
        constraints: list[ConstraintSqlAlchemy],
    ) -> list[DataResource]:
        """
        Filter resources used by validator.
        """
        res_names = flatten_list([const.resources for const in constraints])
        res_to_validate = [res for res in resources if res.name in res_names]
        return [res for res in res_to_validate if res.store in self.stores]

    def _check_unique_store(
        self,
        constraints: list[ConstraintSqlAlchemy],
        resources: list[DataResource],
    ) -> list:
        """
        Check univocity of resources location and return connection string for db access.
        Basically, all resources must be in the same database.
        """

        grouped = {}
        for const in constraints:
            # Check if all resources described by constraint are in the same database
            res_stores = [res.store for res in resources if res.name in const.resources]
            store_num = len(set(res_stores))
            if store_num > 1:
                raise ValidationError(f"Resources for constraint '{const.name}' are not in the same database.")
            if store_num == 0:
                raise ValidationError(f"No resources for constraint '{const.name}' are in a configured store.")

            # Pack constraint and store together
            grouped.append({"constraint": const, "store": self.stores[res_stores][0]})

        return grouped