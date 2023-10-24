"""
Client module.
Implementation of a Client object to interact with storages
and create runs.
"""
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from nefertem.run.run import Run

from nefertem.client.run_builder import RunBuilder
from nefertem.client.store_handler import StoreHandler
from nefertem.utils.commons import DEFAULT_EXPERIMENT


class Client:
    """
    Client class.

    The Client is a public interface that exposes methods to create
    runs and allows the user to add artifact stores to the pool of runs stores.
    The Client constructor build a StoreHandler to keep track of stores,
    both metadata and artifact, and a RunBuilder to create runs.
    All the parameters passed to the Client interface are passed to the
    StoreHandler.

    Parameters
    ----------
    metadata_store : str
        Path to the metadata store.
    store : list[dict]
        List of dict containing configuration for the artifact stores.
    tmp_dir : str
        Default local temporary folder where to store input data".

    Methods
    -------
    add_store
        Add a new store to the client internal registry.
    create_run
        Create a new run.

    """

    def __init__(
        self,
        metadata_store_path: str | None = None,
        stores: list[dict] | None = None,
        tmp_dir: str | None = None,
    ) -> None:
        self._store_handler = StoreHandler(metadata_store_path, stores, tmp_dir)
        self._run_builder = RunBuilder(self._store_handler)

    def add_store(self, config: dict) -> None:
        """
        Add a new store to the client internal registry.

        Parameters
        ----------
        config : dict
            Dictionary containing the configuration of the store.

        Returns
        -------
        None
        """
        self._store_handler.add_artifact_store(config)

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
        return self._run_builder.create_run(resources, run_config, experiment, run_id, overwrite)
