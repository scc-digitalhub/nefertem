"""
Nefertem base report module.
"""


class NefertemBaseReport:
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

    def __init__(
        self,
        lib_name: str,
        lib_version: str,
        duration: float,
    ) -> None:
        """
        Constructor.
        """
        super().__init__()
        self.lib_name = lib_name
        self.lib_version = lib_version
        self.duration = duration

    def to_dict(self) -> dict:
        return self.__dict__

    def __repr__(self) -> str:
        return f"{self.to_dict()}"
