"""
Run configuration objects module.
"""
from __future__ import annotations

from pydantic import BaseModel


class ExecConfig(BaseModel):
    """
    Generic configuration for run operation.
    """

    framework: str
    """Library to use for performing an operation."""

    exec_args: dict = {}
    """Execution arguments to pass to plugins."""


class RunConfig(BaseModel):
    """
    Run configuration.
    """

    operation: str
    """Operation to perform."""

    exec_config: list[ExecConfig]
    """Execution configuration."""

    parallel: bool = False
    """Flag to execute operation in parallel."""

    num_worker: int = 10
    """Number of workers to execute operation in parallel, by default 10"""
