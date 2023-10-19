from typing import Any, Optional

from pydantic import root_validator
from typing_extensions import Literal

from nefertem.models.constraints.base import Constraint
from nefertem.utils.commons import (
    CONSTRAINT_SQL_CHECK_ROWS,
    CONSTRAINT_SQL_CHECK_VALUE,
    CONSTRAINT_SQL_EMPTY,
    CONSTRAINT_SQL_EXACT,
    CONSTRAINT_SQL_MAXIMUM,
    CONSTRAINT_SQL_MINIMUM,
    CONSTRAINT_SQL_NON_EMPTY,
    CONSTRAINT_SQL_RANGE,
)


class ConstraintBaseSQL(Constraint):
    query: str
    """SQL query to execute over resources."""

    expect: Literal[
        CONSTRAINT_SQL_EMPTY,
        CONSTRAINT_SQL_NON_EMPTY,
        CONSTRAINT_SQL_EXACT,
        CONSTRAINT_SQL_RANGE,
        CONSTRAINT_SQL_MINIMUM,
        CONSTRAINT_SQL_MAXIMUM,
    ]
    """SQL constraint type to check."""

    value: Optional[Any] = None
    """Value of the constraint."""

    check: Literal[
        CONSTRAINT_SQL_CHECK_VALUE,
        CONSTRAINT_SQL_CHECK_ROWS,
    ] = CONSTRAINT_SQL_CHECK_ROWS
    """Modality of constraint checking (On rows or single value)."""

    @root_validator(skip_on_failure=True)
    def check_for_emptiness(cls, values):
        """
        Check that evaluation of emptiness is performed
        only at rows level.
        """
        check = values.get("check")
        expect = values.get("expect")
        if expect in (CONSTRAINT_SQL_EMPTY, CONSTRAINT_SQL_NON_EMPTY) and check != CONSTRAINT_SQL_CHECK_ROWS:
            raise ValueError("Invalid, check emptiness only on 'rows'.")
        return values
