"""
EnvLog module.
"""
from __future__ import annotations

import os
import platform

from psutil import virtual_memory


class Env:
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

    def __init__(self) -> None:
        """
        Constructor.
        """
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
        mem = virtual_memory().total / (1024.0**3)
        return f"{mem:.1f} GB"

    def to_dict(self) -> dict:
        return self.__dict__
