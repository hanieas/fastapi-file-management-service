from repositories.file_repository import FileRepo
from dto.file_dto import UploadFilePayload
from typing import Dict, Any
from entities.file import File
import os
import string
from datetime import datetime
import random
from infrastructure.minio import minioStorage
from dto.file_dto import FileBaseDTO
from services.base_service import BaseService
from exceptions.http_exception import PermissionException, FileNotFoundException

class FileService(BaseService[FileRepo]):
    def __init__(self, repo: FileRepo) -> None:
        super().__init__(repo=repo)

    async def file_upload(self, payload: UploadFilePayload) -> File:
        _, file_extension = os.path.splitext(payload.filename)
        filename = (
            "".join(random.choices((string.ascii_letters + string.digits), k=20))
            + datetime.now().strftime("%Y%m%d%H%M%S%f")
            + file_extension
        )
        if not payload.credential:
            bucket = minioStorage.public_bucket
        else:
            bucket = minioStorage.private_bucket
        minioStorage.put_object(
                bucket, filename, payload.file, length=-1, part_size=10 * 1024 * 1024)
        file = self.repo.create_file(FileBaseDTO(path=bucket + "/" + filename, content_type=payload.content_type, detail=payload.detail,
                                                     size=payload.size, credential=payload.credential))
        return file

    async def generate_download_link(self, file: File) -> str:
        bucket_name = file.path.split("/")[0]
        filename = "/".join(file.path.split("/")[1:])
        if not file.credential:
            return minioStorage.get_url(bucket_name=bucket_name, object_name=filename)
        else:
            for key, value in file.credential.items():
                if not isinstance(value, str):
                    file.credential[key] = str(value)
            return minioStorage.get_presigned_url("GET", bucket_name=bucket_name, object_name=filename, extra_query_params=file.credential)

    async def get_file(self, id: id, query_params=Dict[str, Any]) -> File:
        file = self.repo.get_file(id=id)
        if file == None:
            raise FileNotFoundException
        if file.credential:
            for key, value in file.credential.items():
                if not isinstance(value, str):
                    file.credential[key] = str(value)
            if query_params != file.credential:
                raise PermissionException()
        return file
