"""
Frictionless implementation of validation plugin.
"""
from __future__ import annotations

from typing import Any

from nefertem_validation.plugins.constraint import Constraint


class ConstraintFrictionless(Constraint):
    """
    Frictionless constraint.
    """

    field: str
    """Field to validate."""

    field_type: str
    """Datatype of the field to validate."""

    constraint: str
    """Frictionless constraint typology."""

    value: Any
    """Value of the constraint."""


class ConstraintFullFrictionless(Constraint):
    """
    Frictionless full schema constraint.
    """

    table_schema: dict
    """Table schema to validate a resource."""
