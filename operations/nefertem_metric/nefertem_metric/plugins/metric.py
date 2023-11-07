from pydantic import BaseModel, Field

from nefertem.utils.utils import build_uuid


class Metric(BaseModel):
    """
    Base model for metric to be evaluated via profiling.
    """

    id: str = Field(default_factory=build_uuid)
    """UUID of metric."""

    name: str
    """Metric identificator as defined by the corresponding domain."""

    title: str
    """Human readable name for the metric."""

    resources: list[str]
    """List of resources on which the metric should be evaluated."""
