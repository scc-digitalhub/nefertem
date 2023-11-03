"""
RunBuilder module.
"""
from pydantic import ValidationError

from nefertem.metadata.run_info import RunInfo
from nefertem.resources.data_resource import DataResource
from nefertem.run.config import RunConfig
from nefertem.run.handler import RunHandler
from nefertem.run.run import Run
from nefertem.stores.builder import get_output_store
from nefertem.utils.commons import DEFAULT_EXPERIMENT
from nefertem.utils.exceptions import RunError
from nefertem.utils.utils import build_uuid


class RunBuilder:
    """
    RunBuilder object to initialize and create runs.

    Attributes
    ----------
    None

    Methods
    -------
    create_run(resources, run_config, experiment, run_id, overwrite)
        Create a new run.
    _validate_resources(resources)
        Validate data resources against model.
    _check_resources(resources)
        Check if resources already exist.
    _validate_run_config(run_config)
        Validate run config against model.
    """

    def create_run(
        self,
        resources: list[dict],
        run_config: dict,
        tmp_dir: str,
        experiment: str | None = DEFAULT_EXPERIMENT,
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
        experiment : str, optional
            Experiment name, by default DEFAULT_EXPERIMENT.
        run_id : str, optional
            Run id, by default None.
        overwrite : bool, optional
            If True, overwrite run metadata/artifact if it already exists.

        Returns
        -------
        Run
            Run object.
        """
        # Validate resources
        res = self._validate_resources(resources)
        self._check_resources(res)

        # Validate run config
        cfg = self._validate_run_config(run_config)

        # Get run id
        run_id = build_uuid(run_id)

        # Initialize run and get metadata and artifacts URI
        store = get_output_store()
        store.init_run(experiment, run_id, overwrite)
        run_md_uri = str(store.metadata_path)
        run_art_uri = str(store.artifact_path)

        # Create run
        run_handler = RunHandler(cfg)
        run_info = RunInfo(experiment, res, run_id, cfg, run_md_uri, run_art_uri)
        return Run(run_info, run_handler, tmp_dir, overwrite)

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
