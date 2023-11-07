"""
Base abstract Run Plugin module.
"""
from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod

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
        self.lib_name = self.framework_name()
        self.lib_version = self.framework_version()
        self.logger = LOGGER

        self.data_reader = None
        self.exec_args = None

        self.exec_sequential = True
        self.exec_multiprocess = False
        self.exec_multithread = False

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
    @abstractmethod
    def framework_name() -> str:
        """
        Get framework name.
        """

    @staticmethod
    @abstractmethod
    def framework_version() -> str:
        """
        Get framework version.
        """

    def get_framework(self) -> dict:
        """
        Get framework info.
        """
        return {
            "framework_name": self.framework_name(),
            "framework_version": self.framework_version(),
        }
