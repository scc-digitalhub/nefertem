"""
Validation plugin utils.
"""
from __future__ import annotations


def render_error_type(code: str) -> dict:
    """
    Return standard errors record format.

    Parameters
    ----------
    code : str
        Error code.

    Returns
    -------
    dict
        Error type record.
    """
    return {"type": code}


def parse_error_report(error_list: list, report_type) -> list:
    """
    Return a list of record according to user parameter.

    Parameters
    ----------
    error_list : list
        List of errors.

    Returns
    -------
    list
        List of errors.
    """
    if report_type == "count":
        return []
    if report_type == "partial":
        if len(error_list) <= 100:
            return error_list
        return error_list[:100]
    if report_type == "full":
        return error_list


def get_errors(count: int = 0, records: list = None) -> dict:
    """
    Return a common error structure.

    Parameters
    ----------
    count : int
        Number of errors.
    records : list
        List of errors.

    Returns
    -------
    dict
        Error structure.
    """
    if records is None:
        records = []
    return {"count": count, "records": records}
