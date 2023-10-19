from pydantic import Field

from nefertem.models.constraints.sql import ConstraintBaseSQL
from nefertem.utils.commons import LIBRARY_DUCKDB


class ConstraintDuckDB(ConstraintBaseSQL):
    """
    DuckDB constraint.
    """

    type: str = Field(LIBRARY_DUCKDB, Literal=True)
    """Constraint type ("duckdb")."""
