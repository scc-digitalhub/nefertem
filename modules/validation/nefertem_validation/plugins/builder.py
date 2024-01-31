from __future__ import annotations

import typing
from abc import abstractmethod

from nefertem_core.plugins.builder import PluginBuilder

if typing.TYPE_CHECKING:
    from nefertem_validation.plugins.constraint import Constraint


class ValidationPluginBuilder(PluginBuilder):
    """
    Validation plugin builder.
    """

    @staticmethod
    @abstractmethod
    def _filter_constraints(constraints: list[dict]) -> list[Constraint]:
        """
        Filter constraints by library.
        """
