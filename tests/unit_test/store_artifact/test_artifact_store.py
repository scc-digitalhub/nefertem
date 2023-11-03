import pytest

from nefertem.stores.input.objects.base import InputStore
from tests.conftest import TEST_FILENAME


class TestInputStore:
    def test_get_run_artifacts_uri(self, store):
        assert store.get_run_path("test", "test") == "test/test"

    def test_get_resource(self, store):
        assert not store._get_resource(TEST_FILENAME)
        store._register_resource(TEST_FILENAME, TEST_FILENAME)
        assert store._get_resource(TEST_FILENAME) == TEST_FILENAME

    def test_register_resource(self, store):
        store._register_resource(TEST_FILENAME, TEST_FILENAME)
        assert store._get_resource(TEST_FILENAME) == TEST_FILENAME

    def test_clean_paths(self, store):
        assert not store._get_resource(TEST_FILENAME)
        store._register_resource(TEST_FILENAME, TEST_FILENAME)
        assert store._get_resource(TEST_FILENAME) == TEST_FILENAME
        store.clean_paths()
        assert not store._get_resource(TEST_FILENAME)


class InputStoreSample(InputStore):
    def persist_artifact(self, *args, **kwargs):
        ...

    def _get_and_register_artifact(self, *args, **kwargs):
        ...

    def _get_data(self, *args, **kwargs):
        ...

    def _store_data(self, *args, **kwargs):
        ...

    def _check_access_to_storage(self, *args, **kwargs):
        ...


@pytest.fixture
def store():
    return InputStoreSample("", "", "", "")
