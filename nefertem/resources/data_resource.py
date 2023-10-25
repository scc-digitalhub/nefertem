"""
Data resource module.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from nefertem.utils.utils import build_uuid


class DataResource(BaseModel):
    """
    Resource configuration class.
    This object represents a physical resource present
    on a backend or a virtual resource rebuildable starting
    from other resources.
    """

    id: str = Field(default_factory=build_uuid)
    """UUID of DataResource."""

    name: str
    """Name of the DataResource."""

    path: str | list[str]
    """An URI (or a list of URI) that point to data."""

    store: str
    """Store name where to find the resource."""

    package: str | None = None
    """Package name that DataResource belongs to."""

    title: str | None = None
    """Human readable name for the DataResource."""

    description: str | None = None
    """A description of the DataResource."""

    tableSchema: str | dict | None = None
    """Resource table schema or path to table schema."""
