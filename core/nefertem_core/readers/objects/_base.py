"""
DataReader module.
"""
from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any

if typing.TYPE_CHECKING:
    from nefertem_core.stores.input.objects._base import InputStore


class DataReader(metaclass=ABCMeta):
    """
    DataReader abstract class.

    This is the basic abstract class for the DataReaders.

    """

    def __init__(self, store: InputStore) -> None:
        self.store = store

    @abstractmethod
    def fetch_data(self, src: str) -> Any:
        """
        Fetch resources from backend.
        """
