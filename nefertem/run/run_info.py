"""
RunInfo module.
"""
from __future__ import annotations

import typing
from pathlib import Path

from nefertem.metadata.env import Env
from nefertem.run.status import RunStatus
from nefertem.utils.commons import NEFERTEM_VERSION

if typing.TYPE_CHECKING:
    from nefertem.resources.data_resource import DataResource
    from nefertem.run.config import RunConfig


class RunInfo:
    """
    Run's metadata.

    Attributes
    ----------
    run_id : str
        Run id.
    experiment_name : str
        Id of the experiment.
    run_path : Path
        Path where to store run's metadata and artifacts.
    resources : list[DataResource]
        List of input resources.
    run_config : RunConfig
        Run configuration.
    """

    def __init__(
        self,
        run_id: str,
        experiment_name: str,
        run_path: Path,
        run_config: RunConfig,
        resources: list[DataResource],
    ) -> None:
        """
        Constructor.
        """

        # Run info
        self.run_id = run_id
        self.experiment_name = experiment_name

        # Execution info
        self.run_path = run_path
        self.run_config = run_config
        self.run_libraries = None

        # Inputs
        self.resources = resources

        # Outputs
        self.output_files = []

        # Execution environment
        self.nefertem_version = NEFERTEM_VERSION
        self.execution_environment = Env()

        # Status
        self.status = RunStatus.CREATED.value

        # Timings
        self.started = None
        self.finished = None

    def to_dict(self) -> dict:
        """
        Override the method to_dict of the Metadata class.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        return {
            "run_id": self.run_id,
            "experiment_name": self.experiment_name,
            "run_path": str(self.run_path),
            "run_config": self.run_config.dict(exclude_none=True),
            "run_libraries": self.run_libraries,
            "resources": [i.dict(exclude_none=True) for i in self.resources],
            "output_files": [str(i) for i in self.output_files],
            "nefertem_version": self.nefertem_version,
            "execution_environment": self.execution_environment.to_dict(),
            "status": self.status,
            "started": self.started,
            "finished": self.finished,
        }
