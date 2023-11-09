"""
Run module.
"""
from __future__ import annotations

import typing
from pathlib import Path
from typing import Any

from nefertem.readers.builder import build_reader
from nefertem.run.status import RunStatus
from nefertem.stores.builder import get_all_input_stores, get_input_store, get_output_store
from nefertem.utils.commons import BASE_FILE_READER
from nefertem.utils.file_utils import clean_all
from nefertem.utils.logger import LOGGER
from nefertem.utils.utils import get_time, listify

if typing.TYPE_CHECKING:
    from nefertem.run.handler import RunHandler
    from nefertem.run.run_info import RunInfo


class Run:
    """
    Run object.
    The Run is the main interface to interact with data, metadata and operational framework.
    With the Run object you can:

    - Execute plugins
    - Log metadata
    - Persist artifacts
    - Persist input data

    Attributes
    ----------
    run_info : RunInfo
        Run information.
    run_handler : RunHandler
        Run handler.
    tmp_dir : str
        Default local temporary folder where to store input data.

    Methods
    -------
    persist_data
        Persist input data as artifacts into default store.

    """

    def __init__(self, run_info: RunInfo, run_handler: RunHandler, tmp_dir: str) -> None:
        """
        Constructor.
        """
        self.run_info = run_info
        self.run_handler = run_handler
        self.tmp_dir = tmp_dir
        self._filenames = {}

    ############################
    # Run methods
    ############################

    def _get_base_args(self) -> tuple:
        """
        Return base arguments for metadata.

        Returns
        -------
        tuple
            Base arguments for metadata.
        """
        return self.run_info.run_id, self.run_info.experiment_name

    def _log_run(self) -> None:
        """
        Log run's metadata.

        Returns
        -------
        None
        """
        metadata = self.run_info.to_dict()
        self._log_metadata(metadata, "run")
        self.run_info.nefertem_outputs["files"].append("run.json")

    def _log_metadata(self, src: dict, src_type: str) -> None:
        """
        Log generic metadata.

        Returns
        -------
        None
        """
        get_output_store().log_metadata(src, src_type)

    def _persist_artifact(self, src: Any, src_name: str) -> None:
        """
        Persist artifact in the artifact store.

        Parameters
        ----------
        src : Any
            Artifact to persist.
        src_name : str
            Artifact filename.

        Returns
        -------
        None
        """
        get_output_store().persist_artifact(src, src_name)
        self.run_info.artifact_outputs["files"].append(src_name)

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

    ############################
    # Data
    ############################

    def persist_data(self) -> None:
        """
        Persist input data as artifacts.

        Returns
        -------
        None
        """
        for res in self.run_info.resources:
            store = get_input_store(res.store)
            data_reader = build_reader(BASE_FILE_READER, store)
            for path in listify(res.path):
                tmp = Path(data_reader.fetch_data(path))
                self._persist_artifact(tmp, tmp.name)

    def _clean_all(self) -> None:
        """
        Clean up.
        """
        for store in get_all_input_stores():
            store.clean_paths()
        try:
            clean_all(self.tmp_dir)
        except FileNotFoundError:
            pass

    ############################
    # Context manager
    ############################

    def __enter__(self) -> Run:
        # Handle run's start
        LOGGER.info(f"Starting run {self.run_info.run_id}")

        # Set run's status
        self.run_info.status = RunStatus.RUNNING.value
        self.run_info.started = get_time()

        # Log run's metadata
        self._log_run()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # Handle run's end
        if exc_type is None:
            self.run_info.status = RunStatus.FINISHED.value
        elif exc_type in (InterruptedError, KeyboardInterrupt):
            self.run_info.status = RunStatus.INTERRUPTED.value
        else:
            self.run_info.status = RunStatus.ERROR.value
        self.run_info.finished = get_time()

        # Get libraries used in the run
        self.run_info.run_libraries = self.run_handler.get_libraries()

        # Log run's metadata
        self._log_run()

        # Clean up
        LOGGER.info("Run finished. Clean up of temp resources.")
        self._clean_all()

    ############################
    # Dunder
    ############################

    def __repr__(self) -> str:
        return str(self.run_info.to_dict())
