"""
Plugin utils module.
"""
from __future__ import annotations

import time
from collections import namedtuple
from enum import Enum
from typing import Any, Callable

RenderTuple = namedtuple("RenderTuple", ("object", "filename"))


class ExecutionStatus(Enum):
    """
    Enum class for execution status.
    """

    INIT = "created"
    RUNNING = "executing"
    FINISHED = "finished"
    ERROR = "error"


class ResultType(Enum):
    """
    Enum class for result type.
    """

    FRAMEWORK = "framework"
    NEFERTEM = "nefertem"
    RENDERED = "rendered"
    LIBRARY = "library"


class Result:
    """
    Simple class to aggregate result of plugin operation.
    """

    def __init__(
        self,
        status: str | None = ExecutionStatus.INIT.value,
        duration: float | None = None,
        errors: tuple | None = None,
        artifact: Any | None = None,
    ) -> None:
        """
        Constructor.
        """
        self.status = status
        self.duration = duration
        self.errors = errors
        self.artifact = artifact

    def to_dict(self) -> dict:
        """
        Return result as dict.

        Returns
        -------
        dict
            Result as dict.
        """
        return {
            "status": self.status,
            "duration": self.duration,
            "errors": self.errors,
            "artifact": self.artifact,
        }


def exec_decorator(fnc: Callable) -> Result:
    """
    Decorator that keeps track of execution time and status.
    """

    def wrapper(*args, **kwargs) -> Result:
        """
        Wrapper.
        """
        data = Result()
        start = time.perf_counter()
        data.status = ExecutionStatus.RUNNING.value
        try:
            data.artifact = fnc(*args, **kwargs)
            data.status = ExecutionStatus.FINISHED.value
        except Exception as exc:
            data.errors = exc.args
            data.status = ExecutionStatus.ERROR.value
        data.duration = round(time.perf_counter() - start, 2)
        return data

    return wrapper
