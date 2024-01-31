from __future__ import annotations

from nefertem_core.utils.utils import build_uuid
from pydantic import BaseModel, Field


class Constraint(BaseModel):
    """
    Base model for constraint.
    """

    id: str = Field(default_factory=build_uuid)
    """UUID of constraint."""

    name: str
    """Constraint id."""

    type: str
    """Constraint type."""

    title: str
    """Human readable name for the constraint."""

    resources: list[str]
    """List of resources affected by the constraint."""

    weight: int
    """Criticity of an eventual error encountered in the validation for the constraint."""
