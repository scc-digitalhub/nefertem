"""
Frictionless implementation of validation plugin.
"""
from typing import Any

from pydantic import Field

from nefertem.plugins.validation.base import Constraint


class ConstraintFrictionless(Constraint):
    """
    Frictionless constraint.
    """

    type: str = Field("frictionless", Literal=True)
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

    type: str = Field("frictionless_full", Literal=True)
    """Constraint type ("frictionless_schema")."""

    tableSchema: dict
    """Table schema to validate a resource."""
