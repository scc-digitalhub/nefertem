"""
Local metadata store module.
"""
from __future__ import annotations

import shutil
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any

from nefertem.stores.output.objects._base import OutputStore
from nefertem.utils.exceptions import RunError
from nefertem.utils.io_utils import write_json, write_object


class LocalOutputStore(OutputStore):
    """
    Local metadata store object.

    Allows the client to interact with local filesystem.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)

        self.path = Path(self.path)

        self._initialized = False
        self._run_path = None
        self._artifact_path = None
        self._metadata_path = None

    ############################
    # Run methods
    ############################

    def init_run(self, exp_name: str, run_id: str, overwrite: bool) -> None:
        """
        Initial run folders. If folder doesn't exist, create it.
        If overwrite is True, delete the folder and create it again.

        Parameters
        ----------
        exp_name : str
            Experiment name.
        run_id : str
            Run id.

        Returns
        -------
        None
        """
        self._set_paths(exp_name, run_id)
        if self._run_path.exists():
            if not overwrite:
                raise RunError("Run already exists, please use another id.")
            else:
                shutil.rmtree(self._run_path)
                self._create_run_directories()
        else:
            self._create_run_directories()
        self._initialized = True

    def _set_paths(self, exp_name: str, run_id: str) -> None:
        """
        Set run paths.

        Parameters
        ----------
        exp_name : str
            Experiment name.
        run_id : str
            Run id.

        Returns
        -------
        None
        """
        self._run_path = self.path / exp_name / run_id
        self._artifact_path = self._run_path / "artifacts"
        self._metadata_path = self._run_path / "metadata"

    def _create_run_directories(self) -> None:
        """
        Create run folders.

        Returns
        -------
        None
        """
        self._run_path.mkdir(parents=True)
        self._artifact_path.mkdir()
        self._metadata_path.mkdir()

    def get_run_path(self) -> Path:
        """
        Return run path.

        Parameters
        ----------
        exp_name : str
            Experiment name.
        run_id : str
            Run id.

        Returns
        -------
        Path
            Run path.

        Raises
        ------
        RunError
            If the run is not initialized.
        """
        if not self._initialized:
            raise RunError("Run not initialized.")
        return self._run_path

    ############################
    # Write methods
    ############################

    def log_metadata(self, obj: dict, filename: str) -> Path:
        """
        Method that log metadata.

        Parameters
        ----------
        obj: dict
            Metadata dictionary to be logged.
        filename: str
            Filename for the metadata.

        Returns
        -------
        Path
            Path to the metadata file.
        """

        if not isinstance(obj, dict):
            raise RunError("Metadata must be a dictionary.")
        dst = self._metadata_path / filename
        write_json(obj, dst)
        return dst

    def persist_artifact(self, obj: Any, filename: str) -> Path:
        """
        Method to persist an artifact.
        The local store supports the following types:

        - Local file or dump string
        - Dictionary
        - StringIO/BytesIO buffer

        Parameters
        ----------
        obj : Any
            The source object to be persisted.
        filename: str
            Filename for the artifact.

        Returns
        -------
        str
            Path to the artifact.

        Raises
        ------
        RunError
            If the source type is not supported.
        """
        dst = self._artifact_path / filename

        if isinstance(obj, (str, Path)):
            shutil.copy(obj, dst)

        elif isinstance(obj, dict):
            write_json(obj, dst)

        elif isinstance(obj, (BytesIO, StringIO)):
            write_object(obj, dst)

        else:
            raise RunError("Invalid object type, it can not be persisted.")

        return dst
