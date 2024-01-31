"""
Implementation of REST artifact store.
"""
from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urlparse

import requests
from nefertem_core.stores.input.objects._base import InputStore, StoreConfig


class RemoteStoreConfig(StoreConfig):
    """
    HTTP store configuration class.
    """

    auth: str = None
    """Authentication type."""

    user: str = None
    """User name."""

    password: str = None
    """Password."""

    token: str = None
    """Bearer token."""


class RemoteInputStore(InputStore):
    """
    Rest artifact store object.

    Allows the client to interact with remote HTTP store.

    """

    def __init__(self, name: str, store_type: str, temp_dir: str, config: RemoteStoreConfig) -> None:
        """
        Constructor.
        """
        super().__init__(name, store_type, temp_dir)
        self.config = config

    ############################
    # Read methods
    ############################

    def fetch_file(self, src: str) -> Path:
        """
        Return the path where a resource it is stored.

        Parameters
        ----------
        src : str
            The name of the file.

        Returns
        -------
        Path
            The location of the requested file.
        """
        key = f"{src}_file"
        cached = self._get_resource(key)
        if cached is not None:
            return cached

        self.logger.info(f"Fetching resource {src} from store {self.name}")
        dst = self.temp_dir / self._get_filename(src)
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

    def _download_file(self, url: str, dst: str) -> Path:
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
        Path
            The path of the downloaded file.
        """
        self._check_head(url)
        kwargs = self._get_auth()
        with requests.get(url, stream=True, timeout=60, **kwargs) as r:
            r.raise_for_status()
            with open(dst, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return Path(dst)

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

    @staticmethod
    def _get_filename(url: str) -> str:
        """
        Get the filename from a url.

        Parameters
        ----------
        url : str
            The url of the file.

        Returns
        -------
        str
            The filename.

        Raises
        ------
        ValueError
            If the file extension is not supported.
        """
        filename = Path(unquote(urlparse(url).path)).name
        if filename.split(".")[-1] not in ["csv", "parquet"]:
            raise ValueError("Only csv and parquet files are supported for download.")
        return filename
