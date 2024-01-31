"""
Data resource module.
"""
from __future__ import annotations

from typing import Union

from nefertem_core.utils.utils import build_uuid
from pydantic import BaseModel, Field


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

    path: Union[str, list[str]]
    """An URI (or a list of URI) that point to data."""

    store: str
    """Store name where to find the resource."""

    package: str = None
    """Package name that DataResource belongs to."""

    title: str = None
    """Human readable name for the DataResource."""

    description: str = None
    """A description of the DataResource."""

    table_schema: Union[str, dict] = None
    """Resource table schema or path to table schema."""
