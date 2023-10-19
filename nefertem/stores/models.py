"""
Stores related models.
"""
from typing import Optional, Union

from pydantic import BaseModel


class StoreConfig(BaseModel):
    """
    Store configuration class.
    It defines the configuration settings for a Store like endpoints, credentials, etc.
    It is modelled on different kind of Store.
    """


class StoreParameters(BaseModel):
    """
    Store configuration class.
    This object define the configuration of a Store passed to a
    Client in order to create a Store object to interact with
    various backend storages.
    """

    name: str
    """Store id."""

    type: str
    """Store type to instantiate."""

    uri: str
    """Store URI."""

    title: Optional[str] = None
    """Human readable name for Store."""

    isDefault: Optional[bool] = False
    """Determine if a Store is the default one."""

    config: Optional[Union[dict, StoreConfig]] = None
    """Dictionary containing the configuration for the backend."""
