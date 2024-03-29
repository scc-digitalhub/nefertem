import pytest
from nefertem_core.stores.output.objects.dummy import DummyOutputStore


class TestDummyOutputStore:
    def test_init_run(self, store):
        assert store.init_run("exp1", "run1", True) is None

    def test_log_metadata(self, store):
        assert store.log_metadata() is None

    def test_build_source_destination(self, store):
        assert store._build_source_destination("dst", "src_type") is None

    def test_get_run_metadata_uri(self, store):
        assert store.get_run_path("exp1", "run1") is None


@pytest.fixture
def store() -> DummyOutputStore:
    return DummyOutputStore("_dummy")
