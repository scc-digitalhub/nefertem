"""
Implementation of local metadata store.
"""
from nefertem.stores.metadata.objects.base import MetadataStore
from nefertem.utils.exceptions import RunError
from nefertem.utils.file_utils import check_dir, clean_all, get_path, make_dir
from nefertem.utils.io_utils import write_json
from nefertem.metadata.kinds import MetadataKind


class LocalMetadataStore(MetadataStore):
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
        uri = self.get_run_path(exp_name, run_id)
        self._check_dst_folder(uri, overwrite, init=True)

    def log_metadata(self, metadata: dict, dst: str, src_type: str, overwrite: bool) -> None:
        """
        Method that log metadata.

        Parameters
        ----------
        metadata : dict
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
        self._check_dst_folder(dst, overwrite)
        dst = self._build_source_destination(dst, src_type)
        write_json(metadata, dst)

    @staticmethod
    def _check_dst_folder(dst: str, overwrite: bool, init: bool = False) -> None:
        """
        Check if run folder already exist, otherwise it creates it.

        Parameters
        ----------
        dst : str
            Destination path.
        overwrite : bool
            Overwrite existing run folder.
        init : bool
            Initialize run folder.

        Raises
        ------
        RunError
            If run already exists and init is False.

        Returns
        -------
        None
        """
        if check_dir(dst):
            if init and not overwrite:
                raise RunError("Run already exists, please use another id.")
            if init and overwrite:
                clean_all(dst)
                make_dir(dst)
        else:
            make_dir(dst)

    def _build_source_destination(self, dst: str, src_type: str) -> str:
        """
        Return source path based on input source type.

        Parameters
        ----------
        dst : str
            Destination path.
        src_type : str
            Source type.

        Returns
        -------
        str
            Source path.
        """
        if src_type in [MetadataKind.RUN.value, MetadataKind.RUN_ENV.value]:
            filename = f"{src_type}.json"
        else:
            self._cnt[src_type] = self._cnt.get(src_type, 0) + 1
            filename = f"{src_type}_{self._cnt[src_type]}.json"
        return get_path(dst, filename)

    def get_run_path(self, exp_name: str, run_id: str) -> str:
        """
        Return the path of the metadata folder for the Run.

        Parameters
        ----------
        exp_name : str
            Experiment name.
        run_id : str
            Run id.

        Returns
        -------
        str
            Path of the metadata folder for the Run.
        """
        return get_path(self.path, exp_name, run_id)
