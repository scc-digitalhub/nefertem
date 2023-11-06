"""
Dummy implementation of validation plugin.
"""
from nefertem_validation.plugins._dummy.plugin import ValidationPluginDummy
from nefertem_validation.plugins.builder import ValidationPluginBuilder


class ValidationBuilderDummy(ValidationPluginBuilder):
    """
    Dummy validation plugin builder.
    """

    def build(self, *args) -> list[ValidationPluginDummy]:
        """
        Build a plugin.
        """
        return [ValidationPluginDummy()]

    @staticmethod
    def _filter_constraints(*args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """

    def destroy(self, *args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """
