from nefertem.metadata.blob import BlobLog


class TestBlobLog:
    def test_to_dict(self):
        log = BlobLog("test", "test", "test", {"test": "test"})
        expected_data = {
            "run_id": "test",
            "experiment_name": "test",
            "nefertem_version": "test",
            "contents": {"test": "test"},
        }
        assert log.to_dict() == expected_data
