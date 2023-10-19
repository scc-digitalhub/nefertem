from dataclasses import dataclass, field
from typing import List

from nefertem.metadata.reports.base import NefertemBaseReport


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
    metrics: List["NefertemProfileMetric"] = field(default_factory=list)
    field_metrics: dict = field(default_factory=dict)
