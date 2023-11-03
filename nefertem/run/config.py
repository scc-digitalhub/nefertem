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

    library: str | None = "_dummy"
    """Library to use for performing an operation."""

    exec_args: dict | None = {}
    """Execution arguments to pass to plugins."""


class RunConfig(BaseModel):
    """
    Run configuration object.
    """

    validation: list[ExecConfig] | None = [ExecConfig()]
    """List of validation configuration."""

    inference: list[ExecConfig] | None = [ExecConfig()]
    """List of inference configuration."""

    profiling: list[ExecConfig] | None = [ExecConfig()]
    """List of profiling configuration."""
