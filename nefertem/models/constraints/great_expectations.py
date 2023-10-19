from pydantic import Field

from nefertem.models.constraints.base import Constraint
from nefertem.utils.commons import LIBRARY_GREAT_EXPECTATIONS


class ConstraintGreatExpectations(Constraint):
    """
    Great Expectation constraint.
    """

    type: str = Field(LIBRARY_GREAT_EXPECTATIONS, Literal=True)
    """Constraint type ("great_expectations")."""

    expectation: str
    """Name of the expectation to apply to data."""

    expectation_args: dict
    """Arguments for the exepectation."""
