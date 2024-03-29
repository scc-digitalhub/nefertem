import pytest
from nefertem_core.plugins.utils import Result, exec_decorator
from nefertem_core.utils.commons import STATUS_ERROR, STATUS_FINISHED


@pytest.fixture(
    params=[
        (
            (lambda x: x**2),
            [2],
            {"status": STATUS_FINISHED, "duration": 0, "errors": None},
        ),
        (
            (lambda x: 1 / x),
            [0],
            {"status": STATUS_ERROR, "duration": 0, "errors": ("division by zero",)},
        ),
    ]
)
def input_output(request):
    fnc, args, expected = request.param
    return fnc, args, Result(**expected)


def test_exec_decorator(input_output):
    fnc, args, expected = input_output
    actual = exec_decorator(fnc)(*args)
    assert actual.status == expected.status
    assert actual.duration == expected.duration
    assert actual.errors == expected.errors
