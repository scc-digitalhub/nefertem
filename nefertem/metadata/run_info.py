"""
RunInfo module.
Implementation of the basic Run's metadata.
"""
from __future__ import annotations

import typing

from nefertem.metadata.metadata import Metadata
from nefertem.utils.utils import get_time

if typing.TYPE_CHECKING:
    from nefertem.resources.data_resource import DataResource
    from nefertem.run.run_config import RunConfig


class RunInfo(Metadata):
    """
    Run's metadata.

    Attributes
    ----------
    experiment_name : str
        Id of the experiment.
    run_id : str
        Run id.
    run_type: str
        Run typology.
    run_meta_path : str
        URI that point to the metadata store.
    run_art_path : str
        URI that point to the artifact store.
    resources_uri : str
        URI that point to the resource.
    """

    def __init__(
        self,
        experiment_name: str,
        resources: list[DataResource],
        run_id: str,
        run_config: RunConfig,
        run_meta_path: str | None = None,
        run_art_path: str | None = None,
    ) -> None:
        self.experiment_name = experiment_name
        self.run_id = run_id
        self.run_config = run_config
        self.run_libraries = None
        self.run_meta_path = run_meta_path
        self.run_art_path = run_art_path

        self.resources = resources

        self.created = get_time()
        self.begin_status = None
        self.started = None
        self.end_status = None
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
            "experiment_name": self.experiment_name,
            "run_id": self.run_id,
            "run_config": self.run_config.dict(exclude_none=True),
            "run_libraries": self.run_libraries,
            "run_meta_path": self.run_meta_path,
            "run_art_path": self.run_art_path,
            "resources": [i.dict(exclude_none=True) for i in self.resources],
            "created": self.created,
            "begin_status": self.begin_status,
            "started": self.started,
            "end_status": self.end_status,
            "finished": self.finished,
        }
