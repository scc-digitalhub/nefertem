"""
Base abstract Run Plugin module.
"""
from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any

from nefertem.plugins.utils import RenderTuple
from nefertem.utils.logger import LOGGER
from nefertem.utils.utils import build_uuid

if typing.TYPE_CHECKING:
    from nefertem.plugins.utils import Result


class Plugin(metaclass=ABCMeta):
    """
    Base plugin abstract class.
    """

    def __init__(self) -> None:
        self._id = build_uuid()
        self.lib_name = self.get_lib_name()
        self.lib_version = self.get_lib_version()
        self.logger = LOGGER
        self.data_reader = None
        self.exec_args = None
        self.exec_sequential = True
        self.exec_multiprocess = False
        self.exec_multithread = False
        self.exec_distributed = False

    @abstractmethod
    def setup(self, *args, **kwargs) -> None:
        """
        Configure a plugin.
        """

    @abstractmethod
    def execute(self) -> dict:
        """
        Execute main plugin operation.
        """

    @abstractmethod
    def render_nefertem(self, obj: Result) -> Result:
        """
        Produce nefertem output.
        """

    @abstractmethod
    def render_artifact(self, obj: Result) -> Result:
        """
        Render an artifact to be persisted.
        """

    @staticmethod
    def get_render_tuple(obj: Any, filename: str) -> RenderTuple:
        """
        Return a RenderTuple.
        """
        return RenderTuple(obj, filename)

    @staticmethod
    @abstractmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """

    @staticmethod
    @abstractmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """

    def get_library(self) -> dict:
        """
        Get library info.
        """
        return {
            "libraryName": self.get_lib_name(),
            "libraryVersion": self.get_lib_version(),
        }
