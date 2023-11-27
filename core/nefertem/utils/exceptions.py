"""
Exceptions module.
"""


class NefertemError(Exception):
    """
    Base class for nefertem exception.
    """


class StoreError(NefertemError):
    """
    Raised when incontered errors on Stores.
    """


class RunError(NefertemError):
    """
    Raised when incontered errors on Runs.
    """
