"""
Base abstract Run Plugin module.
"""
from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod

from nefertem_core.plugins.utils import RenderTuple
from nefertem_core.utils.logger import LOGGER
from nefertem_core.utils.utils import build_uuid

if typing.TYPE_CHECKING:
    from nefertem_core.plugins.utils import Result


class Plugin(metaclass=ABCMeta):
    """
    Base plugin abstract class.
    """

    def __init__(self) -> None:
        self.id = build_uuid()
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
    def render_nefertem(self, obj: Result) -> RenderTuple:
        """
        Return a NefertemProfile object ready to be persisted as metadata.
        """

    @abstractmethod
    def render_artifact(self, obj: Result) -> list[RenderTuple]:
        """
        Return an object ready to be persisted as artifact.
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
