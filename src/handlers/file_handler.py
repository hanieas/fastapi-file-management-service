from services.file_service import FileService
from fastapi import UploadFile, status
from constants.messages import Message
from dto.file_dto import UploadFileDTO, UploadChunkDTO
from api.responses.file_response import FileResponse, UploadInitResponse, UploadChunkResponse
from handlers.base_handler import BaseHandler
from constants.errors import ValidatonErrors
from api.responses.response import SuccessResponse, ErrorResponse
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from exceptions.http_exception import BaseException
import json
from constants.file_extensions import FileExtension
from minio.error import MinioException
from constants.errors import Errors
from typing import Dict, Any
from core.config import config
import time


class FileHandler(BaseHandler[FileService]):
    def __init__(self, service: FileService) -> None:
        super().__init__(service=service)

    async def upload_initialize(self):
        upload_id = await self.service.upload_initialize()
        return self.response.success(content=SuccessResponse[UploadInitResponse](data=UploadInitResponse(
            chunck_size=config.APP_MAX_CHUNK_SIZE,
            upload_id=upload_id
        )))

    async def upload_chunk(self, chunk_size: int, upload_id: str, chunk_index: int, file: UploadFile):
        payload = UploadChunkDTO(
            chunk_size=chunk_size, file=file, upload_id=upload_id, chunk_index=chunk_index)
        try:
            await self.service.upload_chunk(payload)
            return self.response.success(content=SuccessResponse[UploadChunkResponse](
                data=UploadChunkResponse(chunk_index=chunk_index, upload_id=upload_id), message=Message.UPLOADED_CHUNK
            ))
        except FileNotFoundError as exc:
            return self.response.error(ErrorResponse(message=Errors.FILE_NOT_FOUND), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    async def upload_file(self, upload_id: str, total_chunks: int, total_size: int, file_extension: FileExtension,
                          content_type: str, credential: str, detail: str, size: int = 0) -> JSONResponse:
        if credential:
            try:
                credential_dict = json.loads(credential)
            except json.JSONDecodeError:
                raise RequestValidationError(errors=[{
                    'loc': ('body', 'credential'),
                    'msg': ValidatonErrors.INVALID_JSON_CREDENTIAL,
                    'type': 'value_error'
                }],
                    body={"credential": "invalid_format"})
        else:
            credential_dict = None

        if detail:
            try:
                detail_dict = json.loads(detail)
            except json.JSONDecodeError:
                raise RequestValidationError(errors=[{
                    'loc': ('body', 'detail'),
                    'msg': ValidatonErrors.INVALID_JSON_DETAIL,
                    'type': 'value_error'
                }],
                    body={"detail": "invalid_format"})
        else:
            detail_dict = None
        payload = UploadFileDTO(upload_id=upload_id, total_chunks=total_chunks, total_size=total_size, file_extension=file_extension,
                                content_type=content_type, detail=detail_dict, credential=credential_dict, size=size)
        try:
            file = await self.service.upload_file(payload=payload)
            download_url = await self.service.get_download_link(file)
            data = FileResponse(id=file.id, path=file.path, credential=file.credential,
                                content_type=file.content_type, detail=file.detail, download_url=download_url)
            return self.response.success(content=SuccessResponse[FileResponse](data=data))
        except FileNotFoundError as exc:
            return self.response.error(ErrorResponse(message=Errors.FILE_NOT_FOUND), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    async def get_file(self, id: str, query_params=Dict[str, Any]) -> JSONResponse:
        try:
            file = await self.service.get_file(id=id, query_params=query_params)
            download_url = await self.service.get_download_link(file)
            data = FileResponse(id=file.id, path=file.path, credential=file.credential,
                                content_type=file.content_type, detail=file.detail, download_url=download_url)
            return self.response.success(SuccessResponse[FileResponse](data=data))

        except BaseException as exception:
            return self.response.error(ErrorResponse(message=exception.message, status=exception.status))
