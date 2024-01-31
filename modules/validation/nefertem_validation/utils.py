from __future__ import annotations

from nefertem_core.utils.exceptions import NefertemError


class ValidationError(NefertemError):
    """
    Raised when incontered errors on validation.
    """
