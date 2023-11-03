"""
Implementation of REST artifact store.
"""
import requests

from nefertem.stores.input.objects.base import InputStore, StoreConfig
from nefertem.utils.file_utils import get_path
from nefertem.utils.uri_utils import get_name_from_uri


class RemoteStoreConfig(StoreConfig):
    """
    HTTP store configuration class.
    """

    user: str | None = None
    """User name."""

    password: str | None = None
    """Password."""

    token: str | None = None
    """Bearer token."""


class RemoteInputStore(InputStore):
    """
    Rest artifact store object.

    Allows the client to interact with remote HTTP store.

    """

    def __init__(self, name: str, uri: str, store_type: str, temp_dir: str, config: RemoteStoreConfig) -> None:
        """
        Constructor.
        """
        super().__init__(name, uri, store_type, temp_dir)
        self.config = config

    ############################
    # Read methods
    ############################

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
        key = f"{src}_file"
        cached = self._get_resource(key)
        if cached is not None:
            return cached

        if src.split(".")[-1] not in ["csv", "parquet"]:
            raise ValueError("Only csv and parquet files are supported for download.")

        self.logger.info(f"Fetching resource {src} from store {self.name}")
        dst = get_path(self.temp_dir, get_name_from_uri(src))
        filepath = self._download_file(src, dst)
        self._register_resource(key, filepath)
        return filepath

    def fetch_native(self, src: str) -> str:
        """
        Return a native format path for a resource.

        Parameters
        ----------
        src : str
            The URL of the resource.

        Returns
        -------
        str
            The URL of the resource.
        """
        return src

    ############################
    # Helper methods
    ############################

    @staticmethod
    def _check_head(src) -> None:
        """
        Check if the source exists.

        Parameters
        ----------
        src : str
            The source location.

        Returns
        -------
        None

        Raises
        ------
        HTTPError
            If an error occurs while checking the source.
        """
        r = requests.head(src, timeout=60)
        r.raise_for_status()

    def _download_file(self, url: str, dst: str) -> str:
        """
        Method to download a file from a given url.

        Parameters
        ----------
        url : str
            The url of the file to download.
        dst : str
            The destination of the file.

        Returns
        -------
        str
            The path of the downloaded file.
        """
        self._check_head(url)
        kwargs = self._get_auth()
        with requests.get(url, stream=True, timeout=60, **kwargs) as r:
            r.raise_for_status()
            with open(dst, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return dst

    def _get_auth(self) -> dict:
        """
        Get authentication parameters from the config.

        Returns
        -------
        dict
            The authentication parameters.
        """
        if self.config.auth == "basic":
            return {"auth": (self.config.user, self.config.password)}
        if self.config.auth == "oauth":
            return {"headers": {"Authorization": f"Bearer {self.config.token}"}}
        return {}
