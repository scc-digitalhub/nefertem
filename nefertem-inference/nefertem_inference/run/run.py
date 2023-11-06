"""
Run handler module.
"""
from typing import Any

from nefertem_inference.metadata.report import NefertemSchema

from nefertem.metadata.blob import BlobLog
from nefertem.run.run import Run
from nefertem.utils.commons import RESULT_ARTIFACT, RESULT_NEFERTEM, RESULT_RENDERED


class RunInference(Run):
    """
    Run inference extension.

    Methods
    -------
    infer
        Execute schema inference on resources.
    infer_wrapper
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

    ############################
    # Inferece
    ############################

    def infer_wrapper(self) -> list[Any]:
        """
        Execute schema inference on resources with inference frameworks.

        Returns
        -------
        list[Any]
            Return a list of framework results.

        """
        schemas = self.run_handler.get_item(RESULT_ARTIFACT)
        if schemas:
            return schemas

        self.run_handler.run(self.run_info.resources)
        return self.run_handler.get_item(RESULT_ARTIFACT)

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

    def infer(self, only_nt: bool = False) -> Any:
        """
        Execute schema inference on resources.

        Parameters
        ----------
        only_nt : bool
            Flag to return only the Nefertem report.

        Returns
        -------
        Any
            Return a list of NefertemSchemas and the corresponding list of framework results.
        """
        schema = self.infer_wrapper()
        schema_nt = self.infer_nefertem()
        if only_nt:
            return None, schema_nt
        return schema, schema_nt

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
