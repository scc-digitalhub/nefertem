"""
Run configuration objects module.
"""
from pydantic import BaseModel, Field

from nefertem.utils.utils import build_uuid


class ExecConfig(BaseModel):
    """
    Generic configuration for run operation.
    """

    id: str = Field(default_factory=build_uuid)
    """UUID of operation."""

    framework: str
    """Library to use for performing an operation."""

    exec_args: dict | None = {}
    """Execution arguments to pass to plugins."""


class RunConfig(BaseModel):
    operation: str
    """Operation to perform."""

    exec_config: list[ExecConfig]
    """Execution configuration."""

    parallel: bool = False
    """Flag to execute operation in parallel."""

    num_worker: int = 10
    """Number of workers to execute operation in parallel, by default 10"""
