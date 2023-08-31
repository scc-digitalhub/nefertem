"""
Implementation of local metadata store.
"""
from typing import Optional

from nefertem.store_metadata.metadata_store import MetadataStore
from nefertem.utils import commons as cfg
from nefertem.utils.exceptions import RunError
from nefertem.utils.file_utils import check_dir, get_path, make_dir, clean_all
from nefertem.utils.io_utils import write_json


class LocalMetadataStore(MetadataStore):
    """
    Local metadata store object.

    Allows the client to interact with local filesystem.

    """

    def __init__(
        self,
        name: str,
        store_type: str,
        metadata_uri: str,
        config: Optional[dict] = None,
    ) -> None:
        super().__init__(name, store_type, metadata_uri, config)
        self._filenames = {
            self._RUN_METADATA: cfg.FN_RUN_METADATA,
            self._NT_REPORT: cfg.FN_NT_REPORT,
            self._NT_SCHEMA: cfg.FN_NT_SCHEMA,
            self._NT_PROFILE: cfg.FN_NT_PROFILE,
            self._ARTIFACT_METADATA: cfg.FN_ARTIFACT_METADATA,
            self._RUN_ENV: cfg.FN_RUN_ENV,
        }
        self._cnt = {
            self._NT_REPORT: 0,
            self._NT_SCHEMA: 0,
            self._NT_PROFILE: 0,
            self._ARTIFACT_METADATA: 0,
        }

    def init_run(self, exp_name: str, run_id: str, overwrite: bool) -> None:
        """
        Check run metadata folder existence.
        If folder doesn't exist, create it.
        If overwrite is True, it delete all the run's folder contents.
        """
        uri = self.get_run_metadata_uri(exp_name, run_id)
        self._check_dst_folder(uri, overwrite, init=True)

    def log_metadata(
        self, metadata: dict, dst: str, src_type: str, overwrite: bool
    ) -> None:
        """
        Method that log metadata.
        """
        self._check_dst_folder(dst, overwrite)
        dst = self._build_source_destination(dst, src_type)
        write_json(metadata, dst)

    @staticmethod
    def _check_dst_folder(
        dst: str, overwrite: bool, init: Optional[bool] = False
    ) -> None:
        """
        Check if run folder already exist, otherwise it creates it.
        """
        if check_dir(dst):
            if init and not overwrite:
                raise RunError("Run already exists, please use another id.")
            if init and overwrite:
                clean_all(dst)
                make_dir(dst)
        else:
            make_dir(dst)

    def _build_source_destination(
        self, dst: str, src_type: str, key: Optional[str] = None
    ) -> str:
        """
        Return source path based on input source type.
        """
        filename = self._filenames[src_type]
        if src_type in self._cnt:
            filename = filename.format(self._cnt[src_type])
            self._cnt[src_type] += 1
        return get_path(dst, filename)

    def get_run_metadata_uri(self, exp_name: str, run_id: str) -> str:
        """
        Return the path of the metadata folder for the Run.
        """
        return get_path(self.metadata_uri, exp_name, run_id)
