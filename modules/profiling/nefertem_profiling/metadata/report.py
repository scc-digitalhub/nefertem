from __future__ import annotations

from nefertem_core.metadata.report import NefertemBaseReport


class NefertemProfile(NefertemBaseReport):
    """
    Succint version of a profile produced by some profiling library.

    Attributes
    ----------
    stats : dict
        Descriptors of data stats.
    fields : dict
        Descriptors of data fields.
    """

    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        duration: float,
        stats: dict,
        fields: dict,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(framework_name, framework_version, duration)
        self.stats = stats
        self.fields = fields
