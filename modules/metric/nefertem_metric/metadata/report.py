from nefertem_core.metadata.report import NefertemBaseReport


class ProfileMetric:
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


class NefertemMetricReport(NefertemBaseReport):
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
        framework_name: str,
        framework_version: str,
        duration: float,
        stats: dict,
        fields: dict,
        metrics: list[dict],
        field_metrics: dict,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(framework_name, framework_version, duration)
        self.stats = stats
        self.fields = fields
        self.metrics = metrics
        self.field_metrics = field_metrics
