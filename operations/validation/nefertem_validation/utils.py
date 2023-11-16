from __future__ import annotations

from nefertem.utils.exceptions import NefertemError


class ValidationError(NefertemError):
    """
    Raised when incontered errors on validation.
    """
