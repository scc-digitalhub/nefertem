import pytest
from nefertem_core.client.client import Client
from nefertem_core.run.run import Run
from nefertem_core.utils.exceptions import StoreError


class TestClient:
    def test_create_empty_client(self):
        client = Client()
        assert isinstance(client, Client)

    def test_create_client_only_metadata_store(self, tmp_path):
        client = Client(metadata_store_path=tmp_path)
        assert isinstance(client, Client)

    def test_create_client_only_artifact_store(self, local_store_cfg):
        print(local_store_cfg)
        client = Client(store=[local_store_cfg])
        assert isinstance(client, Client)

    def test_create_client(self, local_store_cfg, tmp_path):
        client = Client(metadata_store_path=tmp_path, store=[local_store_cfg])
        assert isinstance(client, Client)

    def test_create_client_multiple_stores(self, local_store_cfg, local_store_cfg_2, tmp_path):
        client = Client(
            metadata_store_path=tmp_path,
            store=[local_store_cfg, local_store_cfg_2],
        )
        assert isinstance(client, Client)

    def test_add_store(self, local_store_cfg, local_store_cfg_2, tmp_path):
        client = Client(metadata_store_path=tmp_path, store=[local_store_cfg])
        client.add_store(local_store_cfg_2)

    def test_fail_add_store(self):
        client = Client()
        with pytest.raises(StoreError):
            client.add_store("")

    def test_create_run(self, local_store_cfg, tmp_path, run_empty, local_resource):
        client = Client(metadata_store_path=tmp_path, store=[local_store_cfg])
        run = client.create_run([local_resource], run_empty)
        assert isinstance(run, Run)
