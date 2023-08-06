from __future__ import absolute_import

import glob
import logging
import os.path
import pathlib
import tarfile
import tempfile
from collections import namedtuple
from typing import Optional, Tuple

import oss2
import six
from six.moves.urllib import parse

logger = logging.getLogger(__name__)


def is_oss_uri(uri: str) -> bool:
    """Return if url is in OSS URL schema."""
    return bool(uri and isinstance(uri, six.string_types) and uri.startswith("oss://"))


ParsedOssUri = namedtuple(
    "ParsedOssUri", field_names=["bucket_name", "object_key", "endpoint", "role_arn"]
)


def parse_oss_uri(uri: str) -> "ParsedOssUri":
    """Parse the given OSS schema URI and returns a namedtuple including bucket_name,
        object_key, endpoint, role_arn.

    Args:
        uri: URL in OSS schema ( oss://<bucket.endpoint>/<object_key>?endpoint=<endpoint>&host=<endpoint>&role_arn=<role_arn>)
    Returns:
        ParsedOssUrl: Returns a namedtuple including bucket_name, object_key, endpoint and role_arn.
    """

    uri = OssUriObj(uri)
    return ParsedOssUri(
        bucket_name=uri.bucket_name,
        object_key=uri.object_key,
        endpoint=uri.endpoint,
        role_arn=uri.role_arn,
    )


def _tar_file(source_file, target=None):
    source_file = (
        source_file if os.path.isabs(source_file) else os.path.abspath(source_file)
    )
    if not os.path.exists(source_file):
        raise ValueError("source file not exists: %s", source_file)
    if os.path.isdir(source_file):
        arcname = ""
    else:
        arcname = os.path.basename(source_file)

    if not target:
        target = tempfile.mktemp()
    with tarfile.open(target, "w:gz") as tar:
        tar.add(name=source_file, arcname=arcname)
    return target


def upload_data(
    source_path: str,
    oss_path: str,
    oss_bucket: oss2.Bucket,
    is_tar: Optional[bool] = False,
) -> str:
    """Upload local source file/directory to OSS.

    Examples::

        # compress and upload local directory `./src/` to OSS
        >>> upload_data(source_path="./src/", oss_path="path/to/file",
        >>> oss_bucket=session.oss_bucket, is_tar=True)


    Args:
        source_path (str): Source file local path which needs to be uploaded, can be
            a single file or a directory.
        oss_path (str): Destination OSS path.
        oss_bucket (oss2.Bucket): OSS bucket used to store the upload data.
        is_tar (bool): Whether to compress the file before uploading (default: False).

    Returns:
        str: A string in OSS URI format. If the source_path is directory, return the
            OSS URI represent the directory for uploaded data, else then
            returns the OSS URI points the uploaded file.
    """
    source_path_obj = pathlib.Path(source_path)
    if not source_path_obj.exists():
        raise RuntimeError("Source path is not exist: {}".format(source_path))

    if is_tar:
        # compress the local data and upload the compressed source data.
        with tempfile.TemporaryDirectory() as dir_name:
            temp_tar_path = _tar_file(
                source_path, os.path.join(dir_name, "source.tar.gz")
            )
            dest_path = (
                os.path.join(oss_path, os.path.basename(temp_tar_path))
                if oss_path.endswith("/")
                else oss_path
            )
            oss_bucket.put_object_from_file(key=dest_path, filename=temp_tar_path)
            return "oss://{}/{}".format(oss_bucket.bucket_name, dest_path)
    elif not source_path_obj.is_dir():
        # if source path is a file, just invoke bucket.put_object.

        # if the oss_path is endswith slash, the file will be uploaded to
        # "{oss_path}{filename}", else the file will be uploaded to "{oss_path}".
        dest_path = (
            os.path.join(oss_path, os.path.basename(source_path))
            if oss_path.endswith("/")
            else oss_path
        )
        oss_bucket.put_object_from_file(key=dest_path, filename=source_path)
        return "oss://{}/{}".format(oss_bucket.bucket_name, dest_path)
    else:
        # if the source path is a directory, upload all the file under the directory.
        source_files = glob.glob(
            pathname=str(source_path_obj / "**"),
            recursive=True,
        )
        if not oss_path.endswith("/"):
            oss_path += "/"
        for file_path in source_files:
            file_path_obj = pathlib.Path(file_path)
            if file_path_obj.is_dir():
                continue
            file_relative_path = file_path_obj.relative_to(source_path_obj).as_posix()
            object_key = oss_path + file_relative_path
            oss_bucket.put_object_from_file(key=object_key, filename=file_path)
        return "oss://{}/{}".format(oss_bucket.bucket_name, oss_path)


def download_data(oss_path: str, local_path: str, bucket: oss2.Bucket, un_tar=False):
    """Download OSS objects to local path.

    Args:
        oss_path (str): Source OSS path, could be a single OSS object or a OSS
            directory.
        local_path (str): Local path used to store the data from OSS.
        bucket (oss2.Bucket): OSS Bucket that store the original data.
        un_tar (bool, optional): Whether to decompress the downloaded data. It is only
            work for `oss_path` point to a single file that has a suffix "tar.gz".

    Returns:
        str: A local file path for the downloaded data.

    """
    if not bucket.object_exists(oss_path) or oss_path.endswith("/"):
        # The `oss_path` is representing a "directory" in the OSS bucket, download the
        # objects which object key is prefixed with `oss_path`.
        # Note: `un_tar` is not work while `oss_path` is a directory.

        oss_path += "/" if not oss_path.endswith("/") else ""
        iterator = oss2.ObjectIteratorV2(
            bucket=bucket,
            prefix=oss_path,
        )
        keys = [obj.key for obj in iterator if not obj.key.endswith("/")]
        for key in keys:
            rel_path = os.path.relpath(key, oss_path)
            dest = os.path.join(local_path, rel_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            bucket.get_object_to_file(key, dest)
        return local_path
    else:
        # The `oss_path` is representing a single file in OSS bucket.
        if oss_path.endswith(".tar.gz") and un_tar:
            # currently, only tar.gz format is supported for un_tar after downloading.
            with tempfile.TemporaryDirectory() as temp_dir:
                target_path = os.path.join(temp_dir, os.path.basename(oss_path))
                bucket.get_object_to_file(oss_path, target_path)
                with tarfile.open(name=target_path, mode="r") as t:
                    t.extractall(path=local_path)

            return local_path
        else:
            os.makedirs(local_path, exist_ok=True)
            dest = os.path.join(local_path, os.path.basename(oss_path))
            bucket.get_object_to_file(oss_path, dest)
            return dest


class OssUriObj(object):
    """A class that represent an OSS URI and provide some convenient methods."""

    def __init__(self, uri):
        """Constructor for class OssUriObj.

        Args:
            uri (str): A string in OSS URI schema: oss://<bucket_name>[.endpoint]/<path/to/file>,
                endpoint in url is optional.
        """
        if not uri.startswith("oss://"):
            raise ValueError(
                "Invalid OSS uri schema, please provide a string starts with 'oss://'"
            )
        bucket_name, object_key, endpoint, role_arn = self.parse(uri)
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.endpoint = endpoint
        self.role_arn = role_arn

    @classmethod
    def from_bucket_key_endpoint(
        cls, bucket_name: str, object_key: str, endpoint: Optional[str] = None
    ) -> "OssUriObj":
        """Initialize an OSSUri object from bucket_name, object_key and endpoint.

        Args:
            bucket_name (str): The name of the OSS bucket.
            object_key (str): OSS object key/path.
            endpoint (str, optional): Endpoint for the OSS bucket.

        Returns:
            OssUriObj:

        """

        # OSS object key could not contain leading slashes.
        # Document: https://help.aliyun.com/document_detail/273129.html
        object_key = object_key.lstrip("/")
        if endpoint:
            if endpoint.startswith("http://"):
                endpoint = endpoint.lstrip("http://")
            elif endpoint.startswith("https://"):
                endpoint = endpoint.lstrip("https://")

            uri = f"oss://{bucket_name}.{endpoint}/{object_key}"
        else:
            uri = f"oss://{bucket_name}/{object_key}"
        return OssUriObj(uri=uri)

    @classmethod
    def parse(cls, oss_uri: str) -> Tuple[str, str, str, str]:
        """Parse OSS uri string and returns a tuple of [bucket_name, object_key, endpoint, role_arn].

        Args:
            oss_uri (str): A string in OSS Uri schema: oss://{bucket_name}.{endpoint}/{object_key}.

        Returns:
            Tuple: An tuple of [bucket_name, object_key, endpoint, role_arn].

        """
        parsed_result = parse.urlparse(oss_uri)
        if parsed_result.scheme != "oss":
            raise ValueError(
                "require OSS url('oss://[bucket_name]/[object_key]') but given '{}'".format(
                    oss_uri
                )
            )
        object_key = parsed_result.path
        if object_key.startswith("/"):
            object_key = object_key[1:]

        query = parse.parse_qs(parsed_result.query)
        if "." in parsed_result.hostname:
            bucket_name, endpoint = parsed_result.hostname.split(".", 1)
        else:
            bucket_name = parsed_result.hostname
            # try to get OSS endpoint from url query.
            if "endpoint" in query:
                endpoint = query.get("endpoint")[0]
            elif "host" in query:
                endpoint = query.get("host")[0]
            else:
                endpoint = None
        role_arn = query.get("role_arn")[0] if "role_arn" in query else None

        return bucket_name, object_key, endpoint, role_arn

    def get_uri_with_endpoint(self, endpoint: str = None) -> str:
        """Get an OSS uri string contains endpoint.

        Args:
            endpoint (str): Endpoint of the OSS bucket.

        Returns:
            str: An string in OSS uri schema contains endpoint.

        """
        if not endpoint and not self.endpoint:
            raise ValueError("Unknown endpoint for the OSS bucket.")

        return "oss://{bucket_name}.{endpoint}/{object_key}".format(
            bucket_name=self.bucket_name,
            endpoint=endpoint or self.endpoint,
            object_key=self.object_key,
        )

    def get_dir_uri(self):
        """Returns directory in OSS uri string format of the original object."""
        _, dirname, _ = self.parse_object_key()
        dir_uri = f"oss://{self.bucket_name}{dirname}"
        return dir_uri

    @property
    def uri(self) -> str:
        """Returns OSS uri in string format."""
        return "oss://{bucket_name}/{object_key}".format(
            bucket_name=self.bucket_name,
            object_key=self.object_key,
        )

    def parse_object_key(self) -> Tuple[bool, str, str]:
        """Parse the OSS URI object key, returns a tuple of (is_dir, dir_path, file_name).

        Returns:
            namedtuple: An tuple of is_dir, dir_path, file_name.
        """
        object_key = self.object_key.strip()
        if object_key.endswith("/"):
            is_dir, dir_path, file_name = True, os.path.join("/", object_key), None
        else:
            idx = object_key.rfind("/")
            if idx < 0:
                is_dir, dir_path, file_name = False, "/", object_key
            else:
                is_dir, dir_path, file_name = (
                    False,
                    os.path.join("/", object_key[: idx + 1]),
                    object_key[idx + 1 :],
                )
        return is_dir, dir_path, file_name
