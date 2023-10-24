"""
StoreBuilder module.
"""
from __future__ import annotations

import typing

from pydantic import ValidationError

from nefertem.stores.artifact.objects.base import StoreParameters
from nefertem.stores.artifact.registry import artstore_registry
from nefertem.stores.kinds import StoreKinds
from nefertem.stores.metadata.registry import mdstore_registry
from nefertem.utils.commons import DUMMY
from nefertem.utils.exceptions import StoreError
from nefertem.utils.file_utils import get_absolute_path, get_path
from nefertem.utils.uri_utils import map_uri_scheme, rebuild_uri
from nefertem.utils.utils import build_uuid

if typing.TYPE_CHECKING:
    from nefertem.stores.artifact.objects.base import ArtifactStore, StoreConfig
    from nefertem.stores.metadata.objects.base import MetadataStore


class StoreBuilder:
    """
    StoreBuilder class.
    """

    def build_metadata_store(self, path: str | None = None) -> MetadataStore:
        """
        Method to create a metadata stores. If the path is None, the method creates a dummy
        metadata store.

        Parameters
        ----------
        path: str
            Path to the metadata store.

        Returns
        -------
        MetadataStore
            Metadata store object.
        """
        if path is None:
            return mdstore_registry[StoreKinds.DUMMY.value](DUMMY)
        uri = get_absolute_path(path, "metadata")
        return mdstore_registry[StoreKinds.LOCAL.value](uri)

    def build_artifact_store(self, tmp_dir: str, config: dict | None = None) -> ArtifactStore:
        """
        Method to create a artifact stores.

        Parameters
        ----------
        config : dict
            Store configuration.
        tmp_dir: str
            Temporary directory.

        Returns
        -------
        ArtifactStore
            Artifact store object.
        """
        params = self._parse_parameters(tmp_dir, config)
        return self._get_store(params)

    def _parse_parameters(self, tmp_dir: str, config: dict | None = None) -> dict:
        """
        Parse store parameters.

        Parameters
        ----------
        tmp_dir : str
            Temporary directory.
        config : dict
            Store configuration.

        Returns
        -------
        dict
            Store parameters.
        """
        cfg: StoreParameters = self._validate_parameters(config)
        store_type = map_uri_scheme(cfg.uri)
        return {
            "name": cfg.name,
            "store_type": store_type,
            "uri": self._resolve_uri(store_type, cfg.uri),
            "temp_dir": get_path(tmp_dir, build_uuid()),
            "is_default": cfg.is_default,
            "config": self._validate_config(store_type, cfg.config),
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
            return StoreParameters(StoreKinds.DUMMY.value, "_dummy://")
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
            return artstore_registry[store_type]["model"](**config)
        except (ValidationError, TypeError):
            raise StoreError("Invalid store configuration.")
        except KeyError:
            raise StoreError("Invalid store type.")

    @staticmethod
    def _get_store(params: dict) -> ArtifactStore:
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
            return artstore_registry[store_type]["store"](**params)
        except TypeError:
            raise StoreError("Something went wrong.")
        except KeyError:
            raise StoreError("Invalid store type.")

    @staticmethod
    def _resolve_uri(store_type: str, uri: str) -> str:
        """
        Resolve artifact URI location.

        Parameters
        ----------
        store_type : str
            Store type.
        uri : str
            Artifact URI.

        Returns
        -------
        str
            Resolved URI.
        """
        if store_type == StoreKinds.LOCAL.value:
            return get_absolute_path(uri, "artifact")
        if store_type == StoreKinds.S3.value:
            return rebuild_uri(uri, "artifact")
        return uri
