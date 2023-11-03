"""
Nefertem base report module.
"""
from nefertem.metadata.base import Metadata


class NefertemBaseReport:
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

    def __init__(
        self,
        lib_name: str,
        lib_version: str,
        duration: float,
    ) -> None:
        """
        Constructor.
        """
        super().__init__()
        self.lib_name = lib_name
        self.lib_version = lib_version
        self.duration = duration

    def to_dict(self) -> dict:
        return self.__dict__

    def __repr__(self) -> str:
        return f"{self.to_dict()}"


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
    value: Any
        Metric value

    """

    def __init__(self, name: str, title: str, type: str, args: dict, value: any) -> None:
        """
        Constructor.
        """
        self.name = name
        self.title = title
        self.type = type
        self.args = args
        self.value = value

    def to_dict(self) -> dict:
        return self.__dict__


class NefertemProfile(NefertemBaseReport):
    """
    Succint version of a profile produced by some profiling library.

    Attributes
    ----------
    stats : dict
        Descriptors of data stats.
    fields : dict
        Descriptors of data fields.
    metrics : list[dict]
        List of metric evaluations over dataset.
    field_metrics: dict
        Dataset field metrics
    """

    def __init__(
        self,
        lib_name: str,
        lib_version: str,
        duration: float,
        stats: dict,
        fields: dict,
        metrics: list[dict],
        field_metrics: dict,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(lib_name, lib_version, duration)
        self.stats = stats
        self.fields = fields
        self.metrics = metrics
        self.field_metrics = field_metrics


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

    def __init__(
        self,
        lib_name: str,
        lib_version: str,
        duration: float,
        constraint: dict,
        valid: bool,
        errors: list,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(lib_name, lib_version, duration)
        self.constraint = constraint
        self.valid = valid
        self.errors = errors
