import importlib

import evidently
from evidently.test_suite import TestSuite

from nefertem.metadata.reports.report import NefertemReport
from nefertem.plugins.utils import Result, exec_decorator
from nefertem.plugins.validation.base import Validation
from nefertem.plugins.validation.evidently.constraints import ConstraintEvidently
from nefertem.readers.base.file import FileReader
from nefertem.resources.data_resource import DataResource


class ValidationPluginEvidently(Validation):
    """
    Evidently implementation of validation plugin.
    """

    def __init__(self) -> None:
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
    def render_nefertem(self, result: Result) -> NefertemReport:
        """
        Return a NefertemReport.
        """
        exec_err = result.errors
        duration = result.duration
        constraint = self.constraint.dict()
        errors = self._get_errors()

        if exec_err is None:
            artifact = result.artifact.as_dict()
            valid = artifact["summary"]["all_passed"]
            if not valid:
                errors_list = list(filter(lambda t: t["status"] != "SUCCESS", artifact["tests"]))
                parsed_error_list = self._parse_error_report(errors_list)
                errors = self._get_errors(len(errors_list), parsed_error_list)
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            valid = False

        return NefertemReport(
            self.get_lib_name(),
            self.get_lib_version(),
            duration,
            constraint,
            valid,
            errors,
        )

    @exec_decorator
    def render_artifact(self, result: Result) -> list[tuple]:
        """
        Return an Evidently report to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = result.artifact.as_dict()
        filename = self._fn_report.format("evidently.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return evidently.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return evidently.__version__