from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from nefertem.utils.commons import LIBRARY_DUMMY


class ExecConfig(BaseModel):
    """
    Generic configuration for run operation.
    """

    id: str = Field(default_factory=uuid4)
    """UUID of operation."""

    library: Optional[str] = LIBRARY_DUMMY
    """Library to use for performing an operation."""

    execArgs: Optional[dict] = {}
    """Execution arguments to pass to plugins."""


class RunConfig(BaseModel):
    """
    Run configuration object.
    """

    validation: Optional[List[ExecConfig]] = [ExecConfig()]
    """List of validation configuration."""

    inference: Optional[List[ExecConfig]] = [ExecConfig()]
    """List of inference configuration."""

    profiling: Optional[List[ExecConfig]] = [ExecConfig()]
    """List of profiling configuration."""
