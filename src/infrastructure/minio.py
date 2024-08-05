from datetime import timedelta
from core.config import config
from minio import Minio
from minio.helpers import ObjectWriteResult
from typing import Type, TypeVar

T = TypeVar('T', bound='MinioStorage')

class MinioStorage:

    _instance : T = None

    def __new__(cls: Type[T]) -> T:
        """
        `MinioStorage` class the main entrypoint to use minio
    
        ##  Example
        ```python
        from infrastructure.minio import MinioStorage

        minioStorage = MinioStorage()
        ```
        """
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialize()
        return cls._instance

    def __initialize(self) -> None:
        self.client = Minio(
            config.MINIO_ENDPOINT,
            access_key = config.MINIO_ACCESS_KEY,
            secret_key = config.MINIO_SECRET_KEY,
            secure = False,
        )
        self.public_bucket = config.MINIO_PUBLIC_BUCKET
        self.private_bucket = config.MINIO_PRIVATE_BUCKET
        
    def bucket_exists(self, bucket_name) -> bool:
        """
        Check if the bucket exists

        :param bucket_name: Name of the bucket
        """
        found = self.client.bucket_exists(bucket_name)
        if not found:
            return False
        return True

    def create_bucket(self, bucket_name, location: str | None = None, object_lock: bool = False,)-> None:
        """
        Create a bucket with given name and region and object lock

        :param bucket_name: Name of the bucket.
        :param location: Region in which the bucket will be created.
        :param object_lock: Flag to set object-lock feature.

        """
        self.client.make_bucket(bucket_name, location, object_lock)

    def put_object(self, bucket_name, object_name, data, length, content_type="application/octet-stream", metadate=None,
                  sse=None, progress=None, part_size=0, num_parallel_uploads=3, tags=None, retention=None, legal_hold=False) -> ObjectWriteResult:
        """
        Uploads data from a stream to an object in a bucket.

        :param bucket_name: Name of the bucket.
        :param object_name: Object name in the bucket.
        :param data: An object having callable read() returning bytes object.
        :param length: Data size; -1 for unknown size and set valid part_size.
        :param content_type: Content type of the object.
        :param metadata: Any additional metadata to be uploaded along
            with your PUT request.
        :param sse: Server-side encryption.
        :param progress: A progress object;
        :param part_size: Multipart part size.
        :param num_parallel_uploads: Number of parallel uploads.
        :param tags: :class:`Tags` for the object.
        :param retention: :class:`Retention` configuration object.
        :param legal_hold: Flag to set legal hold for the object.
        :return: :class:`ObjectWriteResult` object.
        """
        if not self.bucket_exists(bucket_name=bucket_name):
            self.create_bucket(bucket_name=bucket_name)
        return self.client.put_object(bucket_name, object_name, data, length, content_type, metadate, sse, progress, part_size,
                                num_parallel_uploads, tags, retention ,legal_hold)
    
    def get_presigned_url(self, method, bucket_name, object_name, expires=timedelta(days=7), response_headers=None, request_date=None, 
                        version_id=None, extra_query_params=None) -> str:
        """
        Get presigned URL of an object for HTTP method, expiry time and custom
        request parameters.

        :param method: HTTP method.
        :param bucket_name: Name of the bucket.
        :param object_name: Object name in the bucket.
        :param expires: Expiry in seconds; defaults to 7 days.
        :param response_headers: Optional response_headers argument to
                                 specify response fields like date, size,
                                 type of file, data about server, etc.
        :param request_date: Optional request_date argument to
                             specify a different request date. Default is
                             current date.
        :param version_id: Version ID of the object.
        :param extra_query_params: Extra query parameters for advanced usage.
        :return: URL string.
        """
        return self.client.get_presigned_url(method, bucket_name, object_name, expires, response_headers, request_date, version_id, extra_query_params)

    def get_url(self, bucket_name, object_name):
        return f"{config.MINIO_URL}/{bucket_name}/{object_name}"
    
minioStorage = MinioStorage()