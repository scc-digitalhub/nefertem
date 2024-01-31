from pathlib import Path

import pytest
from nefertem_core.plugins.utils import ResultType
from nefertem_core.run.handler import RunHandler


class TestRun:
    def test_log_run(self, handler, temp_data):
        pth = Path(temp_data, "report_0.json")
        handler.log_metadata({"test": "test"}, str(pth.parent), "report", True)
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_log_env(self, handler, temp_data):
        pth = Path(temp_data, "report_0.json")
        handler.log_metadata({"test": "test"}, str(pth.parent), "report", True)
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_get_blob(self, handler):
        pass

    def test_log_metadata(self, handler, temp_data):
        pth = Path(temp_data, "report_0.json")
        handler.log_metadata({"test": "test"}, str(pth.parent), "report", True)
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_get_artifact_metadata(self, handler):
        pass

    def test_persist_artifact(self, handler, temp_data):
        pth = Path(temp_data, "test.txt")
        handler.persist_artifact({"test": "test"}, str(pth.parent), "test.txt", {})
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_render_artifact_name(self, handler):
        pass

    def test_check_metadata_uri(self, handler):
        pass

    def test_check_artifacts_uri(self, handler):
        pass

    def test_get_libraries(self, handler):
        pass

    def test_infer_framework(self, handler):
        pass

    def test_infer_nefertem(self, handler):
        pass

    def test_infer(self, handler):
        pass

    def test_log_schema(self, handler):
        pass

    def test_persist_schema(self, handler):
        pass

    def test_validate_framework(self, handler):
        pass

    def test_validate_nefertem(self, handler):
        pass

    def test_validate(self, handler):
        pass

    def test_log_report(self, handler):
        pass

    def test_persist_report(self, handler):
        pass

    def test_profile_framework(self, handler):
        pass

    def test_profile_nefertem(self, handler):
        pass

    def test_profile(self, handler):
        pass

    def test_log_profile(self, handler):
        pass

    def test_persist_profile(self, handler):
        pass

    def test_persist_data(self, handler, local_resource, tmp_path):
        # Use another tmp path, otherways raise SameFileError
        # because copy same file to same path (from temp_data to temp_data)
        handler.persist_data([local_resource], tmp_path)
        assert Path(tmp_path, "test_csv_file.csv").exists()


# RunHandler
@pytest.fixture()
def handler(run_empty, store_handler):
    return RunHandler(run_empty, store_handler)


# Sample result dict
@pytest.fixture()
def dict_result(result_obj):
    return {
        ResultType.FRAMEWORK.value: result_obj,
        ResultType.NEFERTEM.value: result_obj,
        ResultType.RENDERED.value: result_obj,
        ResultType.LIBRARY.value: [{"test": "test"}],
    }
