"""
Inference plugin abstract class module.
"""
from abc import abstractmethod
from typing import Any

from nefertem_inference.plugins.utils import RenderTuple

from nefertem.plugins.plugin import Plugin
from nefertem.plugins.utils import ResultType


class InferencePlugin(Plugin):
    """
    Run plugin that executes inference over a Resource.
    """

    _fn_schema = "schema_{}"

    def execute(self) -> dict:
        """
        Method that call specific execution.

        Returns
        -------
        dict
            Results of execution.
        """
        plugin = f"Plugin: {self.lib_name} {self._id};"
        self.logger.info(f"Execute inference - {plugin}")
        lib_result = self.infer()
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
    def infer(self) -> Any:
        """
        Inference method for schema.
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

    @staticmethod
    def _get_fields(name: str = None, type_: str = None) -> dict:
        """
        Return a common field structure.

        Parameters
        ----------
        name : str
            Field name.
        type_ : str
            Field type.

        Returns
        -------
        dict
            Field structure.
        """
        return {"name": name, "type": type_}
