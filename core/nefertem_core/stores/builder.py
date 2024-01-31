"""
StoreBuilder module.
"""
from __future__ import annotations

import typing

from nefertem_core.stores.input.objects._base import StoreParameters
from nefertem_core.stores.input.registry import input_store_registry
from nefertem_core.stores.kinds import StoreKinds
from nefertem_core.stores.output.registry import mdstore_registry
from nefertem_core.utils.commons import DUMMY
from nefertem_core.utils.exceptions import StoreError
from pydantic import ValidationError

if typing.TYPE_CHECKING:
    from nefertem_core.stores.input.objects._base import InputStore, StoreConfig
    from nefertem_core.stores.output.objects._base import OutputStore


class StoreBuilder:
    """
    StoreBuilder class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self._stores: dict = {}
        self._output_store: OutputStore | None = None

    def build_output_store(self, path: str | None = None) -> None:
        """
        Method to create an output stores. If the path is None, the method creates a dummy
        output store.

        Parameters
        ----------
        path: str
            Output path.

        Returns
        -------
        None
        """
        if path is None:
            return mdstore_registry[StoreKinds.DUMMY.value](DUMMY)
        if self._output_store is None:
            self._output_store = mdstore_registry[StoreKinds.LOCAL.value](path)

    def build_input_store(self, temp_dir: str, config: dict | None = None) -> None:
        """
        Method to create an input stores.

        Parameters
        ----------
        config : dict
            Store configuration.
        temp_dir: str
            Temporary directory.

        Returns
        -------
        None
        """
        params = self._parse_parameters(temp_dir, config)
        if params["name"] in self._stores:
            raise StoreError(f"Store {params['name']} already exists.")
        self._stores[params["name"]] = self._get_store(params)

    def _parse_parameters(self, temp_dir: str, config: dict | None = None) -> dict:
        """
        Parse store parameters.

        Parameters
        ----------
        temp_dir : str
            Temporary directory.
        config : dict
            Store configuration.

        Returns
        -------
        dict
            Store parameters.
        """
        cfg: StoreParameters = self._validate_parameters(config)
        return {
            "name": cfg.name,
            "store_type": cfg.store_type,
            "temp_dir": temp_dir,
            "config": self._validate_config(cfg.store_type, cfg.config),
        }

    @staticmethod
    def _validate_parameters(config: dict | None = None) -> StoreParameters:
        """
        Validate store parameters against a pydantic model.

        Parameters
        ----------
        config : dict
            Store configuration.

        Returns
        -------
        StoreParameters
            Store parameters.

        Raises
        ------
        StoreError
            If the store configuration is invalid.
        """
        try:
            return StoreParameters(**config)
        except TypeError:  # If config is None
            return StoreParameters(StoreKinds.DUMMY.value, DUMMY)
        except ValidationError:
            raise StoreError("Invalid store configuration.")

    @staticmethod
    def _validate_config(store_type: str, config: dict | None = None) -> StoreConfig:
        """
        Validate store configuration.

        Parameters
        ----------
        store_type : str
            Store type.
        config : dict
            Store configuration.

        Returns
        -------
        dict
            Store configuration.

        Raises
        ------
        StoreError
            If the store configuration is invalid.
        """
        try:
            return input_store_registry[store_type]["model"](**config)
        except (ValidationError, TypeError):
            raise StoreError("Invalid store configuration.")
        except KeyError:
            raise StoreError("Invalid store type.")

    @staticmethod
    def _get_store(params: dict) -> InputStore:
        """
        Validate store configuration.

        Parameters
        ----------
        params : dict
            Store configuration.

        Returns
        -------
        dict
            Store configuration.

        Raises
        ------
        StoreError
            If the store configuration is invalid.
        """
        try:
            store_type = params["store_type"]
            return input_store_registry[store_type]["store"](**params)
        except TypeError:
            raise StoreError("Something went wrong.")
        except KeyError:
            raise StoreError("Invalid store type.")

    def get_input_store(self, name: str) -> InputStore:
        """
        Get store by name.

        Parameters
        ----------
        name : str
            Store name.

        Returns
        -------
        InputStore
            Artifact store object.

        Raises
        ------
        StoreError
            If the store is not found.
        """
        store = self._stores.get(name)
        if store is None:
            raise StoreError(f"Store {name} not found.")
        return store

    def get_all_input_stores(self) -> list[InputStore]:
        """
        Get all stores.

        Returns
        -------
        list
            List of artifact store objects.
        """
        stores = list(self._stores.values())
        if not stores:
            raise StoreError("No stores found.")
        return stores

    def get_output_store(self) -> OutputStore:
        """
        Get output store.

        Returns
        -------
        OutputStore
            Metadata store object.

        Raises
        ------
        StoreError
            If the store is not found.
        """
        if self._output_store is None:
            raise StoreError("Output store not found.")
        return self._output_store


store_builder = StoreBuilder()


def get_input_store(name: str) -> InputStore:
    """
    Wrapper for StoreBuilder.get_input_store.

    Parameters
    ----------
    name : str
        Store name.

    Returns
    -------
    InputStore
        Artifact store object.
    """
    return store_builder.get_input_store(name)


def get_all_input_stores() -> list[InputStore]:
    """
    Wrapper for StoreBuilder.get_all_input_stores.

    Returns
    -------
    list
        List of artifact store objects.
    """
    return store_builder.get_all_input_stores()


def get_output_store() -> OutputStore:
    """
    Wrapper for StoreBuilder.get_output_store.

    Returns
    -------
    OutputStore
        Metadata store object.
    """
    return store_builder.get_output_store()
