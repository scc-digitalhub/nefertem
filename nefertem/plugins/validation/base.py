"""
Validation plugin abstract class module.
"""
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any

from pydantic import BaseModel, Field

from nefertem.plugins.base import Plugin, PluginBuilder
from nefertem.utils.commons import RESULT_LIBRARY, RESULT_NEFERTEM, RESULT_RENDERED, RESULT_WRAPPED
from nefertem.utils.utils import build_uuid

####################
# PLUGIN
####################


class Validation(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes validation over a Resource.
    """

    _fn_report = "report_{}"

    def __init__(self) -> None:
        super().__init__()
        self.constraint = None
        self.error_report = None

    def execute(self) -> dict:
        """
        Method that call specific execution.
        """
        plugin = f"Plugin: {self.lib_name} {self._id};"
        constraint = f"Constraint: {self.constraint.name};"
        resources = f"Resources: {self.constraint.resources};"
        self.logger.info(f"Execute validation - {plugin} {constraint} {resources}")
        lib_result = self.validate()
        self.logger.info(f"Render report - {plugin}")
        nt_result = self.render_nefertem(lib_result)
        self.logger.info(f"Render artifact - {plugin}")
        render_result = self.render_artifact(lib_result)
        return {
            RESULT_WRAPPED: lib_result,
            RESULT_NEFERTEM: nt_result,
            RESULT_RENDERED: render_result,
            RESULT_LIBRARY: self.get_library(),
        }

    @abstractmethod
    def validate(self) -> Any:
        """
        Validate a resource.
        """

    @staticmethod
    def _render_error_type(code: str) -> dict:
        """
        Return standard errors record format.
        """
        return {"type": code}

    def _parse_error_report(self, error_list: list) -> list:
        """
        Return a list of record according to user parameter.
        """
        if self.error_report == "count":
            return []
        if self.error_report == "partial":
            if len(error_list) <= 100:
                return error_list
            return error_list[:100]
        if self.error_report == "full":
            return error_list

    @staticmethod
    def _get_errors(count: int = 0, records: list = None) -> dict:
        """
        Return a common error structure.
        """
        if records is None:
            records = []
        return {"count": count, "records": records}


####################
# BUILDER
####################


class ValidationPluginBuilder(PluginBuilder):
    """
    Validation plugin builder.
    """

    @staticmethod
    @abstractmethod
    def _filter_constraints(constraints: list[Constraint]) -> list[Constraint]:
        """
        Filter constraints by library.
        """


####################
# CONSTRAINT
####################


class Constraint(BaseModel):
    """
    Base model for constraint.
    """

    id: str = Field(default_factory=build_uuid)
    """UUID of constraint."""

    name: str
    """Constraint id."""

    title: str
    """Human readable name for the constraint."""

    resources: list[str]
    """List of resources affected by the constraint."""

    weight: int
    """Criticity of an eventual error encountered in the validation for the constraint."""
