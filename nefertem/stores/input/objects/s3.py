"""
Implementation of S3 artifact store.
"""
# pylint: disable=unused-import
from typing import Type

import boto3
import botocore.client
from botocore.exceptions import ClientError

from nefertem.stores.input.objects.base import InputStore, StoreConfig
from nefertem.utils.exceptions import StoreError
from nefertem.utils.file_utils import get_path
from nefertem.utils.uri_utils import get_name_from_uri, get_uri_path

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

    def __init__(self, name: str, uri: str, store_type: str, temp_dir: str, config: S3StoreConfig) -> None:
        """
        Constructor.
        """
        super().__init__(name, uri, store_type, temp_dir)
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
        dst = get_path(self.temp_dir, get_name_from_uri(src))
        filepath = self._download_file(src, dst)
        self._register_resource(key, filepath)
        return filepath

    def fetch_native(self, src: str) -> str:
        """
        Return a native format path for a resource.

        Parameters
        ----------
        src : str
            A presigned URL.

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
        return str(self.config.bucket_name)

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

    @staticmethod
    def _get_key(path: str) -> str:
        """
        Build key.

        Parameters
        ----------
        path : str
            The source path to get the key from.

        Returns
        -------
        str
            The key.
        """
        key = get_uri_path(path)
        if key.startswith("/"):
            key = key[1:]
        return key

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

    def _check_access_to_storage(self, client: S3Client, bucket: str) -> None:
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

    def _download_file(self, key: str, dst: str) -> str:
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
        str
            The path of the downloaded file.
        """
        client, bucket = self._check_factory()
        client.download_file(bucket, key, dst)
        return dst

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
