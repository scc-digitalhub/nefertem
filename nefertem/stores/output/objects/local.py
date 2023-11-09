"""
Local metadata store module.
"""
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any

from nefertem.stores.output.objects._base import OutputStore
from nefertem.utils.exceptions import RunError
from nefertem.utils.file_utils import clean_all, copy_file
from nefertem.utils.io_utils import write_json, write_object


class LocalOutputStore(OutputStore):
    """
    Local metadata store object.

    Allows the client to interact with local filesystem.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self._cnt = {}
        self._filenames = {}

    ############################
    # Run methods
    ############################

    def init_run(self, exp_name: str, run_id: str, overwrite: bool) -> None:
        """
        Check run metadata folder existence. If folder doesn't exist, create it.
        If overwrite is True, it delete all the run's folder contents.

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
        self.run_path = Path(self.get_run_path(exp_name, run_id))
        self.artifact_path = self.run_path / "artifacts"
        self.metadata_path = self.run_path / "metadata"

        if self.run_path.exists():
            if not overwrite:
                raise RunError("Run already exists, please use another id.")
            else:
                clean_all(self.run_path)
                self.artifact_path.mkdir(parents=True)
                self.metadata_path.mkdir(parents=True)
        else:
            self.artifact_path.mkdir(parents=True, exist_ok=True)
            self.metadata_path.mkdir(parents=True, exist_ok=True)

    def get_run_path(self, exp_name: str, run_id: str) -> str:
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
        str
            Run path.
        """
        return str(Path(self.path) / exp_name / run_id)

    ############################
    # Write methods
    ############################

    def log_metadata(self, src: dict, src_type: str) -> str:
        """
        Method that log metadata.

        Parameters
        ----------
        src : dict
            Metadata to log.
        src_type : str
            Source type.

        Returns
        -------
        str
            Path of the metadata file.
        """

        if not isinstance(src, dict):
            raise RunError("Metadata must be a dictionary.")

        self.metadata_path.mkdir(exist_ok=True)
        filename = self._get_metadata_filename(src_type)
        dst = self.metadata_path / filename
        write_json(src, dst)
        return str(dst)

    def _get_metadata_filename(self, src_type: str) -> str:
        """
        Return source path based on input source type.

        Parameters
        ----------
        src_type : str
            Source type.

        Returns
        -------
        str
            Filename.
        """
        if src_type == "run_metadata":
            return f"{src_type}.json"
        else:
            self._cnt[src_type] = self._cnt.get(src_type, 0) + 1
            return f"{src_type}_{self._cnt[src_type]}.json"

    def persist_artifact(self, src: Any, src_name: str) -> None:
        """
        Method to persist an artifact.

        Parameters
        ----------
        src : Any
            The source file to be persisted.
        src_name : str
            Name given to the source file.

        Returns
        -------
        str
            Path of the artifact.

        Raises
        ------
        RunError
            If the source type is not supported.
        """

        self.artifact_path.mkdir(exist_ok=True)
        filename = self._get_artifact_name(src_name)
        dst = self.artifact_path / filename

        # Local file or dump string
        if isinstance(src, (str, Path)):
            copy_file(src, dst)

        # Dictionary
        elif isinstance(src, dict):
            write_json(src, dst)

        # StringIO/BytesIO buffer
        elif isinstance(src, (BytesIO, StringIO)):
            write_object(src, dst)

        else:
            raise RunError("Invalid object type, it could not be persisted.")

        return str(dst)

    def _get_artifact_name(self, filename: str) -> str:
        """
        Return a modified filename to avoid overwriting in persistence.

        Parameters
        ----------
        filename : str
            Filename.

        Returns
        -------
        str
            Return a modified filename.
        """
        self._filenames[filename] = self._filenames.get(filename, 0) + 1
        return f"{Path(filename).stem}_{self._filenames[filename]}{Path(filename).suffix}"
