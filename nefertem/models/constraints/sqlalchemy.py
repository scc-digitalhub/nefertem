from pydantic import Field

from nefertem.models.constraints.sql import ConstraintBaseSQL
from nefertem.utils.commons import LIBRARY_SQLALCHEMY


class ConstraintSqlAlchemy(ConstraintBaseSQL):
    """
    SqlAlchemy constraint.
    """

    type: str = Field(LIBRARY_SQLALCHEMY, Literal=True)
    """Constraint type ("sqlalchemy")."""
