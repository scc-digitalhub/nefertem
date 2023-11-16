from nefertem.plugins.inference.base import Inference
from nefertem.plugins.utils import Result, ResultType, exec_decorator


class SamplePlugin(Inference):
    """
    Sample concrete plugin implementation for testing.
    """

    def setup(self, *args, **kwargs) -> None:
        ...

    @exec_decorator
    def infer(self) -> dict:
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


class TestInference:
    def test_execute(self, caplog):
        plugin = SamplePlugin()
        plugin._id = "test"
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
        assert f"Execute inference - {plg}" in caplog.text
        assert f"Render report - {plg}" in caplog.text
        assert f"Render artifact - {plg}" in caplog.text
