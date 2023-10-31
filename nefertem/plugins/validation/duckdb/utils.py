"""
SQL checks module.
"""
import re
from typing import Any


def evaluate_validity(result: Any, expect: str, value: Any) -> tuple:
    """
    Evaluate validity of query results.
    """
    try:
        if expect == "empty":
            return evaluate_empty(result, empty=True)
        if expect == "non-empty":
            return evaluate_empty(result, empty=False)
        if expect == "exact":
            return evaluate_exact(result, value)
        if expect == "range":
            return evaluate_range(result, value)
        if expect == "minimum":
            return evaluate_min(result, value)
        if expect == "maximum":
            return evaluate_max(result, value)
        else:
            return False, "Invalid constraint expectation."

    except Exception as ex:
        return False, ex.args


def evaluate_empty(result: Any, empty: bool) -> tuple:
    """
    Evaluate table emptiness.
    """
    # Could be done with evaluate_exact,
    # but we want a specific error.
    if empty:
        if result == 0:
            return True, None
        return False, "Table is not empty."
    if result > 0:
        return True, None
    return False, "Table is empty."


def evaluate_exact(result: Any, value: Any) -> tuple:
    """
    Evaluate if a value is exactly as expected.
    """
    if bool(result == value):
        return True, None
    return False, f"Expected value {value}, instead got {result}."


def evaluate_min(result: int | float, value: int | float) -> tuple:
    """
    Check if a value is bigger than a specific value.
    """
    if bool(float(result) >= value):
        return True, None
    return False, f"Minimum value {value}, instead got {result}."


def evaluate_max(result: int | float, value: int | float) -> tuple:
    """
    Check if a value is lesser than a specific value.
    """
    if bool(float(result) <= value):
        return True, None
    return False, f"Maximum value {value}, instead got {result}."


def evaluate_range(result: Any, _range: str) -> tuple:
    """
    Check if a value is in desired range.
    """
    regex = r"^(\[|\()([+-]?[0-9]+[.]?[0-9]*),\s?([+-]?[0-9]+[.]?[0-9]*)(\]|\))$"
    try:
        mtc = re.match(regex, _range)
        if mtc:
            # Upper and lower limit type
            # [ ] are inclusive
            # ( ) are exclusive
            ll = mtc.group(1)
            ul = mtc.group(4)

            # Minimum and maximum range values
            _min = float(mtc.group(2))
            _max = float(mtc.group(3))

            # Value to check to float
            cv = float(result)

            if ll == "[" and ul == "]":
                valid = _min <= cv <= _max
            elif ll == "[" and ul == ")":
                valid = _min <= cv < _max
            elif ll == "(" and ul == "]":
                valid = _min < cv <= _max
            elif ll == "(" and ul == ")":
                valid = _min < cv < _max

            if valid:
                return True, None
            return (
                False,
                f"Expected value between {ll}{mtc.group(2)}, {mtc.group(3)}{ul}.",
            )
    except ValueError:
        return False, "Invalid range format."
