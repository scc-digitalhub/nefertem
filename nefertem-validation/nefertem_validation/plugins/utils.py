from typing import Any


class ValidationReport:
    """
    Simple class to aggregate custom validation result.
    """

    def __init__(
        self,
        result: Any,
        valid: bool,
        error: list,
    ) -> None:
        self.result = result
        self.valid = valid
        self.error = error

    def to_dict(self):
        return {"result": self.result, "valid": self.valid, "error": self.error}
