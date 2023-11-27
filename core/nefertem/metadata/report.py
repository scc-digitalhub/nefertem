"""
Nefertem base report module.
"""
from __future__ import annotations


class NefertemBaseReport:
    """
    Nefertem base report class.

    Attributes
    ----------
    framework_name : str
        Execution library name.
    framework_version : str
        Execution library version.
    duration : float
        Time required by the execution process.
    """

    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        duration: float,
    ) -> None:
        """
        Constructor.
        """
        super().__init__()
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.duration = duration

    def to_dict(self) -> dict:
        return self.__dict__

    def __repr__(self) -> str:
        return f"{self.to_dict()}"
