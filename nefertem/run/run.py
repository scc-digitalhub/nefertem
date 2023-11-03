"""
Run module.
"""
from __future__ import annotations

import typing
from pathlib import Path
from typing import Any

from nefertem.metadata.blob import BlobLog
from nefertem.metadata.env import EnvLog
from nefertem.readers.builder import build_reader
from nefertem.stores.builder import get_all_input_stores, get_input_store, get_output_store
from nefertem.utils.commons import (
    BASE_FILE_READER,
    NEFERTEM_VERSION,
    RESULT_ARTIFACT,
    RESULT_NEFERTEM,
    RESULT_RENDERED,
    STATUS_ERROR,
    STATUS_FINISHED,
    STATUS_INIT,
    STATUS_INTERRUPTED,
)
from nefertem.utils.file_utils import clean_all, get_absolute_path
from nefertem.utils.logger import LOGGER
from nefertem.utils.uri_utils import get_name_from_uri
from nefertem.utils.utils import get_time, listify

if typing.TYPE_CHECKING:
    from nefertem.metadata.nefertem import NefertemSchema
    from nefertem.metadata.run_info import RunInfo
    from nefertem.plugins.utils import RenderTuple
    from nefertem.run.handler import RunHandler


class Run:
    """
    Run object.
    The Run is the main interface to interact with data, metadata and
    operational framework. With the Run, you can infer, validate and
    profile resources, log and persist data and metadata.

    Methods
    -------
    infer_wrapper
        Execute schema inference on resources with inference frameworks.
    infer_nefertem
        Execute schema inference on resources with Nefertem.
    infer
        Execute schema inference on resources.
    log_schema
        Log NefertemSchemas.
    persist_schema
        Persist frameworks schemas.
    validate_wrapper
        Execute validation on resources with validation frameworks.
    validate_nefertem
        Execute validation on resources with Nefertem.
    validate
        Execute validation on resources.
    log_report
        Log NefertemReports.
    persist_report
        Persist frameworks reports.
    profile_wrapper
        Execute profiling on resources with profiling frameworks.
    profile_nefertem
        Execute profiling on resources with Nefertem.
    profile
        Execute profiling on resources.
    log_profile
        Log NefertemProfiles.
    persist_profile
        Persist frameworks profiles.
    persist_data
        Persist input data as artifacts into default store.

    """

    def __init__(self, run_info: RunInfo, run_handler: RunHandler, tmp_dir: str, overwrite: bool) -> None:
        self.run_info = run_info
        self._run_handler = run_handler
        self._tmp_dir = tmp_dir
        self._overwrite = overwrite

        self._filenames = {}

    ############################
    # Run methods
    ############################

    def _log_run(self) -> None:
        """
        Log run's metadata.

        Returns
        -------
        None
        """
        metadata = self._get_blob(self.run_info.to_dict())
        self._log_metadata(metadata, "run")

    def _log_env(self) -> None:
        """
        Log run's enviroment details.

        Returns
        -------
        None
        """
        metadata = self._get_blob(EnvLog().to_dict())
        self._log_metadata(metadata, "run_env")

    def _get_blob(self, blob: dict | None = None) -> dict:
        """
        Return structured blob to log.

        Returns
        -------
        dict
            Return a structured blob.
        """
        blob = blob if blob is not None else {}
        return BlobLog(self.run_info.run_id, self.run_info.experiment_name, NEFERTEM_VERSION, blob).to_dict()

    def _log_artifact(self, src_name: str | None = None) -> None:
        """
        Log artifact metadata.

        Returns
        -------
        None
        """
        metadata = self._get_blob({"uri": self.run_info.run_art_path, "name": src_name})
        get_output_store().log_metadata(metadata, "artifact")

    def _log_metadata(self, src: dict, src_type: str) -> None:
        """
        Log generic metadata.

        Returns
        -------
        None
        """
        get_output_store().log_metadata(src, src_type)

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

    def _persist_artifact(self, obj: RenderTuple) -> None:
        """
        Persist artifact in the artifact store.

        Parameters
        ----------
        obj : RenderTuple
            Tuple containing the object to persist and the filename.

        Returns
        -------
        None
        """
        src_name = self._render_artifact_name(obj.filename)
        get_output_store().persist_artifact(obj.object, src_name)
        self._log_artifact(src_name)

    def _get_libraries(self) -> None:
        """
        Return the list of libraries used by the run.

        Returns
        -------
        None
        """
        self.run_info.run_libraries = self._run_handler.get_libs()

    ############################
    # Data
    ############################

    def persist_data(self) -> None:
        """
        Persist input data as artifacts into default store.

        Depending on the functioning of the store object on which the artifacts are stored,
        the store will try to download the data locally.
        In the case of SQL origin, the format will be parquet.
        In the case of remote or s3 origin, the persistence format will be the same
        as the artifacts present in the storage.

        Returns
        -------
        None
        """
        for res in self.run_info.resources:
            store = get_input_store(res.store)
            data_reader = build_reader(BASE_FILE_READER, store)
            for path in listify(res.path):
                tmp_pth = data_reader.fetch_data(path)
                tmp_pth = get_absolute_path(tmp_pth)
                filename = get_name_from_uri(tmp_pth)
                get_output_store().persist_artifact(tmp_pth, filename)

    def _clean_all(self) -> None:
        """
        Clean up.
        """
        for store in get_all_input_stores():
            store.clean_paths()
        try:
            clean_all(self._tmp_dir)
        except FileNotFoundError:
            pass

    ############################
    # Context manager
    ############################

    def __enter__(self) -> Run:
        # Set run status
        LOGGER.info(f"Starting run {self.run_info.run_id}")
        self.run_info.begin_status = STATUS_INIT
        self.run_info.started = get_time()
        self._log_run()
        self._log_env()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            self.run_info.end_status = STATUS_FINISHED
        elif exc_type in (InterruptedError, KeyboardInterrupt):
            self.run_info.end_status = STATUS_INTERRUPTED
        elif exc_type in (AttributeError,):
            self.run_info.end_status = STATUS_ERROR
        else:
            self.run_info.end_status = STATUS_ERROR

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
