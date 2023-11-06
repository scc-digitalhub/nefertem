"""
Inference plugin abstract class module.
"""
from abc import ABCMeta, abstractmethod
from typing import Any

from nefertem.plugins.plugin import Plugin
from nefertem.utils.commons import RESULT_ARTIFACT, RESULT_LIBRARY, RESULT_NEFERTEM, RESULT_RENDERED


class InferencePlugin(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes inference over a Resource.
    """

    _fn_schema = "schema_{}"

    def execute(self) -> dict:
        """
        Method that call specific execution.
        """
        plugin = f"Plugin: {self.lib_name} {self._id};"
        self.logger.info(f"Execute inference - {plugin}")
        lib_result = self.infer()
        self.logger.info(f"Render report - {plugin}")
        nt_result = self.render_nefertem(lib_result)
        self.logger.info(f"Render artifact - {plugin}")
        render_result = self.render_artifact(lib_result)
        return {
            RESULT_ARTIFACT: lib_result,
            RESULT_NEFERTEM: nt_result,
            RESULT_RENDERED: render_result,
            RESULT_LIBRARY: self.get_library(),
        }

    @abstractmethod
    def infer(self) -> Any:
        """
        Inference method for schema.
        """

    @staticmethod
    def _get_fields(name: str = None, type_: str = None) -> dict:
        """
        Return a common field structure.
        """
        return {"name": name, "type": type_}