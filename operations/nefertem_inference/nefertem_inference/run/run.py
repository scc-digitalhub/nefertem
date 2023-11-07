"""
Run handler module.
"""
from typing import Any

from nefertem_inference.metadata.report import NefertemSchema

from nefertem.metadata.blob import BlobLog
from nefertem.run.run import Run
from nefertem.utils.commons import RESULT_FRAMEWORK, RESULT_NEFERTEM, RESULT_RENDERED


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
        schemas = self.run_handler.get_item(RESULT_FRAMEWORK)
        if schemas:
            return schemas

        self.run_handler.run(self.run_info.resources)
        return self.run_handler.get_item(RESULT_FRAMEWORK)

    def infer_nefertem(self) -> list[NefertemSchema]:
        """
        Execute schema inference on resources with Nefertem.

        Returns
        -------
        list[NefertemSchema]
            Return a list of NefertemSchemas.

        """
        schemas = self.run_handler.get_item(RESULT_NEFERTEM)
        if schemas:
            return schemas

        self.run_handler.run(self.run_info.resources)
        return self.run_handler.get_item(RESULT_NEFERTEM)

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
        for obj in self.run_handler.get_item(RESULT_NEFERTEM):
            metadata = BlobLog(*self._get_base_args(), obj.to_dict()).to_dict()
            self._log_metadata(metadata, "schema")

    def persist_schema(self) -> None:
        """
        Persist frameworks schemas.

        Returns
        -------
        None
        """
        for obj in self.run_handler.get_item(RESULT_RENDERED):
            self._persist_artifact(obj.object, self._render_artifact_name(obj.filename))
