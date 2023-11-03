"""
Local metadata store module.
"""
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any

from nefertem.stores.output.objects.base import OutputStore
from nefertem.utils.exceptions import RunError
from nefertem.utils.file_utils import check_path, clean_all, copy_file
from nefertem.utils.io_utils import write_json, write_object


class LocalOutputStore(OutputStore):
    """
    Local metadata store object.

    Allows the client to interact with local filesystem.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self._cnt = {}

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
        self.path = Path(self.path) / exp_name / run_id
        self.artifact_path = self.path / "artifacts"
        self.metadata_path = self.path / "metadata"

        if self.path.exists():
            if not overwrite:
                raise RunError("Run already exists, please use another id.")
            else:
                clean_all(self.path)
                self.artifact_path.mkdir(parents=True)
                self.metadata_path.mkdir(parents=True)
        else:
            self.artifact_path.mkdir(parents=True, exist_ok=True)
            self.metadata_path.mkdir(parents=True, exist_ok=True)

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
        None

        Raises
        ------
        NotImplementedError
            If the object located in 'src' is not one of the accepted types.
        """

        self.artifact_path.mkdir(exist_ok=True)
        dst = self.artifact_path / src_name

        # Local file or dump string
        if isinstance(src, (str, Path)) and check_path(src):
            copy_file(src, dst)

        # Dictionary
        elif isinstance(src, dict) and src_name is not None:
            write_json(src, dst)

        # StringIO/BytesIO buffer
        elif isinstance(src, (BytesIO, StringIO)) and src_name is not None:
            write_object(src, dst)

        else:
            raise NotImplementedError("Invalid object type located at src, it could not be persisted.")

    def log_metadata(self, src: dict, src_type: str) -> None:
        """
        Method that log metadata.

        Parameters
        ----------
        src : dict
            Metadata to log.
        dst : str
            Destination path.
        src_type : str
            Source type.
        overwrite : bool
            Overwrite existing metadata.

        Returns
        -------
        None
        """
        self.metadata_path.mkdir(exist_ok=True)
        filename = self._get_metadata_filename(src_type)
        path = self.metadata_path / filename
        write_json(src, path)

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
        if src_type in ["run", "run_env"]:
            return f"{src_type}.json"
        else:
            self._cnt[src_type] = self._cnt.get(src_type, 0) + 1
            return f"{src_type}_{self._cnt[src_type]}.json"
