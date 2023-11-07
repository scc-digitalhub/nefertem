import pytest

from nefertem.utils.exceptions import NefertemError, RunError, StoreError
from operations.nefertem_validation.nefertem_validation.utils import ValidationError


def test_nefertem_error():
    with pytest.raises(NefertemError):
        raise NefertemError("Nefertem error occurred")


def test_store_error():
    with pytest.raises(StoreError):
        raise StoreError("Store error occurred")


def test_run_error():
    with pytest.raises(RunError):
        raise RunError("Run error occurred")


def test_validation_error():
    with pytest.raises(ValidationError):
        raise ValidationError("Validation error occurred")


def test_subclass():
    assert issubclass(StoreError, NefertemError)
    assert issubclass(RunError, NefertemError)
    assert issubclass(ValidationError, NefertemError)
