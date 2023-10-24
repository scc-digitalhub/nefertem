
from pydantic import BaseModel, Field

from nefertem.models.constraints.base import Constraint
from nefertem.utils.commons import LIBRARY_EVIDENTLY
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


class EvidentlyElement(BaseModel):
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

    type: str = Field(LIBRARY_EVIDENTLY, Literal=True)
    """Metric input type ("Evidently")."""

    resource: str
    """Resource to profile."""

    reference_resource: str | None = None
    """Resource to use as reference."""

    metrics: list[EvidentlyElement]
    """Evidently tests."""


class ConstraintEvidently(Constraint):
    """
    Evidently constraint.
    """

    type: str = Field(LIBRARY_EVIDENTLY, Literal=True)
    """Constraint type ("Evidently")."""

    resource: str
    """Resource to validate."""

    reference_resource: str | None = None
    """Resource to use as reference."""

    tests: list[EvidentlyElement]
    """Evidently tests."""
