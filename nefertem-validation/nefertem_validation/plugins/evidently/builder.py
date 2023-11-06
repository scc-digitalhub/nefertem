from nefertem_validation.plugins.builder import ValidationPluginBuilder
from nefertem_validation.plugins.evidently.constraints import ConstraintEvidently
from nefertem_validation.plugins.evidently.plugin import ValidationPluginEvidently

from nefertem.resources.data_resource import DataResource
from nefertem.utils.commons import BASE_FILE_READER


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
        f_constraints = self._filter_constraints(constraints)
        plugins = []
        for constraint in f_constraints:
            data_reader = None
            curr_resource = None
            ref_data_reader = None
            ref_resource = None
            for resource in resources:
                if resource.name == constraint.resource:
                    store = self._get_resource_store(resource)
                    data_reader = self._get_data_reader(BASE_FILE_READER, store)
                    curr_resource = resource
                elif resource.name == constraint.reference_resource:
                    store = self._get_resource_store(resource)
                    ref_data_reader = self._get_data_reader(BASE_FILE_READER, store)
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
    def _filter_constraints(constraints: list[dict]) -> list[ConstraintEvidently]:
        """
        Build constraints.
        """
        const = []
        for c in constraints:
            if c.get("type") == "evidently":
                const.append(ConstraintEvidently(**c))
        return const

    def destroy(self, *args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """
