from typing import Any

from pydantic import Field
from typing_extensions import Literal

from nefertem.plugins.validation.base import Constraint


class ConstraintDuckDB(Constraint):
    """
    DuckDB constraint.
    """

    type: str = Field("duckdb", Literal=True)
    """Constraint type ("duckdb")."""

    query: str
    """SQL query to execute over resources."""

    expect: Literal["empty", "non-empty", "exact", "range", "minimum", "maximum"]
    """SQL constraint type to check."""

    value: Any | None = None
    """Value of the constraint."""

    check: Literal["value", "rows"] = "rows"
    """Modality of constraint checking (On rows or single value)."""
