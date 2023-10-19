"""
Nefertem base report module.
"""
from dataclasses import dataclass

from nefertem.metadata.metadata import Metadata


@dataclass
class NefertemBaseReport(Metadata):
    """
    Nefertem base report class.

    Attributes
    ----------
    lib_name : str
        Execution library name.
    lib_version : str
        Execution library version.
    duration : float
        Time required by the execution process.
    """

    lib_name: str
    lib_version: str
    duration: float
