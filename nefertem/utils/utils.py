"""
Common generic utils.
"""
from __future__ import annotations

import functools
import operator
from datetime import datetime
from typing import Any
from uuid import uuid4


def build_uuid(uuid: str | None = None) -> str:
    """
    Create a uuid if not given

    Parameters
    ----------
    uuid : str
        UUID. Optional.

    Returns
    -------
    str
        The uuid.
    """
    if uuid is not None:
        return uuid
    return str(uuid4())


def flatten_list(list_of_list: list[list[Any]]) -> list[Any]:
    """
    Flatten a list of list.

    Parameters
    ----------
    list_of_list : list[list[Any]]
        The list of list to be flattened.
    """
    try:
        return functools.reduce(operator.iconcat, list_of_list)
    except TypeError:
        return []


def listify(obj: Any) -> list[Any]:
    """
    Convert an object to a list.

    Parameters
    ----------
    obj : Any
        The object to be converted.

    Returns
    -------
    list[Any]
        The list.
    """
    if not isinstance(obj, (list, tuple)):
        obj = [obj]
    return obj


def get_time() -> str:
    """
    Get current time with timezone info.

    Returns
    -------
    str
        ISO 8601 time with timezone info.
    """
    return datetime.now().astimezone().isoformat(timespec="milliseconds")
