from dataclasses import dataclass

from nefertem.metadata.reports.base import NefertemBaseReport


@dataclass
class NefertemSchema(NefertemBaseReport):
    """
    Succint version of an inferred schema produced by some inference library.

    Attributes
    ----------
    fields : list
        A list of fields.

    """

    fields: list
