from pathlib import Path

import pytest

from nefertem.plugins.factory import builder_factory
from nefertem.plugins.plugin import Plugin
from nefertem.plugins.utils import Result, ResultType
from nefertem.run.handler import RunHandler
from nefertem.utils.exceptions import RunError
from tests.conftest import CONST_FRICT_01

INFER = "infer"
VALIDATE = "validate"
PROFILE = "profile"
MT_NT_REPORT = "nefertem_report"


class TestRunHandler:
    def test_create_plugins(self, run_empty, store_handler, handler, local_resource):
        cfg = [run_empty.inference, run_empty.validation, run_empty.profiling]
        ops = [INFER, VALIDATE, PROFILE]
        stores = store_handler.get_all_art_stores()

        for i, j in zip(cfg, ops):
            builders = builder_factory(i, j, stores)
            if j == VALIDATE:
                plugins = handler._create_plugins(builders, [local_resource], [CONST_FRICT_01], "full")
            else:
                plugins = handler._create_plugins(builders, [local_resource])
            assert isinstance(plugins, list)
            for p in plugins:
                assert isinstance(p, Plugin)

    def test_parse_report_arg(self, handler):
        with pytest.raises(RunError):
            handler._parse_report_arg("")
        for i in ("count", "partial", "full"):
            assert handler._parse_report_arg(i) is None

    def test_register_results(self, dict_result, handler):
        res = handler._register_results(INFER, dict_result)
        assert res is None
        with pytest.raises(KeyError):
            handler._register_results("", dict_result)

    def test_destroy_builders(self, run_empty, store_handler, handler):
        cfg = [run_empty.inference, run_empty.validation, run_empty.profiling]
        ops = [INFER, VALIDATE, PROFILE]
        stores = store_handler.get_all_art_stores()

        for i, j in zip(cfg, ops):
            builders = builder_factory(i, j, stores)
            assert handler._destroy_builders(builders) is None

    def test_get_item(self, dict_result, handler):
        op = INFER
        res = handler._register_results(op, dict_result)
        res = handler.get_item(op, ResultType.NEFERTEM.value)
        assert isinstance(res[0], Result)

    def test_get_artifact_schema(self, dict_result, handler):
        op = INFER
        handler._register_results(op, dict_result)
        res = handler.get_artifact_schema()
        assert res[0] == "test"

    def test_get_artifact_report(self, dict_result, handler):
        op = VALIDATE
        handler._register_results(op, dict_result)
        res = handler.get_artifact_report()
        assert res[0] == "test"

    def test_get_artifact_profile(self, dict_result, handler):
        op = PROFILE
        handler._register_results(op, dict_result)
        res = handler.get_artifact_profile()
        assert res[0] == "test"

    def test_get_nefertem_schema(self, dict_result, handler):
        op = INFER
        handler._register_results(op, dict_result)
        res = handler.get_nefertem_schema()
        assert res[0] == "test"

    def test_get_nefertem_report(self, dict_result, handler):
        op = VALIDATE
        handler._register_results(op, dict_result)
        res = handler.get_nefertem_report()
        assert res[0] == "test"

    def test_get_nefertem_profile(self, dict_result, handler):
        op = PROFILE
        handler._register_results(op, dict_result)
        res = handler.get_nefertem_profile()
        assert res[0] == "test"

    def test_get_rendered_schema(self, dict_result, handler):
        op = INFER
        handler._register_results(op, dict_result)
        res = handler.get_rendered_schema()
        assert res[0] == "test"

    def test_get_rendered_report(self, dict_result, handler):
        op = VALIDATE
        handler._register_results(op, dict_result)
        res = handler.get_rendered_report()
        assert res[0] == "test"

    def test_get_rendered_profile(self, dict_result, handler):
        op = PROFILE
        handler._register_results(op, dict_result)
        res = handler.get_rendered_profile()
        assert res[0] == "test"

    def test_get_libraries(self, dict_result, handler):
        op = PROFILE
        handler._register_results(op, dict_result)
        res = handler.get_libraries()
        assert res[op] == [{"test": "test"}]

    def test_log_metadata(self, handler, temp_data):
        pth = Path(temp_data, "report_0.json")
        handler.log_metadata({"test": "test"}, str(pth.parent), MT_NT_REPORT, True)
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_persist_artifact(self, handler, temp_data):
        pth = Path(temp_data, "test.txt")
        handler.persist_artifact({"test": "test"}, str(pth.parent), "test.txt", {})
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

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
