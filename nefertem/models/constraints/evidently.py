from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from nefertem.models.constraints.base import Constraint
from nefertem.utils.commons import LIBRARY_EVIDENTLY


class Metric(BaseModel):
    """
    Base model for metric to be evaluated via profiling.
    """

    id: str = Field(default_factory=uuid4)
    """UUID of metric."""

    name: str
    """Metric identificator as defined by the corresponding domain."""

    title: str
    """Human readable name for the metric."""

    resources: List[str]
    """List of resources on which the metric should be evaluated."""


class EvidentlyElement(BaseModel):
    """
    Evidently single test
    """

    type: str
    """Evidently test/metric type (fully qualified class name)."""
    values: Optional[dict] = None
    """Custom parameters for the test/metric."""


class MetricEvidently(Metric):
    """
    Evidently metric input model.
    """

    type: str = Field(LIBRARY_EVIDENTLY, Literal=True)
    """Metric input type ("Evidently")."""

    resource: str
    """Resource to profile."""

    reference_resource: Optional[str] = None
    """Resource to use as reference."""

    metrics: List[EvidentlyElement]
    """Evidently tests."""


class ConstraintEvidently(Constraint):
    """
    Evidently constraint.
    """

    type: str = Field(LIBRARY_EVIDENTLY, Literal=True)
    """Constraint type ("Evidently")."""

    resource: str
    """Resource to validate."""

    reference_resource: Optional[str] = None
    """Resource to use as reference."""

    tests: List[EvidentlyElement]
    """Evidently tests."""
