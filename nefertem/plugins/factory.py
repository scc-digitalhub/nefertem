"""
Plugin builder factory module.
"""
from __future__ import annotations

import typing

from nefertem.plugins.registry import plugin_registry

if typing.TYPE_CHECKING:
    from nefertem.run.config import ExecConfig


def builder_factory(config: list[ExecConfig], typology: str, stores: dict) -> list:
    """
    Factory method that creates plugin builders.
    """
    builders = []
    for cfg in config:
        try:
            builders.append(plugin_registry[typology][cfg.library](stores, cfg.exec_args))
        except KeyError:
            raise NotImplementedError
    return builders
