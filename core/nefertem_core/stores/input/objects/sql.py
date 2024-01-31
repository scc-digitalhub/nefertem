"""
Implementation of SQL artifact store.
"""
from __future__ import annotations

import re
from pathlib import Path

import polars as pl
from nefertem_core.stores.input.objects._base import InputStore, StoreConfig
from nefertem_core.utils.exceptions import StoreError


class SQLStoreConfig(StoreConfig):
    """
    SQL store configuration class.
    """

    driver: str
    """SQL driver."""

    host: str
    """SQL host."""

    port: int
    """SQL port."""

    user: str
    """SQL user."""

    password: str
    """SQL password."""

    database: str
    """SQL database name."""


class SQLInputStore(InputStore):
    """
    SQL artifact store object.

    Allows the client to interact with SQL based storages.

    """

    def __init__(self, name: str, store_type: str, temp_dir: str, config: SQLStoreConfig) -> None:
        """
        Constructor.
        """
        super().__init__(name, store_type, temp_dir)
        self.config = config

    def persist_artifact(self, *args) -> None:
        """
        Persist an artfact.

        Raises
        ------
        NotImplementedError
            This method is not implemented.
        """
        raise NotImplementedError("SQL store does not support persistence.")

    def fetch_file(self, src: str) -> Path:
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

        self.logger.info(f"Fetching resource {src} from store {self.name}")
        table = self._get_table_name(src)
        dst = self.temp_dir / f"{table}.parquet"
        filepath = self._download_table(table, dst)
        self._register_resource(key, filepath)
        return filepath

    def fetch_native(self, *args) -> str:
        """
        Fetch a native resource.

        Returns
        -------
        str
            The connection string.
        """
        return self._get_connection_string()

    ############################
    # Private helper methods
    ############################

    def _get_connection_string(self) -> str:
        """
        Get the connection string.

        Returns
        -------
        str
            The connection string.
        """
        return (
            f"{self.config.driver}//{self.config.user}:{self.config.password}@"
            f"{self.config.host}:{self.config.port}/{self.config.database}"
        )

    @staticmethod
    def _parse_path(path: str) -> dict:
        """
        Parse the path and return the components.

        Parameters
        ----------
        path : str
            The path.

        Returns
        -------
        dict
            A dictionary containing the components of the path.
        """
        pattern = r"^sql://(?P<database>.+)/(?P<table>.+)$"
        match = re.match(pattern, path)
        if match is None:
            raise ValueError("Invalid SQL path. Must be sql://<database>/<table>")
        return match.groupdict()

    def _get_table_name(self, uri: str) -> str:
        """
        Get the name of the table from the URI.

        Parameters
        ----------
        uri : str
            The URI.

        Returns
        -------
        str
            The name of the table
        """
        return str(self._parse_path(uri).get("table"))

    ############################
    # Private I/O methods
    ############################

    def _execute_query(self, query: str) -> pl.DataFrame:
        """
        Execute a query.

        Parameters
        ----------
        query : str
            The query.

        Returns
        -------
        list
            The query results.
        """
        pl.read_database(query, self._get_connection_string(), engine="adbc")

    def _download_table(self, table: str, dst: str) -> Path:
        """
        Download a table from SQL based storage.

        Parameters
        ----------
        table : str
            The origin table.
        dst : str
            The destination path.

        Returns
        -------
        Path
            The destination of the file on local filesystem.
        """
        self._verify_table(table)
        query = f"select * from {table}"
        self._execute_query(query).write_parquet(dst)
        return Path(dst)

    def _verify_table(self, table: str) -> None:
        """
        Verify if table exists.

        Parameters
        ----------
        table : str
            Table name.

        Returns
        -------
        None
        """
        query = """
        SELECT TABLE_NAME as table
        FROM INFORMATION_SCHEMA.TABLES
        """
        res = self._execute_query(query)
        if table not in res.to_series().to_list():
            raise StoreError(f"Table {table} not in db.")
