from pathlib import Path

import pytest
from nefertem_core.client.store_handler import StoreHandler
from nefertem_core.run.builder import RunBuilder
from nefertem_core.run.run import Run
from nefertem_core.utils.exceptions import RunError


class TestRunBuilder:
    def test_init_run(self, builder, temp_data):
        builder._init_run("test", "test", True)
        path = Path(temp_data, "metadata", "test", "test")
        assert path.exists()
        assert path.is_dir()

    def test_get_md_uri(self, builder, temp_data):
        uri = builder._get_md_uri("test", "test")
        assert uri == str(Path(temp_data, "metadata", "test", "test"))

    def test_get_art_uri(self, builder, temp_data):
        uri = builder._get_art_uri("test", "test")
        assert uri == str(Path(temp_data, "artifact", "test", "test"))

    def test_check_unique_resource(self, builder, local_resource):
        with pytest.raises(RunError):
            builder._check_unique_resource([local_resource, local_resource])

    def test_create_run(self, builder, temp_data, run_empty, local_resource):
        run = builder.create_run([local_resource], run_empty, "test", "test", True)
        path = Path(temp_data, "metadata", "test", "test")
        assert path.exists()
        assert path.is_dir()
        assert isinstance(run, Run)


@pytest.fixture()
def builder(local_md_store_cfg, local_store_cfg):
    store_handler = StoreHandler(metadata_store=local_md_store_cfg, store=local_store_cfg)
    return RunBuilder(store_handler)
