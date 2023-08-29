from nefertem.metadata.blob_log import BlobLog


class TestBlobLog:
    def test_to_dict(self):
        log = BlobLog("test", "test", "test", {"test": "test"})
        expected_data = {
            "runId": "test",
            "experimentName": "test",
            "nefertemVersion": "test",
            "test": "test",
        }
        assert log.to_dict() == expected_data
