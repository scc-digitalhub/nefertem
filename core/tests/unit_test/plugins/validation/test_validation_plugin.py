from unittest.mock import MagicMock

import pytest
from nefertem_core.plugins.utils import Result, ResultType, exec_decorator


class SamplePlugin:
    """
    Sample concrete plugin implementation for testing.
    """

    def setup(self, *args, **kwargs) -> None:
        ...

    @exec_decorator
    def validate(self) -> dict:
        return {"result": "success"}

    @exec_decorator
    def render_nefertem(self, obj: Result) -> Result:
        return obj  # dummy implementation for testing

    @exec_decorator
    def render_artifact(self, obj: Result) -> Result:
        return obj  # dummy implementation for testing

    @staticmethod
    def get_framework_name() -> str:
        return "SamplePlugin"

    @staticmethod
    def get_framework_version() -> str:
        return "1.0"


class TestValidation:
    def test_execute(self, caplog):
        plugin = SamplePlugin()
        plugin._id = "test"
        plugin.constraint = MagicMock()
        plugin.constraint.name = "test"
        plugin.constraint.resources = "test"

        result = plugin.execute()

        assert isinstance(result, dict)

        keys = [
            ResultType.FRAMEWORK.value,
            ResultType.NEFERTEM.value,
            ResultType.RENDERED.value,
            ResultType.LIBRARY.value,
        ]
        for k in keys:
            assert k in result

        assert isinstance(result[ResultType.FRAMEWORK.value], Result)
        assert isinstance(result[ResultType.NEFERTEM.value], Result)
        assert isinstance(result[ResultType.RENDERED.value], Result)
        assert isinstance(result[ResultType.LIBRARY.value], dict)
        lib = {"libraryName": "SamplePlugin", "libraryVersion": "1.0"}
        assert result[ResultType.LIBRARY.value] == lib

        plg = f"Plugin: SamplePlugin {plugin._id};"
        constraint = f"Constraint: {plugin.constraint.name};"
        resources = f"Resources: {plugin.constraint.resources};"
        assert f"Execute validation - {plg} {constraint} {resources}" in caplog.text
        assert f"Render report - {plg}" in caplog.text
        assert f"Render artifact - {plg}" in caplog.text

    def test_render_error_type(self):
        plugin = SamplePlugin()
        assert plugin._render_error_type("test") == {"type": "test"}

    @pytest.mark.parametrize(
        "report_type,error_list,result",
        [
            ("count", [None] * 100, []),
            ("partial", [None] * 101, [None] * 100),
            ("partial", [None] * 99, [None] * 99),
            ("partial", [None] * 99, [None] * 99),
            ("full", [None] * 101, [None] * 101),
            ("full", [None] * 99, [None] * 99),
        ],
    )
    def test_parse_error_report(self, report_type, error_list, result):
        plugin = SamplePlugin()
        plugin.error_report = report_type
        assert plugin._parse_error_report(error_list) == result

    @pytest.mark.parametrize(
        "count,records,expected",
        [
            (0, ["test"], {"count": 0, "records": ["test"]}),
            (0, None, {"count": 0, "records": []}),
        ],
    )
    def test_get_errors(self, count, records, expected):
        plugin = SamplePlugin()
        result = plugin._get_errors(count=count, records=records)
        assert result == expected
