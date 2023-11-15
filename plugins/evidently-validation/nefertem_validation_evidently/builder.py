from __future__ import annotations

from nefertem_validation.plugins.builder import ValidationPluginBuilder
from nefertem_validation_evidently.constraint import ConstraintEvidently
from nefertem_validation_evidently.plugin import ValidationPluginEvidently

from nefertem.readers.builder import build_reader
from nefertem.resources.data_resource import DataResource
from nefertem.utils.commons import FILE_READER


class ValidationBuilderEvidently(ValidationPluginBuilder):
    """
    Evidently validation plugin builder.
    """

    def build(
        self,
        resources: list[DataResource],
        constraints: list[dict],
        error_report: str,
    ) -> list[ValidationPluginEvidently]:
        """
        Build a plugin for every constraint.
        """
        f_constraints = self._validate_constraints(constraints)
        plugins = []
        for constraint in f_constraints:
            for resource in resources:
                if resource.name == constraint.resource:
                    store = self.stores[resource.store]
                    data_reader = build_reader(FILE_READER, store)
                    curr_resource = resource
                elif resource.name == constraint.reference_resource:
                    store = self.stores[resource.store]
                    ref_data_reader = build_reader(FILE_READER, store)
                    ref_resource = resource

            if curr_resource is not None:
                plugin = ValidationPluginEvidently()
                plugin.setup(
                    data_reader,
                    resource,
                    constraint,
                    error_report,
                    self.exec_args,
                    ref_data_reader,
                    ref_resource,
                )
                plugins.append(plugin)

        return plugins

    @staticmethod
    def _validate_constraints(constraints: list[dict]) -> list[ConstraintEvidently]:
        """
        Build constraints.
        """
        return [ConstraintEvidently(**c) for c in constraints if c["type"] == "evidently"]
