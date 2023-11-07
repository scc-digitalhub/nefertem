from nefertem.metadata.report import NefertemBaseReport


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
        lib_name: str,
        lib_version: str,
        duration: float,
        fields: list,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(lib_name, lib_version, duration)
        self.fields = fields
