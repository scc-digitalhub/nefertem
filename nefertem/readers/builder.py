from __future__ import annotations

import importlib
import typing

from nefertem.readers.registry import REGISTRY

if typing.TYPE_CHECKING:
    from nefertem.readers.base import DataReader
    from nefertem.stores.artifact.objects.base import ArtifactStore


def build_reader(reader_type: str, store: ArtifactStore, **kwargs) -> DataReader:
    """
    Reader builder.

    Parameters
    ----------
    reader_type: str
        Reader type.
    store: ArtifactStore
        Store to read from.
    kwargs: dict
        Reader kwargs.

    Returns
    -------
    DataReader
        Reader instance.
    """
    try:
        module = importlib.import_module(REGISTRY[reader_type][0])
        reader = getattr(module, REGISTRY[reader_type][1])
        return reader(store, **kwargs)
    except (KeyError, ModuleNotFoundError, AttributeError, ImportError):
        raise KeyError(f"Reader {reader_type} not found. Check installed libraries.")
