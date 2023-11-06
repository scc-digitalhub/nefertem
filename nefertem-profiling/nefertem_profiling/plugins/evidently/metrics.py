"""
Evidently metric input model.
"""
from pydantic import BaseModel, Field

from nefertem_profiling.plugins.metric import Metric


class Element(BaseModel):
    """
    Evidently single test
    """

    type: str
    """Evidently test/metric type (fully qualified class name)."""
    values: dict | None = None
    """Custom parameters for the test/metric."""


class MetricEvidently(Metric):
    """
    Evidently metric input model.
    """

    type: str = Field("evidently", Literal=True)
    """Metric input type ("Evidently")."""

    resource: str
    """Resource to profile."""

    reference_resource: str | None = None
    """Resource to use as reference."""

    metrics: list[Element]
    """Evidently tests."""
