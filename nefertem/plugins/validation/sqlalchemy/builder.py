from copy import deepcopy

from nefertem.plugins.validation.base import Constraint, ValidationPluginBuilder
from nefertem.plugins.validation.sqlalchemy.constraints import ConstraintSqlAlchemy
from nefertem.plugins.validation.sqlalchemy.plugin import ValidationPluginSqlAlchemy
from nefertem.resources.data_resource import DataResource
from nefertem.utils.commons import PANDAS_DATAFRAME_SQL_READER
from nefertem.utils.exceptions import ValidationError
from nefertem.utils.utils import flatten_list


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
