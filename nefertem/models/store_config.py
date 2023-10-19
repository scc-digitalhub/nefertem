from typing import Optional

from pydantic import BaseModel
from typing_extensions import Literal

from nefertem.utils.commons import (
    STORE_AZURE,
    STORE_DUMMY,
    STORE_FTP,
    STORE_HTTP,
    STORE_LOCAL,
    STORE_ODBC,
    STORE_S3,
    STORE_SQL,
)


class StoreConfig(BaseModel):
    """
    Store configuration class.
    This object define the configuration of a Store passed to a
    Client in order to create a Store object to interact with
    various backend storages.
    """

    name: str
    """Store id."""

    type: Literal[STORE_LOCAL, STORE_HTTP, STORE_FTP, STORE_S3, STORE_AZURE, STORE_SQL, STORE_ODBC, STORE_DUMMY]
    """Store type to instantiate."""

    uri: str
    """Store URI."""

    title: Optional[str] = None
    """Human readable name for Store."""

    isDefault: Optional[bool] = False
    """Determine if a Store is the default one."""

    config: Optional[dict] = None
    """Dictionary containing the configuration for the backend."""
