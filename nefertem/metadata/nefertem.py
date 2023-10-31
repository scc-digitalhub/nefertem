"""
Nefertem base report module.
"""
from dataclasses import dataclass, field

from nefertem.metadata.base import Metadata


@dataclass
class NefertemBaseReport(Metadata):
    """
    Nefertem base report class.

    Attributes
    ----------
    lib_name : str
        Execution library name.
    lib_version : str
        Execution library version.
    duration : float
        Time required by the execution process.
    """

    lib_name: str
    lib_version: str
    duration: float


@dataclass
class NefertemProfileMetric:
    """
    Metric report data.

    Attributes
    ----------
    name: str
        Metric identificator as defined by the corresponding domain.
    title: str
        Human readable name for the metric.
    type: str
        Metric domain (es., library).
    args: dict
        Metric arguments (if applies)
    value: any
        Metric value

    """

    name: str
    title: str
    type: str
    args: dict = field(default_factory=dict)
    value: any = None


@dataclass
class NefertemProfile(NefertemBaseReport):
    """
    Succint version of a profile produced by some profiling library.

    Attributes
    ----------
    stats : dict
        Descriptors of data stats.
    fields : dict
        Descriptors of data fields.
    metrics : list
        List of metric evaluations over dataset.
    field_metrics: dict
        Dataset field metrics
    """

    stats: dict
    fields: dict
    metrics: list[NefertemProfileMetric] = field(default_factory=list)
    field_metrics: dict = field(default_factory=dict)


@dataclass
class NefertemReport(NefertemBaseReport):
    """
    Succint version of a report produced by some validation library.

    Attributes
    ----------
    constraint : dict
        Constraint validated.
    valid : bool
        Validation outcome.
    errors : list
        List of errors found by validation process.

    """

    constraint: dict
    valid: bool
    errors: dict


@dataclass
class NefertemSchema(NefertemBaseReport):
    """
    Succint version of an inferred schema produced by some inference library.

    Attributes
    ----------
    fields : list
        A list of fields.

    """

    fields: list