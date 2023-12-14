"""
Nefertem Inference Plugin Utils.
"""
from __future__ import annotations


def get_fields(name: str = None, type_: str = None) -> dict:
    """
    Return a common field structure.

    Parameters
    ----------
    name : str
        Field name.
    type_ : str
        Field type.

    Returns
    -------
    dict
        Field structure.
    """
    if name is None:
        name = "unknown"
    if type_ is None:
        type_ = "unknown"
    return {"name": name, "type": type_}
