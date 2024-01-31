"""
RunBuilder module.
"""
from __future__ import annotations

import importlib
import typing

from nefertem_core.resources.data_resource import DataResource
from nefertem_core.run.config import RunConfig
from nefertem_core.run.handler import RunHandler
from nefertem_core.run.run_info import RunInfo
from nefertem_core.stores.builder import get_output_store
from nefertem_core.utils.exceptions import RunError
from nefertem_core.utils.utils import build_uuid
from pydantic import ValidationError

if typing.TYPE_CHECKING:
    from nefertem_core.run.run import Run


class RunBuilder:
    """
    RunBuilder object to initialize and create runs.

    Attributes
    ----------
    None

    Methods
    -------
    create_run
        Create a new run.
    """

    def create_run(
        self,
        resources: list[dict],
        run_config: dict,
        tmp_dir: str,
        experiment_name: str | None = None,
        run_id: str | None = None,
        overwrite: bool = False,
    ) -> Run:
        """
        Create a new run.

        Parameters
        ----------
        resources : list[dict]
            List of resources to add to the run.
        run_config : dict
            Run configuration.
        tmp_dir : str
            Temporary directory to store artifacts.
        experiment_name : str
            Experiment name.
        run_id : str
            Run id, by default None.
        overwrite : bool
            If True, overwrite run if already exists.

        Returns
        -------
        Run
            Run object.
        """
        if experiment_name is None:
            experiment_name = "default"

        # Validate resources
        res = self._validate_resources(resources)
        self._check_resources(res)

        # Validate run config
        cfg = self._validate_run_config(run_config)

        # Get run id
        run_id = build_uuid(run_id)

        # Initialize run and get run path
        store = get_output_store()
        store.init_run(experiment_name, run_id, overwrite)
        run_path = store.get_run_path()

        # Get run specific operations
        ClsRun: Run = self._get_run_object(cfg.operation)

        # Create run
        run_handler = RunHandler(cfg)
        run_info = RunInfo(
            run_id=run_id,
            experiment_name=experiment_name,
            run_path=run_path,
            run_config=cfg,
            resources=res,
        )
        return ClsRun(run_info, run_handler, tmp_dir)

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

    def _get_run_object(self, operation: str) -> Run:
        """
        Get run class.

        Parameters
        ----------
        operation : str
            Operation to perform.

        Returns
        -------
        Run
            Run specific class.

        Raises
        ------
        RunError
            If run class does not exist.
        """
        try:
            module = importlib.import_module(f"nefertem_{operation}.run.run")
            run: Run = getattr(module, f"Run{operation.capitalize()}")
            return run
        except AttributeError:
            raise RunError(f"Run for operation {operation} does not exist!")


run_builder = RunBuilder()
