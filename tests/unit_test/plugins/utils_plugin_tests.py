from nefertem_inference.metadata.report import NefertemSchema
from nefertem_validation.metadata.report import NefertemReport

from nefertem.metadata.report import NefertemProfile
from nefertem.plugins.plugin import Plugin
from nefertem.plugins.utils import RenderTuple, Result
from nefertem.utils.commons import INFER, PROFILE, VALIDATE


def correct_setup(plg):
    assert isinstance(plg, Plugin)
    # Possible attributes of a plugin
    test_attr = [
        "data_reader",
        "resource",
        "exec_args",
        "error_report",
        "constraint",
        "db",
    ]
    for attr in test_attr:
        if hasattr(plg, attr):
            assert getattr(plg, attr) == "test"


def correct_result(output):
    assert isinstance(output, Result)
    assert output.errors is None
    assert output.status == "finished"
    assert output.artifact is not None


def correct_execute(output):
    correct_result(output)


def correct_render_nefertem(output, op):
    correct_result(output)
    artifact = output.artifact
    if op == INFER:
        assert isinstance(artifact, NefertemSchema)
        assert isinstance(artifact.duration, float)
        assert isinstance(artifact.fields, list)
    if op == PROFILE:
        assert isinstance(artifact, NefertemProfile)
        assert isinstance(artifact.duration, float)
        assert isinstance(artifact.stats, dict)
        assert isinstance(artifact.fields, dict)
    if op == VALIDATE:
        assert isinstance(artifact, NefertemReport)
        assert isinstance(artifact.duration, float)
        assert isinstance(artifact.constraint, dict)
        assert isinstance(artifact.valid, bool)
        assert isinstance(artifact.errors, dict)


def correct_render_artifact(output):
    correct_result(output)
    assert isinstance(output.artifact, list)
    assert isinstance(output.artifact[0], RenderTuple)


def incorrect_execute(output):
    assert isinstance(output, Result)
    assert output.errors is not None
    assert output.status == "error"
    assert output.artifact is None


def incorrect_render_nefertem(output, op):
    assert isinstance(output, Result)
    artifact = output.artifact
    if op == INFER:
        assert isinstance(artifact, NefertemSchema)
        assert isinstance(artifact.duration, float)
        assert not artifact.fields
    if op == PROFILE:
        assert isinstance(artifact, NefertemProfile)
        assert isinstance(artifact.duration, float)
        assert not artifact.stats
        assert not artifact.fields
    if op == VALIDATE:
        assert isinstance(artifact, NefertemReport)
        assert isinstance(artifact.duration, float)
        assert not artifact.valid


def incorrect_render_artifact(output):
    assert isinstance(output, Result)
    assert output.artifact is not None
    assert isinstance(output.artifact, list)
    assert isinstance(output.artifact[0], RenderTuple)
    assert "errors" in output.artifact[0].object


def correct_plugin_build(plugins, plg_type):
    assert isinstance(plugins, list)
    assert len(plugins) == 1
    assert isinstance(plugins[0], plg_type)
