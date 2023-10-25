"""
Dummy implementation of validation plugin.
"""
from __future__ import annotations

import typing
from collections import namedtuple

from nefertem.metadata.reports.report import NefertemReport
from nefertem.plugins.utils.plugin_utils import exec_decorator
from nefertem.plugins.validation.base import Validation, ValidationPluginBuilder
from nefertem.utils.commons import DUMMY

if typing.TYPE_CHECKING:
    from nefertem.plugins.utils.plugin_utils import Result

DummyConstraint = namedtuple("DummyConstraint", ["name", "resources"], defaults=["", [""]])


class ValidationPluginDummy(Validation):
    """
    Dummy implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.constraint = DummyConstraint()

    def setup(self, *args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """

    @exec_decorator
    def validate(self) -> dict:
        """
        Do nothing.
        """
        return {}

    @exec_decorator
    def render_nefertem(self, *args) -> NefertemReport:
        """
        Return a NefertemReport.
        """
        return NefertemReport(self.get_lib_name(), self.get_lib_version(), 0.0, {}, True, {})

    @exec_decorator
    def render_artifact(self, result: Result) -> list[tuple]:
        """
        Return a dummy report to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_report.format(f"{DUMMY}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return DUMMY

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return DUMMY


class ValidationBuilderDummy(ValidationPluginBuilder):
    """
    Dummy validation plugin builder.
    """

    def build(self, *args) -> list[ValidationPluginDummy]:
        """
        Build a plugin.
        """
        return [ValidationPluginDummy()]

    @staticmethod
    def _filter_constraints(*args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """

    def destroy(self, *args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """
