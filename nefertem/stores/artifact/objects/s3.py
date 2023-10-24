"""
Implementation of S3 artifact store.
"""
# pylint: disable=unused-import
import json
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Type

import boto3
import botocore.client
from botocore.exceptions import ClientError

from nefertem.stores.artifact.objects.base import ArtifactStore, StoreConfig
from nefertem.utils.exceptions import StoreError
from nefertem.utils.file_utils import check_path, get_path
from nefertem.utils.io_utils import wrap_string, write_bytesio
from nefertem.utils.uri_utils import build_key, get_name_from_uri, get_uri_path

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


class S3ArtifactStore(ArtifactStore):
    """
    S3 artifact store object.

    Allows the client to interact with S3 based storages.

    """

    def __init__(
        self,
        name: str,
        store_type: str,
        uri: str,
        temp_dir: str,
        is_default: bool,
        config: S3StoreConfig,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(name, store_type, uri, temp_dir, is_default)
        self.config = config

    ############################
    # I/O methods
    ############################

    def persist_artifact(self, src: Any, dst: str, src_name: str, metadata: dict) -> None:
        """
        Persist an artifact on S3 based storage.

        Parameters:
        -----------
        src : Any
            The source object to be persisted. It can be a file path as a string or Path object,
            a dictionary containing key-value pairs, or a buffer like StringIO/BytesIO.

        dst : str
            The destination partition for the artifact.

        src_name : str
            The name of the source object.

        metadata : dict
            Additional information to be stored with the artifact.

        Raises:
        -------
        NotImplementedError :
            If the source object is not a file path, dictionary, StringIO/BytesIO buffer.

        Returns:
        --------
        None
        """
        # Build the key for the artifact
        key = build_key(dst, src_name)

        # Local file
        if isinstance(src, (str, Path)) and check_path(src):
            return self._upload_file(str(src), key, metadata)

        # Dictionary
        if isinstance(src, dict) and src_name is not None:
            # Convert the dictionary to JSON string and write it to BytesIO buffer
            bytesio = write_bytesio(json.dumps(src))
            return self._upload_fileobj(bytesio, key, metadata)

        # StringIO/BytesIO buffer
        if isinstance(src, (BytesIO, StringIO)) and src_name is not None:
            # Wrap the buffer in a BufferedIOBase object and upload it
            bytesio = wrap_string(src)
            return self._upload_fileobj(bytesio, key, metadata)

        raise NotImplementedError

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
        key = f"{src}_native"
        cached = self._get_resource(key)
        if cached is not None:
            return cached

        self.logger.info(f"Fetching resource {src} from store {self.name}")
        url = self._get_presinged_url(src)
        self._register_resource(key, url)
        return url

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

    def _upload_file(self, src: str, key: str, metadata: dict) -> None:
        """
        Upload file to S3.

        Parameters
        ----------
        src : str
            The path to the file that needs to be uploaded to S3.
        key : str
            The key under which the file needs to be saved in S3.
        metadata : dict
            A dictionary containing metadata to be associated with the uploaded object.

        Returns
        -------
        None
        """
        client, bucket = self._check_factory()
        ex_args = {"Metadata": metadata}
        client.upload_file(Filename=src, Bucket=bucket, Key=key, ExtraArgs=ex_args)

    def _upload_fileobj(self, obj: BytesIO, key: str, metadata: dict) -> None:
        """
        Upload a file object to S3.

        Parameters
        ----------
        obj : BytesIO
            A file object representing the data to be uploaded to S3.
        key : str
            The key under which the file object needs to be saved in S3.
        metadata : dict
            A dictionary containing metadata to be associated with the uploaded object.

        Returns
        -------
        None
        """
        client, bucket = self._check_factory()
        ex_args = {"Metadata": metadata}
        client.upload_fileobj(obj, Bucket=bucket, Key=key, ExtraArgs=ex_args)
