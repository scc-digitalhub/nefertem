"""
Validation plugin abstract class module.
"""
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from nefertem_core.plugins.plugin import Plugin
from nefertem_core.plugins.utils import ResultType


class ValidationPlugin(Plugin):
    """
    Run plugin that executes validation over a Resource.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()
        self.constraint = None
        self.error_report = None

    def execute(self) -> dict:
        """
        Method that call specific execution.

        Returns
        -------
        dict
            Results of execution.
        """
        plugin = f"Plugin: {self.framework_name()} {self.id};"
        constraint = f"Constraint: {self.constraint.name};"
        resources = f"Resources: {self.constraint.resources};"
        self.logger.info(f"Execute validation - {plugin} {constraint} {resources}")
        lib_result = self.validate()
        self.logger.info(f"Render report - {plugin}")
        nt_result = self.render_nefertem(lib_result)
        self.logger.info(f"Render artifact - {plugin}")
        render_result = self.render_artifact(lib_result)
        return {
            ResultType.FRAMEWORK.value: lib_result,
            ResultType.NEFERTEM.value: nt_result,
            ResultType.RENDERED.value: render_result,
            ResultType.LIBRARY.value: self.get_framework(),
        }

    @abstractmethod
    def validate(self) -> Any:
        """
        Validate a resource.
        """
