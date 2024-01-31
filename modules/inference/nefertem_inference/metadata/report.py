from __future__ import annotations

from nefertem_core.metadata.report import NefertemBaseReport


class NefertemSchema(NefertemBaseReport):
    """
    Succint version of an inferred schema produced by some inference library.

    Attributes
    ----------
    fields : list
        A list of fields.

    """

    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        duration: float,
        fields: list,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(framework_name, framework_version, duration)
        self.fields = fields
