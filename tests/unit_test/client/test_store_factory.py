import os

import pytest

from nefertem.stores.artifact.objects.base import ArtifactStore, StoreParameters
from nefertem.stores.builder import store_builder
from nefertem.stores.metadata.objects.base import MetadataStore
from nefertem.utils.uri_utils import get_uri_scheme

PROJ = "test"


class TestStoreBuilder:
    def test_build_metadata_store(self, tmp_path):
        store = store_builder.build_metadata_store(tmp_path)
        assert isinstance(store, MetadataStore)

    def test_build_artifact_store(self, st_loc1):
        store = store_builder.build_artifact_store(st_loc1)
        assert isinstance(store, ArtifactStore)

    def test_resolve_artifact_uri(self):
        uris = [
            "./test",
            "/test/test",
            "file:///test",
            "wasb://test/test",
            "wasbs://test/test",
            "s3://test/test",
            "ftp://test/test",
            "http://localhost:5000",
            "https://test.com",
            "sql://test.test",
            "dremio://test.test",
            "odbc://test.test",
        ]

        resolved_uris = []
        for uri in uris:
            scheme = get_uri_scheme(uri)
            new_uri = store_builder.resolve_artifact_uri(uri, scheme)
            resolved_uris.append(new_uri)
        assert resolved_uris[0] == f"{os.getcwd()}/test/artifact"
        assert resolved_uris[1] == "/test/test/artifact"
        assert resolved_uris[2] == "/test/artifact"
        assert resolved_uris[3] == "wasb://test/test/artifact"
        assert resolved_uris[4] == "wasbs://test/test/artifact"
        assert resolved_uris[5] == "s3://test/test/artifact"
        assert resolved_uris[6] == "ftp://test/test/artifact"
        assert resolved_uris[7] == "http://localhost:5000"
        assert resolved_uris[8] == "https://test.com"
        assert resolved_uris[9] == "sql://test.test"
        assert resolved_uris[10] == "dremio://test.test"
        assert resolved_uris[11] == "odbc://test.test"

        with pytest.raises(NotImplementedError):
            uri = "fail://test"
            scheme = get_uri_scheme(uri)
            new_uri = store_builder.resolve_artifact_uri(uri, scheme)

    def test_validate_parameters(self, st_loc1):
        cfg = store_builder._validate_parameters(st_loc1)
        assert isinstance(cfg, StoreParameters)
        assert cfg.type == "local"

        with pytest.raises(TypeError):
            store_builder._validate_parameters([])


# Artifact store config
@pytest.fixture
def st_loc1(local_store_cfg):
    return local_store_cfg
