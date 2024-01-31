"""
Plugin builder factory module.
"""
from __future__ import annotations

import importlib
import typing

from nefertem_core.utils.exceptions import RunError

if typing.TYPE_CHECKING:
    from nefertem_core.plugins.builder import PluginBuilder
    from nefertem_core.run.config import RunConfig


def builder_factory(config: RunConfig, stores: dict) -> list:
    """
    Factory method that creates plugin builders.
    """
    builders = []
    for cfg in config.exec_config:
        ClsBuilder = _get_object(config.operation, cfg.framework)
        builders.append(ClsBuilder(stores, cfg.exec_args))
    return builders


def _get_object(operation: str, framework: str) -> PluginBuilder:
    """
    Get run handler class.

    Parameters
    ----------
    operation : str
        Operation to perform.
    framework : str
        Framework to use.

    Returns
    -------
    PluginBuilder
        Plugin builder class.
    """
    try:
        module = importlib.import_module(f"nefertem_{operation}_{framework}")
        return getattr(module, "Builder")
    except (ImportError, AttributeError):
        raise RunError(f"Builder of {framework} for {operation} not found.")
