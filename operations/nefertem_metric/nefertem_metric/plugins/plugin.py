from abc import abstractmethod
from typing import Any

from nefertem.plugins.plugin import Plugin
from nefertem.utils.commons import RESULT_FRAMEWORK, RESULT_LIBRARY, RESULT_NEFERTEM, RESULT_RENDERED


class MetricPlugin(Plugin):
    """
    Run plugin that executes metric over a Resource.
    """

    _fn_metric = "metric_{}"

    def __init__(self) -> None:
        super().__init__()
        self.metric = None

    def execute(self) -> dict:
        """
        Method that call specific execution.
        """
        plugin = f"Plugin: {self.lib_name} {self._id};"
        self.logger.info(
            f"Execute metric - {plugin}" + (" Metric: {self.metric.name}" if self.metric is not None else "")
        )
        lib_result = self.measure()
        self.logger.info(f"Render report - {plugin}")
        nt_result = self.render_nefertem(lib_result)
        self.logger.info(f"Render artifact - {plugin}")
        render_result = self.render_artifact(lib_result)
        return {
            RESULT_FRAMEWORK: lib_result,
            RESULT_NEFERTEM: nt_result,
            RESULT_RENDERED: render_result,
            RESULT_LIBRARY: self.get_library(),
        }

    @abstractmethod
    def measure(self) -> Any:
        """
        Generate metrics.
        """
