from typing import Any

from pydantic import Field
from typing_extensions import Literal

from nefertem.plugins.validation.base import Constraint


class ConstraintSqlAlchemy(Constraint):
    """
    SqlAlchemy constraint.
    """

    type: str = Field("sqlalchemy", Literal=True)
    """Constraint type ("sqlalchemy")."""

    query: str
    """SQL query to execute over resources."""

    expect: Literal["empty", "non-empty", "exact", "range", "minimum", "maximum"]
    """SQL constraint type to check."""

    value: Any | None = None
    """Value of the constraint."""

    check: Literal["value", "rows"] = "rows"
    """Modality of constraint checking (On rows or single value)."""
