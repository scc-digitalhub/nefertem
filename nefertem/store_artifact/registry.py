"""
ArtifactStore registry.
"""
from nefertem.store_artifact.azure_artifact_store import AzureArtifactStore
from nefertem.store_artifact.dummy_artifact_store import DummyArtifactStore
from nefertem.store_artifact.ftp_artifact_store import FTPArtifactStore
from nefertem.store_artifact.http_artifact_store import HTTPArtifactStore
from nefertem.store_artifact.local_artifact_store import LocalArtifactStore
from nefertem.store_artifact.odbc_artifact_store import ODBCArtifactStore
from nefertem.store_artifact.s3_artifact_store import S3ArtifactStore
from nefertem.store_artifact.sql_artifact_store import SQLArtifactStore
from nefertem.utils.commons import (
    STORE_AZURE,
    STORE_DUMMY,
    STORE_FTP,
    STORE_HTTP,
    STORE_LOCAL,
    STORE_ODBC,
    STORE_S3,
    STORE_SQL,
)

ART_STORES = {
    STORE_AZURE: AzureArtifactStore,
    STORE_DUMMY: DummyArtifactStore,
    STORE_FTP: FTPArtifactStore,
    STORE_HTTP: HTTPArtifactStore,
    STORE_LOCAL: LocalArtifactStore,
    STORE_ODBC: ODBCArtifactStore,
    STORE_S3: S3ArtifactStore,
    STORE_SQL: SQLArtifactStore,
}
