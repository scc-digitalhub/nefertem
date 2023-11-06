"""
Evidently implementation of validation plugin.
"""
from nefertem_validation.plugins.constraint import Constraint
from pydantic import BaseModel


class Element(BaseModel):
    """
    Evidently single test
    """

    type: str
    """Evidently test/metric type (fully qualified class name)."""
    values: dict | None = None
    """Custom parameters for the test/metric."""


class ConstraintEvidently(Constraint):
    """
    Evidently constraint.
    """

    resource: str
    """Resource to validate."""

    reference_resource: str | None = None
    """Resource to use as reference."""

    tests: list[Element]
    """Evidently tests."""
