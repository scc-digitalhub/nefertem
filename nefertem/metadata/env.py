"""
EnvLog module.
"""
import os
import platform

from psutil import virtual_memory

from nefertem.metadata.base import Metadata


class EnvLog(Metadata):
    """
    Basic log structure for execution enviroment.

    Attributes
    ----------
    platform : str
        Execution platform.
    python_version : str
        Python version.
    cpu_model : str
        CPU model.
    cpu_core : int
        Number of CPU cores.
    ram : str
        RAM memory in GB.
    """

    def __init__(self, run_id: str, experiment_name: str, nefertem_version: str) -> None:
        """
        Constructor.
        """
        super().__init__(run_id, experiment_name, nefertem_version)
        self.platform = platform.platform()
        self.python_version = platform.python_version()
        self.cpu_model = platform.processor()
        self.cpu_core = os.cpu_count()
        self.ram = self.round_ram()

    @staticmethod
    def round_ram() -> str:
        """
        Return rounded GB ram memory.

        Returns
        -------
        str
            Rounded GB ram memory.
        """
        mem = virtual_memory().total
        return str(round(mem / (1024.0**3))) + " GB"

    def to_dict(self) -> dict:
        return self.__dict__
