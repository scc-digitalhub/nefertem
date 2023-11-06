"""
Run module.
"""
from __future__ import annotations

import typing
from pathlib import Path
from typing import Any

from nefertem.metadata.artifact import Artifact
from nefertem.metadata.env import EnvLog
from nefertem.readers.builder import build_reader
from nefertem.run.status import RunStatus
from nefertem.stores.builder import get_all_input_stores, get_input_store, get_output_store
from nefertem.utils.commons import BASE_FILE_READER, NEFERTEM_VERSION
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
        return self.run_info.run_id, self.run_info.experiment_name, NEFERTEM_VERSION

    def _log_run(self) -> None:
        """
        Log run's metadata.

        Returns
        -------
        None
        """
        metadata = self.run_info.to_dict()
        self._log_metadata(metadata, "run")

    def _log_env(self) -> None:
        """
        Log run's enviroment details.

        Returns
        -------
        None
        """
        metadata = EnvLog(*self._get_base_args()).to_dict()
        self._log_metadata(metadata, "run_env")

    def _log_artifact(self, src_name: str) -> None:
        """
        Log artifact metadata.

        Returns
        -------
        None
        """
        metadata = Artifact(*self._get_base_args(), self.run_info.run_art_path, src_name).to_dict()
        get_output_store().log_metadata(metadata, "artifact")

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
        self._log_artifact(src_name)

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

    def _get_libraries(self) -> None:
        """
        Get the list of libraries used by the run.

        Returns
        -------
        None
        """
        self.run_info.run_libraries = self.run_handler.get_libraries()

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
                get_output_store().persist_artifact(tmp, tmp.name)

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
        LOGGER.info(f"Starting run {self.run_info.run_id}")
        self.run_info.begin_status = RunStatus.RUNNING.value
        self.run_info.started = get_time()
        self._log_run()
        self._log_env()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            self.run_info.end_status = RunStatus.FINISHED.value
        elif exc_type in (InterruptedError, KeyboardInterrupt):
            self.run_info.end_status = RunStatus.INTERRUPTED.value
        else:
            self.run_info.end_status = RunStatus.ERROR.value

        self._get_libraries()
        self.run_info.finished = get_time()
        self._log_run()
        LOGGER.info("Run finished. Clean up of temp resources.")

        self._clean_all()

    ############################
    # Dunder
    ############################

    def __repr__(self) -> str:
        return str(self.run_info.to_dict())
