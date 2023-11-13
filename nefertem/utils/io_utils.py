"""
Common IO utils.
"""
from __future__ import annotations

import json
from io import BytesIO, StringIO
from pathlib import Path


def write_bytesio(src: str) -> BytesIO:
    """
    Write string in ByteStream BytesIO.

    Parameters
    ----------
    src : str
        The source string to be wrapped.

    Returns
    -------
    BytesIO
        The wrapped object.
    """
    bytesio = BytesIO()
    bytesio.write(src.encode())
    bytesio.seek(0)
    return bytesio


def write_bytes(byt: bytes, path: Path) -> None:
    """
    Write bytes on a file.

    Parameters
    ----------
    byt : bytes
        The bytes to be written.
    path : Path
        The path to the file.

    Returns
    -------
    None
    """
    path.write_bytes(byt)


def write_object(buff: BytesIO | StringIO, path: Path) -> None:
    """
    Write a buffer as file.

    Parameters
    ----------
    buff : IO
        The buffer to be written.
    path : Path
        The path to the file.

    Returns
    -------
    None
    """
    buff.seek(0)
    if isinstance(buff, BytesIO):
        path.write_bytes(buff.read())
    else:
        path.write_text(buff.read(), encoding="utf-8")


def write_json(data: dict, path: Path) -> None:
    """
    Store JSON file.

    Parameters
    ----------
    data : dict
        The data to be stored.
    path : Path
        The path to the file.

    Returns
    -------
    None
    """
    path.write_text(json.dumps(data, indent=4), encoding="utf-8")
