from __future__ import annotations

import typing

import frictionless
from frictionless import Report, Resource, Schema
from frictionless.exception import FrictionlessException
from nefertem_core.plugins.utils import RenderTuple, Result, exec_decorator
from nefertem_validation.metadata.report import NefertemReport
from nefertem_validation.plugins.plugin import ValidationPlugin
from nefertem_validation.plugins.utils import get_errors, parse_error_report, render_error_type

if typing.TYPE_CHECKING:
    from nefertem_core.readers.objects.file import FileReader
    from nefertem_core.resources.data_resource import DataResource
    from nefertem_validation_frictionless.constraints import ConstraintFrictionless, ConstraintFullFrictionless


class ValidationPluginFrictionless(ValidationPlugin):
    """
    Frictionless implementation of validation plugin.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
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
        Setup plugin.

        Parameters
        ----------
        data_reader : FileReader
            Data reader.
        resource : DataResource
            Data resource.
        constraint : ConstraintFrictionless | ConstraintFullFrictionless
            Constraint to validate resource.
        error_report : str
            Error report modality.
        exec_args : dict
            Execution arguments for Resource.validate method.
        """
        self.data_reader = data_reader
        self.resource = resource
        self.constraint = constraint
        self.error_report = error_report
        self.exec_args = exec_args

    @exec_decorator
    def validate(self) -> Report:
        """
        Get frictionless validation report.

        Returns
        -------
        Report
            Validation report.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        schema = self._rebuild_constraints(str(data))
        res = Resource(path=str(data), schema=schema).validate(**self.exec_args)
        return Report.from_descriptor(res.to_dict())

    def _rebuild_constraints(self, data_path: str) -> Schema:
        """
        Rebuild constraints. Add constraints to a simplified schema or
        return the full table schema.

        Parameters
        ----------
        data_path : str
            Data path.

        Returns
        -------
        Schema
            Schema with constraints.
        """
        # Return the full table schema
        if self.constraint.type != "frictionless":
            return Schema(self.constraint.table_schema)

        # Otherwise, add constraints to a simplified schema

        # Get constraint parameters
        field_name = self.constraint.field
        field_type = self.constraint.field_type
        value = self.constraint.value
        const_type = self.constraint.constraint
        weight = self.constraint.weight

        # Get inferred schema from data
        schema = self._get_schema(data_path)

        # Reconstruction logic
        for field in schema["fields"]:
            if field["name"] == field_name:
                field["error"] = {"weight": weight}
                if const_type == "type":
                    field["type"] = field_type
                elif const_type == "format":
                    field["type"] = field_type
                    field["format"] = value
                else:
                    field["type"] = field_type
                    field["constraints"] = {const_type: value}
                break
        return Schema(schema)

    @staticmethod
    def _get_schema(data_path: str) -> dict:
        """
        Infer simple schema of a resource if not present.

        Parameters
        ----------
        data_path : str
            Data path.

        Returns
        -------
        dict
            Schema.
        """
        try:
            schema = Schema.describe(path=data_path).to_dict()
            if not schema:
                return {"fields": []}
            return {"fields": [{"name": field["name"], "type": "any"} for field in schema["fields"]]}
        except FrictionlessException as fex:
            raise fex

    @exec_decorator
    def render_nefertem(self, result: Result) -> RenderTuple:
        """
        Return a NefertemReport ready to be persisted as metadata.

        Parameters
        ----------
        result : Result
            Execution result.

        Returns
        -------
        RenderTuple
            Rendered object.
        """
        exec_err = result.errors
        duration = result.duration
        constraint = self.constraint.dict()
        errors = None

        if exec_err is None:
            valid = result.artifact.to_dict().get("valid")
            if not valid:
                errors_list = [render_error_type(err[0]) for err in result.artifact.flatten(spec=["code"])]
                total_count = len(errors_list)
                parsed_error_list = parse_error_report(errors_list, self.error_report)
                errors = get_errors(total_count, parsed_error_list)

        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self.id}")
            valid = False

        obj = NefertemReport(
            **self.get_framework(),
            duration=duration,
            constraint=constraint,
            valid=valid,
            errors=errors,
        )
        filename = f"nefertem_report_{self.id}.json"
        return RenderTuple(obj, filename)

    @exec_decorator
    def render_artifact(self, result: Result) -> list[RenderTuple]:
        """
        Return a rendered report ready to be persisted as artifact.

        Parameters
        ----------
        result : Result
            Execution result.

        Returns
        -------
        list[RenderTuple]
            Rendered object.
        """
        if result.artifact is None:
            obj = {"errors": result.errors}
        else:
            obj = result.artifact.to_dict()
        filename = f"frictionless_report_{self.id}.json"
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
        return frictionless.__name__

    @staticmethod
    def framework_version() -> str:
        """
        Get library version.

        Returns
        -------
        str
            Library version.
        """
        return frictionless.__version__
