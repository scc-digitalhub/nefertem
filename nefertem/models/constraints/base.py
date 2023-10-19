from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field


class Constraint(BaseModel):
    """
    Base model for constraint.
    """

    id: str = Field(default_factory=uuid4)
    """UUID of constraint."""

    name: str
    """Constraint id."""

    title: str
    """Human readable name for the constraint."""

    resources: List[str]
    """List of resources affected by the constraint."""

    weight: int
    """Criticity of an eventual error encountered in the validation for the constraint."""
