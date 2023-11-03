"""
Run handler module.
"""
from __future__ import annotations

import typing
from typing import Any
from pathlib import Path

from nefertem_inference.metadata.report import NefertemSchema
from nefertem.run.run import Run
from nefertem.utils.commons import RESULT_ARTIFACT, RESULT_NEFERTEM, RESULT_RENDERED

if typing.TYPE_CHECKING:
    from nefertem_inference.run.handler import RunHandlerInference

    from nefertem.run.run_info import RunInfo


class RunInference(Run):
    """
    Run inference extension.

    Attributes
    ----------
    run_info : RunInfo
        Run information.
    run_handler : RunHandlerInference
        Run handler.

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

    def __init__(self, run_info: RunInfo, run_handler: RunHandlerInference) -> None:
        """
        Constructor.
        """
        super().__init__(run_info)
        self._run_handler: RunHandlerInference = run_handler
        self._filenames = {}

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
        schemas = self._run_handler.get_item(RESULT_ARTIFACT)
        if schemas:
            return schemas

        self._run_handler.infer(self.run_info.resources)
        return self._run_handler.get_item(RESULT_ARTIFACT)

    def infer_nefertem(self) -> list[NefertemSchema]:
        """
        Execute schema inference on resources with Nefertem.

        Returns
        -------
        list[NefertemSchema]
            Return a list of NefertemSchemas.

        """
        schemas = self._run_handler.get_item(RESULT_NEFERTEM)
        if schemas:
            return schemas

        self._run_handler.infer(self.run_info.resources)
        return self._run_handler.get_item(RESULT_NEFERTEM)

    def infer(self, only_nt: bool = False) -> Any:
        """
        Execute schema inference on resources.

        Parameters
        ----------
        parallel : bool
            Flag to execute operation in parallel.
        num_worker : int
            Number of workers to execute operation in parallel, by default 10
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
        for obj in self._run_handler.get_item(RESULT_NEFERTEM):
            metadata = {
                "run_id": self.run_info.run_id,
                "experiment_id": self.run_info.experiment_name,
                "nefertem_version": self.run_info.nefertem_version,
                **obj.to_dict(),
            }
            self._log_metadata(metadata, "schema")

    def persist_schema(self) -> None:
        """
        Persist frameworks schemas.

        Returns
        -------
        None
        """
        for obj in self._run_handler.get_item(RESULT_RENDERED):
            self._persist_artifact(obj.object, self._render_artifact_name(obj.filename))

    def _get_libraries(self) -> None:
        """
        Set the list of libraries used by the run.

        Returns
        -------
        None
        """
        self.run_info.run_libraries = self._run_handler.get_libs()

    ############################
    # Helpers
    ############################

    def _render_artifact_name(self, filename: str) -> str:
        """
        Return a modified filename to avoid overwriting in persistence.

        Returns
        -------
        str
            Return a modified filename.
        """
        self._filenames[filename] = self._filenames.get(filename, 0) + 1
        return f"{Path(filename).stem}_{self._filenames[filename]}{Path(filename).suffix}"
