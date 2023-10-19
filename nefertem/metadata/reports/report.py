from dataclasses import dataclass

from nefertem.metadata.reports.base import NefertemBaseReport


@dataclass
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

    constraint: dict
    valid: bool
    errors: dict
