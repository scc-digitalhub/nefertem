from __future__ import annotations

import importlib

import evidently
from evidently.test_suite import TestSuite
from nefertem_validation.metadata.report import NefertemReport
from nefertem_validation.plugins.plugin import ValidationPlugin
from nefertem_validation.plugins.utils import get_errors, parse_error_report
from nefertem_validation_evidently.constraint import ConstraintEvidently

from nefertem.plugins.utils import RenderTuple, Result, exec_decorator
from nefertem.readers.objects.file import FileReader
from nefertem.resources.data_resource import DataResource


class ValidationPluginEvidently(ValidationPlugin):
    """
    Evidently implementation of validation plugin.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()
        self.resource = None
        self.reference_resource = None
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: FileReader,
        resource: DataResource,
        constraint: ConstraintEvidently,
        error_report: str,
        exec_args: dict,
        reference_data_reader: FileReader = None,
        reference_resource: DataResource = None,
    ) -> None:
        self.data_reader = data_reader
        self.reference_data_reader = reference_data_reader
        self.resource = resource
        self.reference_resource = reference_resource
        self.constraint = constraint
        self.error_report = error_report
        self.exec_args = exec_args

    @exec_decorator
    def validate(self) -> dict:
        """
        Validate a Data Resource.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        reference_data = (
            None
            if self.reference_resource is None
            else self.reference_data_reader.fetch_data(self.reference_resource.path)
        )
        tests = self._rebuild_constraints()
        test_run = TestSuite(tests=tests)
        test_run.run(current_data=data, reference_data=reference_data)
        return test_run

    def _rebuild_constraints(self) -> list[any]:
        """
        Rebuild constraints converting to Evidently test.
        """
        res = []
        for test in self.constraint.tests:
            check = test.type
            module_name, class_name = check.rsplit(".", 1)
            _class = getattr(importlib.import_module(module_name), class_name)
            if test.values:
                res.append(_class(**test.values))
            else:
                res.append(_class())
        return res

    @exec_decorator
    def render_nefertem(self, result: Result) -> RenderTuple:
        """
        Return a NefertemReport.
        """
        exec_err = result.errors
        duration = result.duration
        constraint = self.constraint.dict()
        errors = None

        if exec_err is None:
            artifact = result.artifact.as_dict()
            valid = artifact["summary"]["all_passed"]
            if not valid:
                errors_list = [i for i in artifact["tests"] if i["status"] != "SUCCESS"]
                parsed_error_list = parse_error_report(errors_list, self.error_report)
                errors = get_errors(len(errors_list), parsed_error_list)
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self.id}")
            valid = False

        return NefertemReport(
            self.framework_name(),
            self.framework_version(),
            duration,
            constraint,
            valid,
            errors,
        )

    @exec_decorator
    def render_artifact(self, result: Result) -> list[RenderTuple]:
        """
        Return an Evidently report to be persisted as artifact.
        """
        if result.artifact is None:
            obj = {"errors": result.errors}
        else:
            obj = result.artifact.as_dict()
        filename = self._fn_report.format("evidently.json")
        return [RenderTuple(obj, filename)]

    @staticmethod
    def framework_name() -> str:
        """
        Get library name.

        Returns
        -------
        str
            Library name.
        """
        return evidently.__name__

    @staticmethod
    def framework_version() -> str:
        """
        Get library version.

        Returns
        -------
        str
            Library version.
        """
        return evidently.__version__
