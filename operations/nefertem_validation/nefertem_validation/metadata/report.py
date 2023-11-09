from nefertem.metadata.report import NefertemBaseReport


class NefertemReport(NefertemBaseReport):
    """
    Succint version of a report produced by some validation library.

    Attributes
    ----------
    constraint : dict
        Constraint validated.
    valid : bool
        Validation outcome.
    errors : list
        List of errors found by validation process.

    """

    def __init__(
        self,
        lib_name: str,
        lib_version: str,
        duration: float,
        constraint: dict,
        valid: bool,
        errors: list,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(lib_name, lib_version, duration)
        self.constraint = constraint
        self.valid = valid
        self.errors = errors