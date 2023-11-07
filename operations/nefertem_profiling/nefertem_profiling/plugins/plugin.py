from abc import abstractmethod
from typing import Any

from nefertem_profiling.plugins.utils import RenderTuple

from nefertem.plugins.plugin import Plugin
from nefertem.plugins.utils import ResultType


class ProfilingPlugin(Plugin):
    """
    Run plugin that executes profiling over a Resource.
    """

    _fn_profile = "profile_{}"

    def execute(self) -> dict:
        """
        Method that call specific execution.
        """
        plugin = f"Plugin: {self.lib_name} {self._id};"
        self.logger.info(f"Execute profiling - {plugin}")
        lib_result = self.profile()
        self.logger.info(f"Render report - {plugin}")
        nt_result = self.render_nefertem(lib_result)
        self.logger.info(f"Render artifact - {plugin}")
        render_result = self.render_artifact(lib_result)
        return {
            ResultType.FRAMEWORK.value: lib_result,
            ResultType.NEFERTEM.value: nt_result,
            ResultType.RENDERED.value: render_result,
            ResultType.LIBRARY.value: self.get_framework(),
        }

    @abstractmethod
    def profile(self) -> Any:
        """
        Generate a data profile.
        """

    @staticmethod
    def _get_render_tuple(obj: Any, filename: str) -> RenderTuple:
        """
        Return a RenderTuple.

        Parameters
        ----------
        obj : Any
            Object rendered for persistence.
        filename : str
            Filename.

        Returns
        -------
        RenderTuple
            RenderTuple object.
        """
        return RenderTuple(obj, filename)
