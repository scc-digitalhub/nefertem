"""
PluginBuilder registry.
"""
from __future__ import annotations

import typing

from nefertem.plugins.inference.dummy import InferenceBuilderDummy
from nefertem.plugins.profiling.dummy import ProfileBuilderDummy
from nefertem.plugins.validation.dummy import ValidationBuilderDummy
from nefertem.utils.commons import DUMMY, INFER, PROFILE, VALIDATE

if typing.TYPE_CHECKING:
    from nefertem.plugins.plugin import PluginBuilder


class Registry(dict):
    """
    Registry of plugin builders.
    """

    def __init__(self) -> None:
        self[INFER] = {}
        self[PROFILE] = {}
        self[VALIDATE] = {}

    def register(self, operation: str, library: str, builder: PluginBuilder) -> None:
        """
        Register a plugin builder.
        """
        self[operation][library] = builder


plugin_registry = Registry()
plugin_registry.register(INFER, DUMMY, InferenceBuilderDummy)
plugin_registry.register(PROFILE, DUMMY, ProfileBuilderDummy)
plugin_registry.register(VALIDATE, DUMMY, ValidationBuilderDummy)


# frictionless imports
try:
    from nefertem.plugins.inference.frictionless.builder import InferenceBuilderFrictionless
    from nefertem.plugins.profiling.frictionless.builder import ProfileBuilderFrictionless
    from nefertem.plugins.validation.frictionless.builder import ValidationBuilderFrictionless

    plugin_registry.register(INFER, "frictionless", InferenceBuilderFrictionless)
    plugin_registry.register(PROFILE, "frictionless", ProfileBuilderFrictionless)
    plugin_registry.register(VALIDATE, "frictionless", ValidationBuilderFrictionless)

except ImportError:
    ...


# ydata_profiling imports
try:
    from nefertem.plugins.profiling.ydata_profiling.builder import ProfileBuilderYdataProfiling

    plugin_registry.register(PROFILE, "ydata_profiling", ProfileBuilderYdataProfiling)

except ImportError:
    ...

# duckdb imports
try:
    from nefertem.plugins.validation.duckdb.builder import ValidationBuilderDuckDB

    plugin_registry.register(VALIDATE, "duckdb", ValidationBuilderDuckDB)

except ImportError:
    ...


# sqlalchemy imports
try:
    from nefertem.plugins.validation.sqlalchemy.builder import ValidationBuilderSqlAlchemy

    plugin_registry.register(VALIDATE, "sqlalchemy", ValidationBuilderSqlAlchemy)

except ImportError:
    ...

# evidently imports
# try:
#     from nefertem.plugins.profiling.evidently import ProfileBuilderEvidently
#     from nefertem.plugins.validation.evidently import ValidationBuilderEvidently

#     plugin_registry.register(PROFILE, "evidently", ProfileBuilderEvidently)
#     plugin_registry.register(VALIDATE, "evidently", ValidationBuilderEvidently)

# except ImportError:
#     ...
