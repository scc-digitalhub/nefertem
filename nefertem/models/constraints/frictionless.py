from typing import Any

from pydantic import Field

from nefertem.models.constraints.base import Constraint
from nefertem.utils.commons import CONSTRAINT_FRICTIONLESS_SCHEMA, LIBRARY_FRICTIONLESS


class ConstraintFrictionless(Constraint):
    """
    Frictionless constraint.
    """

    type: str = Field(LIBRARY_FRICTIONLESS, Literal=True)
    """Constraint type ("frictionless")."""

    field: str
    """Field to validate."""

    fieldType: str
    """Datatype of the field to validate."""

    constraint: str
    """Frictionless constraint typology."""

    value: Any
    """Value of the constraint."""


class ConstraintFullFrictionless(Constraint):
    """
    Frictionless full schema constraint.
    """

    type: str = Field(CONSTRAINT_FRICTIONLESS_SCHEMA, Literal=True)
    """Constraint type ("frictionless_schema")."""

    tableSchema: dict
    """Table schema to validate a resource."""
