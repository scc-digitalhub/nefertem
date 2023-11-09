"""
RunInfo module.
"""
from __future__ import annotations

import typing

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
    resources : list[DataResource]
        List of input resources.
    run_config : RunConfig
        Run configuration.
    metadata_path : str
        URI that point to the metadata store.
    artifact_path : str
        URI that point to the artifact store.
    """

    def __init__(
        self,
        run_id: str,
        experiment_name: str,
        run_config: RunConfig,
        resources: list[DataResource],
        metadata_path: str | None = None,
        artifact_path: str | None = None,
    ) -> None:
        """
        Constructor.
        """

        # Run info
        self.run_id = run_id
        self.experiment_name = experiment_name

        # Execution info
        self.run_config = run_config
        self.run_libraries = None

        # Inputs
        self.resources = resources

        # Outputs
        self.nefertem_outputs = {"path": metadata_path, "files": []}
        self.artifact_outputs = {"path": artifact_path, "files": []}

        # Execution environment
        self.nefertem_version = NEFERTEM_VERSION
        self.execution_environment = Env().to_dict()

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
            "run_config": self.run_config.model_dump(exclude_none=True),
            "run_libraries": self.run_libraries,
            "resources": [i.model_dump(exclude_none=True) for i in self.resources],
            "nefertem_outputs": self.nefertem_outputs,
            "artifact_outputs": self.artifact_outputs,
            "nefertem_version": self.nefertem_version,
            "execution_environment": self.execution_environment,
            "status": self.status,
            "started": self.started,
            "finished": self.finished,
        }
