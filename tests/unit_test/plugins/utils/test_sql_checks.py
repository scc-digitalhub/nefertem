from nefertem.plugins.utils.sql_checks import (
    evaluate_empty,
    evaluate_exact,
    evaluate_max,
    evaluate_min,
    evaluate_range,
    evaluate_validity,
)


def test_evaluate_validity():
    assert evaluate_validity(0, "empty", None) == (True, None)
    assert evaluate_validity(5, "empty", None) == (
        False,
        "Table is not empty.",
    )
    assert evaluate_validity(7, "non-empty", None) == (True, None)
    assert evaluate_validity(0, "non-empty", None) == (
        False,
        "Table is empty.",
    )
    assert evaluate_validity(4, "exact", 4) == (True, None)
    assert evaluate_validity(2.1, "exact", 2.0) == (
        False,
        "Expected value 2.0, instead got 2.1.",
    )
    assert evaluate_validity(3, "minimum", 2) == (True, None)
    assert evaluate_validity(4.8, "minimum", 4.9) == (
        False,
        "Minimum value 4.9, instead got 4.8.",
    )
    assert evaluate_validity(-1, "minimum", -3) == (True, None)
    assert evaluate_validity(6, "maximum", 7) == (True, None)
    assert evaluate_validity(9.9, "maximum", 10.1) == (True, None)
    assert evaluate_validity(25, "maximum", 15) == (
        False,
        "Maximum value 15, instead got 25.",
    )
    assert evaluate_validity(5.6, "range", "[4, 9]") == (True, None)
    assert evaluate_validity(13, "range", "[5, 12]") == (
        False,
        "Expected value between [5, 12].",
    )
    assert evaluate_validity("test", "INCORRECT", None) == (
        False,
        "Invalid constraint expectation.",
    )


def test_evaluate_empty():
    assert evaluate_empty(0, True) == (True, None)
    assert evaluate_empty(5, True) == (False, "Table is not empty.")
    assert evaluate_empty(7, False) == (True, None)
    assert evaluate_empty(0, False) == (False, "Table is empty.")


def test_evaluate_exact():
    assert evaluate_exact(4, 4) == (True, None)
    assert evaluate_exact("test", "test") == (True, None)
    assert evaluate_exact(2.1, 2.0) == (False, "Expected value 2.0, instead got 2.1.")


def test_evaluate_min():
    assert evaluate_min(3, 2) == (True, None)
    assert evaluate_min(4.8, 4.9) == (False, "Minimum value 4.9, instead got 4.8.")
    assert evaluate_min(-1, -3) == (True, None)


def test_evaluate_max():
    assert evaluate_max(6, 7) == (True, None)
    assert evaluate_max(9.9, 10.1) == (True, None)
    assert evaluate_max(25, 15) == (False, "Maximum value 15, instead got 25.")


def test_evaluate_range_valid_input():
    assert evaluate_range(5.6, "[4, 9]") == (True, None)
    assert evaluate_range(2.8, "[-10, -1)") == (
        False,
        "Expected value between [-10, -1).",
    )
    assert evaluate_range(3.14, "(2, 4)") == (True, None)


def test_evaluate_range_invalid_input():
    assert evaluate_range(-7, "[2, 10)") == (False, "Expected value between [2, 10).")
    assert evaluate_range(13, "[5, 12]") == (False, "Expected value between [5, 12].")
    assert evaluate_range("bad input", "(0, 1)") == (False, "Invalid range format.")
