"""
Utils functions for data reader.
"""
from __future__ import annotations

import typing

from nefertem.readers.registry import REGISTRY

if typing.TYPE_CHECKING:
    from nefertem.readers.base.base import DataReader
    from nefertem.stores.artifact.objects.base import ArtifactStore


def get_reader(reader_type: str) -> DataReader:
    """
    Registry getter.
    """
    try:
        return REGISTRY[reader_type]
    except KeyError:
        raise KeyError(f"Reader {reader_type} not found. Check installed libraries.")


def build_reader(
    reader_type: str,
    store: ArtifactStore,
    **kwargs,
) -> DataReader:
    """
    Reader builder.
    """
    return get_reader(reader_type)(store, **kwargs)
