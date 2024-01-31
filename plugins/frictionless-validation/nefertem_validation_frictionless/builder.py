from __future__ import annotations

import typing
from copy import deepcopy

from nefertem_core.readers.builder import build_reader
from nefertem_core.utils.commons import FILE_READER
from nefertem_validation.plugins.builder import ValidationPluginBuilder
from nefertem_validation_frictionless.constraints import ConstraintFrictionless, ConstraintFullFrictionless
from nefertem_validation_frictionless.plugin import ValidationPluginFrictionless

if typing.TYPE_CHECKING:
    from nefertem_core.resources.data_resource import DataResource


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
        f_constraints = self._validate_constraints(constraints)
        plugins = []
        for res in resources:
            resource = deepcopy(res)
            for const in f_constraints:
                if resource.name in const.resources:
                    store = self.stores[resource.store]
                    data_reader = build_reader(FILE_READER, store)
                    plugin = ValidationPluginFrictionless()
                    plugin.setup(data_reader, resource, const, error_report, self.exec_args)
                    plugins.append(plugin)
        return plugins

    @staticmethod
    def _validate_constraints(
        constraints: list[dict],
    ) -> list[ConstraintFrictionless | ConstraintFullFrictionless]:
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
