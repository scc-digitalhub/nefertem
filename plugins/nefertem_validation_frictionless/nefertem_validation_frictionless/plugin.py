from __future__ import annotations

import typing

import frictionless
from frictionless import Report, Resource, Schema
from frictionless.exception import FrictionlessException
from nefertem_validation.metadata.report import NefertemReport
from nefertem_validation.plugins.plugin import ValidationPlugin

from nefertem.plugins.utils import Result, exec_decorator

if typing.TYPE_CHECKING:
    from nefertem_validation_frictionless.constraints import ConstraintFrictionless, ConstraintFullFrictionless

    from nefertem.readers.file.file import FileReader
    from nefertem.resources.data_resource import DataResource


class ValidationPluginFrictionless(ValidationPlugin):
    """
    Frictionless implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.schema = None
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: FileReader,
        resource: DataResource,
        constraint: ConstraintFrictionless | ConstraintFullFrictionless,
        error_report: str,
        exec_args: dict,
    ) -> None:
        """
        Set plugin resource.
        """
        self.data_reader = data_reader
        self.resource = resource
        self.constraint = constraint
        self.error_report = error_report
        self.exec_args = exec_args

    @exec_decorator
    def validate(self) -> Report:
        """
        Validate a Data Resource.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        schema = self._rebuild_constraints(data)
        res = Resource(path=data, schema=schema).validate(**self.exec_args)
        return Report.from_descriptor(res.to_dict())

    def _rebuild_constraints(self, data_path: str) -> Schema:
        """
        Rebuild constraints.
        """
        if self.constraint.type == "frictionless":
            field_name = self.constraint.field
            field_type = self.constraint.fieldType
            val = self.constraint.value
            con_type = self.constraint.constraint
            weight = self.constraint.weight

            schema = self._get_schema(data_path)

            for field in schema["fields"]:
                if field["name"] == field_name:
                    field["error"] = {"weight": weight}
                    if con_type == "type":
                        field["type"] = field_type
                    elif con_type == "format":
                        field["type"] = field_type
                        field["format"] = val
                    else:
                        field["type"] = field_type
                        field["constraints"] = {con_type: val}
                    break
            return Schema(schema)

        # Otherwise return the full table schema
        return Schema(self.constraint.table_schema)

    @staticmethod
    def _get_schema(data_path: str) -> dict:
        """
        Infer simple schema of a resource if not present.
        """
        try:
            schema = Schema.describe(path=data_path).to_dict()
            if not schema:
                return {"fields": []}
            return {"fields": [{"name": field["name"], "type": "any"} for field in schema["fields"]]}
        except FrictionlessException as fex:
            raise fex

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
            valid = result.artifact.to_dict().get("valid")
            if not valid:
                errors_list = [self._render_error_type(err[0]) for err in result.artifact.flatten(spec=["code"])]
                total_count = len(errors_list)
                parsed_error_list = self._parse_error_report(errors_list)
                errors = self._get_errors(total_count, parsed_error_list)

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
        Return a rendered report ready to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = result.artifact.to_dict()

        filename = self._fn_report.format("frictionless.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return frictionless.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return frictionless.__version__
