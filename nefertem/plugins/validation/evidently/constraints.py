"""
Evidently implementation of validation plugin.
"""
from pydantic import BaseModel, Field

from nefertem.plugins.validation.base import Constraint


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

    type: str = Field("evidently", Literal=True)
    """Constraint type ("Evidently")."""

    resource: str
    """Resource to validate."""

    reference_resource: str | None = None
    """Resource to use as reference."""

    tests: list[Element]
    """Evidently tests."""
