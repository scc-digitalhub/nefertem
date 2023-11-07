"""
Client module.
"""
from __future__ import annotations

import typing

from nefertem.run.builder import run_builder
from nefertem.stores.builder import store_builder
from nefertem.utils.commons import DEFAULT_DIRECTORY, DEFAULT_EXPERIMENT

if typing.TYPE_CHECKING:
    from nefertem.run.run import Run


class Client:
    """
    The Client is a public interface that exposes methods to create runs and allows
    the user to add input stores to the pool of runs stores.

    Parameters
    ----------
    path : str
        Path where to store metadata and artifacts.
    stores : list[dict]
        List of dict containing configuration for the input stores.
    tmp_dir : str
        Default local temporary folder where to store input data.

    Methods
    -------
    add_store
        Add a new store to the client internal registry.
    create_run
        Create a new run.
    """

    def __init__(
        self,
        path: str | None = None,
        stores: list[dict] | None = None,
        tmp_dir: str | None = None,
    ) -> None:
        self._tmp_dir = tmp_dir if tmp_dir is not None else DEFAULT_DIRECTORY
        self._setup_stores(path, stores)

    def _setup_stores(self, path: str | None = None, configs: list[dict] | None = None) -> None:
        """
        Build stores according to configurations provided by user and register
        them into the store registry.

        Parameters
        ----------
        path : str
            Path where to store metadata and artifacts.
        configs : list[dict]
            List of dict containing configuration for the input stores.
        """

        # Build output store
        store_builder.build_output_store(path)

        # Build input stores
        try:
            for cfg in configs:
                store_builder.build_input_store(self._tmp_dir, cfg)
        except TypeError:
            pass

    def add_store(self, config: dict) -> None:
        """
        Add a new store to the store registry.

        Parameters
        ----------
        config : dict
            Dictionary containing the configuration of the store.

        Returns
        -------
        None
        """
        store_builder.build_input_store(self._tmp_dir, config)

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

        Parameters
        ----------
        resources : list[dict]
            List of DataResource objects.
        run_config : dict
            RunConfig object.
        experiment : str
            Name of the experiment. An experiment is a logical unit for ordering the runs execution,
            by default "experiment".
        run_id : str
            Optional string parameter for user defined run id.
        overwrite : bool
            If True, the run metadata/artifact can be overwritten by a run with the same id.

        Returns
        -------
        Run
            Run object.
        """
        return run_builder.create_run(resources, run_config, self._tmp_dir, experiment, run_id, overwrite)
