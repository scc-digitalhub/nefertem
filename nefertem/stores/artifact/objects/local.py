"""
LocalArtifactStore module.
"""
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any

from nefertem.stores.artifact.objects.base import ArtifactStore, StoreConfig
from nefertem.utils.file_utils import check_dir, check_path, copy_file, get_path, make_dir
from nefertem.utils.io_utils import write_json, write_object


class LocalStoreConfig(StoreConfig):
    """
    Local store configuration class.
    """


class LocalArtifactStore(ArtifactStore):
    """
    Implementation of a local artifact store object that allows the user to
    interact with the local filesystem.
    """

    def __init__(
        self,
        name: str,
        store_type: str,
        uri: str,
        temp_dir: str,
        is_default: bool,
        config: LocalStoreConfig,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(name, store_type, uri, temp_dir, is_default)
        self.config = config

    ############################
    # I/O methods
    ############################

    def persist_artifact(self, src: Any, dst: str, src_name: str, *args) -> None:
        """
        Method to persist an artifact.

        Parameters
        ----------
        src : Any
            The source file to be persisted.
        dst : str
            Destination folder.
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
        if not check_dir(dst):
            make_dir(dst)

        if src_name is not None:
            dst = get_path(dst, src_name)

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

    def fetch_file(self, src: str) -> str:
        """
        Return the path where a resource it is stored.

        Parameters
        ----------
        src : str
            The name of the file.

        Returns
        -------
        str
            The location of the requested file.
        """
        return src

    def fetch_native(self, src: str) -> str:
        """
        Return a native format path for a resource.

        Parameters
        ----------
        src : str
            The name of the file.

        Returns
        -------
        str
            The location of the requested file.
        """
        return src
