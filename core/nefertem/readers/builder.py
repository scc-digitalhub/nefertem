from __future__ import annotations

import importlib
import typing

from nefertem.readers.registry import reader_registry

if typing.TYPE_CHECKING:
    from nefertem.readers.objects._base import DataReader
    from nefertem.stores.input.objects._base import InputStore


def build_reader(reader_type: str, store: InputStore, **kwargs) -> DataReader:
    """
    Reader builder.

    Parameters
    ----------
    reader_type: str
        Reader type.
    store: InputStore
        Store to read from.
    kwargs: dict
        Reader kwargs.

    Returns
    -------
    DataReader
        Reader instance.
    """
    try:
        module = importlib.import_module(reader_registry[reader_type][0])
        reader = getattr(module, reader_registry[reader_type][1])
        return reader(store, **kwargs)
    except (KeyError, ModuleNotFoundError, AttributeError, ImportError):
        raise KeyError(f"Reader {reader_type} not found. Check installed libraries.")
