"""
Validation plugin abstract class module.
"""
from abc import abstractmethod
from typing import Any

from nefertem_validation.plugins.utils import RenderTuple

from nefertem.plugins.plugin import Plugin
from nefertem.plugins.utils import ResultType


class ValidationPlugin(Plugin):
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

        Returns
        -------
        dict
            Results of execution.
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

    @staticmethod
    def _get_render_tuple(obj: Any, filename: str) -> RenderTuple:
        """
        Return a RenderTuple.

        Parameters
        ----------
        obj : Any
            Object rendered for persistence.
        filename : str
            Filename.

        Returns
        -------
        RenderTuple
            RenderTuple object.
        """
        return RenderTuple(obj, filename)

    @staticmethod
    def _render_error_type(code: str) -> dict:
        """
        Return standard errors record format.

        Parameters
        ----------
        code : str
            Error code.

        Returns
        -------
        dict
            Error type record.
        """
        return {"type": code}

    def _parse_error_report(self, error_list: list) -> list:
        """
        Return a list of record according to user parameter.

        Parameters
        ----------
        error_list : list
            List of errors.

        Returns
        -------
        list
            List of errors.
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

        Parameters
        ----------
        count : int
            Number of errors.
        records : list
            List of errors.

        Returns
        -------
        dict
            Error structure.
        """
        if records is None:
            records = []
        return {"count": count, "records": records}
