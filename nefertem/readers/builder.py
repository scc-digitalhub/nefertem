from nefertem.readers.base import DataReader
from nefertem.readers.registry import REGISTRY
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
        return REGISTRY[reader_type](store, **kwargs)
    except KeyError:
        raise KeyError(f"Reader {reader_type} not found. Check installed libraries.")
