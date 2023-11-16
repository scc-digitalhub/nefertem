from __future__ import annotations

from typing import Any

from nefertem_validation.plugins.constraint import Constraint
from typing_extensions import Literal


class ConstraintSqlAlchemy(Constraint):
    """
    SqlAlchemy constraint.
    """

    query: str
    """SQL query to execute over resources."""

    expect: Literal["empty", "non-empty", "exact", "range", "minimum", "maximum"]
    """SQL constraint type to check."""

    value: Any = None
    """Value of the constraint."""

    check: Literal["value", "rows"] = "rows"
    """Modality of constraint checking (On rows or single value)."""
