"""
MetadataKind module.
"""
from enum import Enum


class MetadataKind(Enum):
    "Kind of metadata."

    RUN = "run"
    REPORT = "report"
    SCHEMA = "schema"
    PROFILE = "profile"
    ARTIFACT = "artifact"
    RUN_ENV = "run_env"
