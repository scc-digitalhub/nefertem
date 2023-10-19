"""
StoreBuilder module.
"""
from __future__ import annotations

import typing
from pathlib import Path
from typing import Union

from nefertem.stores.artifact.registry import artstore_registry
from nefertem.stores.kinds import SchemeKinds
from nefertem.stores.metadata.registry import mdstore_registry
from nefertem.stores.models import StoreParameters
from nefertem.utils.commons import API_BASE, DUMMY
from nefertem.utils.file_utils import get_absolute_path
from nefertem.utils.uri_utils import check_url, get_uri_netloc, get_uri_path, get_uri_scheme, rebuild_uri
from nefertem.utils.utils import get_uiid

if typing.TYPE_CHECKING:
    from nefertem.stores.artifact.objects.base import ArtifactStore
    from nefertem.stores.metadata.objects.base import MetadataStore


class StoreBuilder:
    """
    StoreBuilder class.
    """

    def __init__(self, project_id: str, tmp_dir: str) -> None:
        self.project_id = project_id
        self.tmp_dir = tmp_dir

    def build(self, config: Union[dict, StoreParameters], md_store: bool = False) -> dict:
        """
        Builder method that recieves store configurations.
        """
        cfg = self._check_config(config)
        if md_store:
            return self.build_metadata_store(cfg)
        return self.build_artifact_store(cfg)

    def build_metadata_store(self, cfg: StoreParameters) -> MetadataStore:
        """
        Method to create a metadata stores.
        """
        scheme = get_uri_scheme(cfg.uri)
        new_uri = self.resolve_uri_metadata(cfg.uri, scheme, self.project_id)
        try:
            return mdstore_registry[cfg.type](cfg.name, cfg.type, new_uri, cfg.config)
        except KeyError:
            raise NotImplementedError

    @staticmethod
    def resolve_uri_metadata(uri: str, scheme: str, project_name: str) -> str:
        """
        Resolve metadata URI location.
        """
        if scheme in SchemeKinds.LOCAL.value:
            return get_absolute_path(get_uri_netloc(uri), get_uri_path(uri), "metadata")
        if scheme in SchemeKinds.HTTP.value:
            url = uri + API_BASE + project_name
            return check_url(url)
        if scheme in SchemeKinds.DUMMY.value:
            return uri
        raise NotImplementedError

    def build_artifact_store(self, cfg: StoreParameters) -> ArtifactStore:
        """
        Method to create a artifact stores.
        """
        scheme = get_uri_scheme(cfg.uri)
        new_uri = self.resolve_artifact_uri(cfg.uri, scheme)
        tmp = str(Path(self.tmp_dir, get_uiid()))
        try:
            return artstore_registry[cfg.type](cfg.name, cfg.type, new_uri, tmp, cfg.config, cfg.isDefault)
        except KeyError:
            raise NotImplementedError

    @staticmethod
    def resolve_artifact_uri(uri: str, scheme: str) -> str:
        """
        Resolve artifact URI location.
        """
        if scheme in SchemeKinds.LOCAL.value:
            return get_absolute_path(get_uri_netloc(uri), get_uri_path(uri), "artifact")
        if scheme in [
            *SchemeKinds.AZURE.value,
            *SchemeKinds.S3.value,
            *SchemeKinds.FTP.value,
        ]:
            return rebuild_uri(uri, "artifact")
        if scheme in [
            *SchemeKinds.HTTP.value,
            *SchemeKinds.SQL.value,
            *SchemeKinds.ODBC.value,
            *SchemeKinds.DUMMY.value,
        ]:
            return uri
        raise NotImplementedError

    @staticmethod
    def _check_config(config: Union[StoreParameters, dict]) -> StoreParameters:
        """
        Try to convert a dictionary in a StoreParameters model.
        In case the config parameter is None, return a dummy store basic
        config.
        """
        if config is None:
            return StoreParameters(name=DUMMY, type=DUMMY, uri=f"{DUMMY}://")
        if not isinstance(config, StoreParameters):
            try:
                return StoreParameters(**config)
            except TypeError:
                raise TypeError("Malformed store configuration.")
        return config
