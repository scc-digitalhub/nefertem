"""
Implementation of S3 artifact store.
"""
from __future__ import annotations

# pylint: disable=unused-import
from pathlib import Path
from typing import Type

import boto3
import botocore.client
from botocore.exceptions import ClientError
from nefertem_core.stores.input.objects._base import InputStore, StoreConfig
from nefertem_core.utils.exceptions import StoreError

# Type aliases
S3Client = Type["botocore.client.S3"]


class S3StoreConfig(StoreConfig):
    """
    S3 store configuration class.
    """

    endpoint_url: str
    """S3 endpoint URL."""

    aws_access_key_id: str
    """AWS access key ID."""

    aws_secret_access_key: str
    """AWS secret access key."""

    bucket_name: str
    """S3 bucket name."""


class S3InputStore(InputStore):
    """
    S3 artifact store object.

    Allows the client to interact with S3 based storages.

    """

    def __init__(self, name: str, store_type: str, temp_dir: str, config: S3StoreConfig) -> None:
        """
        Constructor.
        """
        super().__init__(name, store_type, temp_dir)
        self.config = config

    ############################
    # Read methods
    ############################

    def fetch_file(self, src: str) -> str:
        """
        Return the path where a resource it is stored.

        Parameters
        ----------
        src : str
            The name of the file.

        Returns
        -------
        str
            The location of the requested file.
        """
        key = f"{src}_file"
        cached = self._get_resource(key)
        if cached is not None:
            return cached

        self.logger.info(f"Fetching resource {src} from store {self.name}")
        dst = self.temp_dir / src.split("/")[-1]
        filepath = self._download_file(src, dst)
        self._register_resource(key, filepath)
        return filepath

    def fetch_native(self, src: str) -> str:
        """
        Return a native format path for a resource.

        Parameters
        ----------
        src : str
            Key of the resource.

        Returns
        -------
        str
            A presigned URL.
        """
        return self._get_presinged_url(src)

    ############################
    # Private helper methods
    ############################

    def _get_bucket(self) -> str:
        """
        Get the name of the S3 bucket from the URI.

        Returns
        -------
        str
            The name of the S3 bucket.
        """
        return self.config.bucket_name

    def _get_client(self) -> S3Client:
        """
        Get an S3 client object.

        Returns
        -------
        S3Client
            Returns a client object that interacts with the S3 storage service.
        """
        cfg = {
            "endpoint_url": self.config.endpoint_url,
            "aws_access_key_id": self.config.aws_access_key_id,
            "aws_secret_access_key": self.config.aws_secret_access_key,
        }
        return boto3.client("s3", **cfg)

    def _check_factory(self) -> tuple[S3Client, str]:
        """
        Check if the S3 bucket is accessible by sending a head_bucket request.

        Returns
        -------
        tuple[S3Client, str]
            A tuple containing the S3 client object and the name of the S3 bucket.
        """
        client = self._get_client()
        bucket = self._get_bucket()
        self._check_access_to_storage(client, bucket)
        return client, bucket

    @staticmethod
    def _check_access_to_storage(client: S3Client, bucket: str) -> None:
        """
        Check if the S3 bucket is accessible by sending a head_bucket request.

        Parameters
        ----------
        client : S3Client
            The S3 client object.
        bucket : str
            The name of the S3 bucket.

        Returns
        -------
        None

        Raises
        ------
        StoreError:
            If access to the specified bucket is not available.
        """
        try:
            client.head_bucket(Bucket=bucket)
        except ClientError as exc:
            raise StoreError("No access to s3 bucket!") from exc

    ############################
    # Private I/O methods
    ############################

    def _download_file(self, key: str, dst: str) -> Path:
        """
        Download a file from S3 based storage. The function checks if the bucket is accessible
        and if the destination directory exists. If the destination directory does not exist,
        it will be created.

        Parameters
        ----------
        key : str
            The key of the file on S3 based storage.
        dst : str
            The destination of the file on local filesystem.

        Returns
        -------
        Path
            The path of the downloaded file.
        """
        client, bucket = self._check_factory()
        client.download_file(bucket, key, dst)
        return Path(dst)

    def _get_presinged_url(self, src: str) -> str:
        """
        Returns a presigned URL for a specified object in an S3 bucket.

        Parameters:
        -----------
        src : str
            The name of the file.

        Returns:
        --------
        url: string
            A string representing the generated Presigned URL
        """
        client, bucket = self._check_factory()
        return client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": src},
            ExpiresIn=7200,
        )
