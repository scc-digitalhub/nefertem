from nefertem_core.metadata.blob import Blob


class TestBlobLog:
    def test_to_dict(self):
        log = Blob("test", "test", "test", {"test": "test"})
        expected_data = {
            "run_id": "test",
            "experiment_name": "test",
            "nefertem_version": "test",
            "contents": {"test": "test"},
        }
        assert log.to_dict() == expected_data
