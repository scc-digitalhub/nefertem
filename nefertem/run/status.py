"""
Run status module.
"""
from __future__ import annotations

from enum import Enum


class RunStatus(Enum):
    """
    Run status.

    Attributes
    ----------
    RUNNING : int
        Run is running.
    COMPLETED : int
        Run is completed.
    FAILED : int
        Run failed.
    """

    CREATED = "created"
    RUNNING = "running"
    FINISHED = "finished"
    INTERRUPTED = "interrupted"
    ERROR = "error"
