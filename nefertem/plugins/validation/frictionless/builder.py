from __future__ import annotations

import typing

from nefertem.plugins.validation.base import ValidationPluginBuilder
from nefertem.plugins.validation.frictionless.constraints import ConstraintFrictionless, ConstraintFullFrictionless
from nefertem.plugins.validation.frictionless.plugin import ValidationPluginFrictionless
from nefertem.utils.commons import BASE_FILE_READER

if typing.TYPE_CHECKING:
    from nefertem.resources.data_resource import DataResource


class ValidationBuilderFrictionless(ValidationPluginBuilder):
    """
    Validation plugin builder.
    """

    def build(
        self,
        resources: list[DataResource],
        constraints: list[dict],
        error_report: str,
    ) -> list[ValidationPluginFrictionless]:
        """
        Build a plugin for every resource and every constraint.
        """
        f_constraints = self._filter_constraints(constraints)
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            for const in f_constraints:
                if resource.name in const.resources:
                    store = self._get_resource_store(resource)
                    data_reader = self._get_data_reader(BASE_FILE_READER, store)
                    plugin = ValidationPluginFrictionless()
                    plugin.setup(data_reader, resource, const, error_report, self.exec_args)
                    plugins.append(plugin)

        return plugins

    @staticmethod
    def _filter_constraints(constraints: list[dict]) -> list[ConstraintFrictionless | ConstraintFullFrictionless]:
        """
        Build constraints.
        """
        const = []
        for c in constraints:
            if c.get("type") == "frictionless":
                const.append(ConstraintFrictionless(**c))
            elif c.get("type") == "frictionless_full":
                const.append(ConstraintFullFrictionless(**c))
        return const

    def destroy(self) -> None:
        """
        Destroy builder.
        """
