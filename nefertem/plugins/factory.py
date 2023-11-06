"""
Plugin builder factory module.
"""
from __future__ import annotations

import importlib
import typing

from nefertem.utils.exceptions import RunError

if typing.TYPE_CHECKING:
    from nefertem.run.config import RunConfig


def builder_factory(config: RunConfig, stores: dict) -> list:
    """
    Factory method that creates plugin builders.
    """
    builders = []
    for cfg in config.exec_config:
        try:
            ClsBuilder = _get_object(config.operation, cfg.library)
            builders.append(ClsBuilder(stores, cfg.exec_args))
        except KeyError:
            raise NotImplementedError
    return builders


def _get_object(operation: str, obj: str) -> type:
    """
    Get run handler class.

    Parameters
    ----------
    operation : str
        Operation to perform.
    obj : str
        Object type to get.

    Returns
    -------
    type
        Run handler class.

    Raises
    ------
    RunError
        If run handler class does not exist.
    """
    try:
        module = importlib.import_module(f"nefertem_{operation}.config")
        plugins = getattr(module, "PLUGINS")
        submodule = importlib.import_module(plugins[obj][0])
        return getattr(submodule, plugins[obj][1])
    except AttributeError:
        raise RunError(f"Run handler for operation {operation} does not exist!")
