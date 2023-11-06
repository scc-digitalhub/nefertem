"""
Dummy implementation of profiling plugin.
"""
from nefertem_profiling.plugins._dummy.plugin import ProfilingPluginDummy
from nefertem_profiling.plugins.builder import ProfilingPluginBuilder


class ProfilingBuilderDummy(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(self, *args) -> list[ProfilingPluginDummy]:
        """
        Build a plugin.
        """
        return [ProfilingPluginDummy()]

    @staticmethod
    def _filter_metrics(*args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """
