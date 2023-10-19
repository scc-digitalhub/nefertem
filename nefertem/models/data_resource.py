from typing import List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field


class DataResource(BaseModel):
    """
    Resource configuration class.
    This object represents a physical resource present
    on a backend or a virtual resource rebuildable starting
    from other resources.
    """

    id: str = Field(default_factory=uuid4)
    """UUID of DataResource."""

    name: str
    """Name of the DataResource."""

    path: Union[str, List[str]]
    """An URI (or a list of URI) that point to data."""

    store: str
    """Store name where to find the resource."""

    package: Optional[str] = None
    """Package name that DataResource belongs to."""

    title: Optional[str] = None
    """Human readable name for the DataResource."""

    description: Optional[str] = None
    """A description of the DataResource."""

    tableSchema: Optional[Union[str, dict]] = None
    """Resource table schema or path to table schema."""
