"""
RunBuilder module.
"""
from __future__ import annotations

import typing

from pydantic import ValidationError

from nefertem.metadata.run_info import RunInfo
from nefertem.resources.data_resource import DataResource
from nefertem.run.run import Run
from nefertem.run.run_config import RunConfig
from nefertem.run.run_handler import RunHandler
from nefertem.utils.commons import DEFAULT_EXPERIMENT
from nefertem.utils.exceptions import RunError
from nefertem.utils.utils import build_uuid

if typing.TYPE_CHECKING:
    from nefertem.client.store_handler import StoreHandler


class RunBuilder:
    """
    RunBuilder object to initialize and create runs.

    """

    def __init__(self, store_handler: StoreHandler) -> None:
        """
        The RunBuilder recieves a store handler to get stores.
        """
        self._store_handler = store_handler

    def create_run(
        self,
        resources: list[dict],
        run_config: dict,
        experiment: str | None = DEFAULT_EXPERIMENT,
        run_id: str | None = None,
        overwrite: bool = False,
    ) -> Run:
        """
        Create a new run.
        """
        # Validate resources
        res = self._validate_resources(resources)
        self._check_resources(res)

        # Validate run config
        cfg = self._validate_run_config(run_config)

        # Get run id
        run_id = build_uuid(run_id)

        # Initialize run and get metadata and artifacts URI
        self._init_run(experiment, run_id, overwrite)
        run_md_uri = self._get_md_uri(experiment, run_id)
        run_art_uri = self._get_art_uri(experiment, run_id)

        # Create run
        run_handler = RunHandler(run_config, self._store_handler)
        run_info = RunInfo(experiment, res, run_id, cfg, run_md_uri, run_art_uri)
        return Run(run_info, run_handler, overwrite)

    def _init_run(self, exp_name: str, run_id: str, overwrite: bool) -> None:
        """
        Initialize run with metadata store.

        Parameters
        ----------
        exp_name : str
            Experiment name.
        run_id : str
            Run id.
        overwrite : bool
            Overwrite run if already exists.

        Returns
        -------
        None
        """
        self._store_handler.get_md_store().init_run(exp_name, run_id, overwrite)

    def _get_md_uri(self, exp_name: str, run_id: str) -> str:
        """
        Get the metadata URI store location.

        Parameters
        ----------
        exp_name : str
            Experiment name.
        run_id : str
            Run id.

        Returns
        -------
        str
            Metadata URI.
        """
        return self._store_handler.get_md_store().get_run_path(exp_name, run_id)

    def _get_art_uri(self, exp_name: str, run_id: str) -> str:
        """
        Get the artifacts URI store location. It uses the default store.

        Parameters
        ----------
        exp_name : str
            Experiment name.
        run_id : str
            Run id.

        Returns
        -------
        str
            Artifacts URI.
        """
        return self._store_handler.get_def_store().get_run_path(exp_name, run_id)

    @staticmethod
    def _validate_resources(resources: list[dict]) -> list[DataResource]:
        """
        Validate data resources against model.

        Parameters
        ----------
        resources : list[dict]
            List of resources to validate.

        Returns
        -------
        list[DataResource]
            List of validated resources.

        Raises
        ------
        RunError
            If a resource does not match the model.
        """
        try:
            return [DataResource(**res) for res in resources]
        except (TypeError, ValidationError):
            raise RunError("Invalid resource!")

    @staticmethod
    def _check_resources(resources: list[DataResource]) -> None:
        """
        Check if resources already exist.

        Parameters
        ----------
        resources : list[DataResource]
            List of resources to check.

        Returns
        -------
        None

        Raises
        ------
        RunError
            If a resource already exists.
        """
        exists = []
        for res in resources:
            if res.name in exists:
                raise RunError(f"Resource with name {res.name} already exists!")
            exists.append(res.name)

    def _validate_run_config(self, run_config: dict) -> RunConfig:
        """
        Validate run config against model.

        Parameters
        ----------
        run_config : dict
            Run config to validate.

        Returns
        -------
        RunConfig
            Validated run config.

        Raises
        ------
        RunError
            If run config does not match the model.
        """
        try:
            return RunConfig(**run_config)
        except (TypeError, ValidationError):
            raise RunError("Invalid run config!")
