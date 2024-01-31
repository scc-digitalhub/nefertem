"""
Run handler module.
"""
from __future__ import annotations

from typing import Any

from nefertem_core.metadata.blob import Blob
from nefertem_core.plugins.utils import ResultType
from nefertem_core.run.run import Run
from nefertem_inference.metadata.report import NefertemSchema


class RunInference(Run):
    """
    Run inference extension.

    Methods
    -------
    infer
        Execute schema inference on resources.
    infer_framework
        Execute schema inference on resources with inference frameworks.
    infer_nefertem
        Execute schema inference on resources with Nefertem.
    log_schema
        Log NefertemSchemas.
    persist_schema
        Persist frameworks schemas.
    persist_data
        Persist input data as artifacts into default store.
    """

    def infer_framework(self) -> list[Any]:
        """
        Execute schema inference on resources with inference frameworks.

        Returns
        -------
        list[Any]
            Return a list of framework results.

        """
        schemas = self.run_handler.get_item(ResultType.FRAMEWORK.value)
        if schemas:
            return schemas

        self.run_handler.run(self.run_info.resources)
        return self.run_handler.get_item(ResultType.FRAMEWORK.value)

    def infer_nefertem(self) -> list[NefertemSchema]:
        """
        Execute schema inference on resources with Nefertem.

        Returns
        -------
        list[NefertemSchema]
            Return a list of NefertemSchemas.

        """
        schemas = self.run_handler.get_item(ResultType.NEFERTEM.value)
        if schemas:
            return schemas

        self.run_handler.run(self.run_info.resources)
        return self.run_handler.get_item(ResultType.NEFERTEM.value)

    def infer(self) -> tuple[list[Any], list[NefertemSchema]]:
        """
        Execute schema inference on resources.

        Returns
        -------
        Any
            Return a list of NefertemSchemas and the corresponding list of framework results.
        """
        return self.infer_framework(), self.infer_nefertem()

    def log_schema(self) -> None:
        """
        Log NefertemSchemas.

        Returns
        -------
        None
        """
        for obj in self.run_handler.get_item(ResultType.NEFERTEM.value):
            metadata = Blob(*self._get_base_args(), obj.object.to_dict()).to_dict()
            self._log_metadata(metadata, obj.filename)

    def persist_schema(self) -> None:
        """
        Persist frameworks schemas.

        Returns
        -------
        None
        """
        for obj in self.run_handler.get_item(ResultType.RENDERED.value):
            self._persist_artifact(obj.object, obj.filename)
