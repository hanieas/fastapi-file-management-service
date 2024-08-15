from services.file_service import FileService
from fastapi import UploadFile, status
from constants.messages import Message
from dto.file_dto import UploadFileDTO, UploadChunkDTO, RetryUploadFileDTO
from api.responses.file_response import FileResponse, UploadInitResponse, UploadChunkResponse, UploadStatusResponse
from handlers.base_handler import BaseHandler
from api.responses.response import SuccessResponse, ErrorResponse
from fastapi.responses import JSONResponse
from exceptions.http_exception import BaseException
from constants.file_extensions import FileExtension
from constants.errors import Errors
from typing import Dict, Any
from core.config import config
from utils import parse_json_to_dict


class FileHandler(BaseHandler[FileService]):
    def __init__(self, service: FileService) -> None:
        super().__init__(service=service)

    async def upload_initialize(self):
        upload_id = await self.service.upload_initialize()
        return self.response.success(content=SuccessResponse[UploadInitResponse](data=UploadInitResponse(
            chunk_size=config.APP_MAX_CHUNK_SIZE,
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

    async def upload_complete(self, upload_id: str, total_chunks: int, total_size: int, file_extension: FileExtension,
                              content_type: str, credential: str, detail: str, size: int = 0) -> JSONResponse:
        if credential:
            credential_dict = parse_json_to_dict(credential, 'credential')
        else:
            credential_dict = None

        if detail:
            detail_dict = parse_json_to_dict(detail, 'detail')
        else:
            detail_dict = None
        payload = UploadFileDTO(upload_id=upload_id, total_chunks=total_chunks, total_size=total_size, file_extension=file_extension,
                                content_type=content_type, detail=detail_dict, credential=credential_dict, size=size)
        try:
            file = await self.service.upload_complete(payload=payload)
            download_url = await self.service.get_download_link(file)
            data = FileResponse(id=file.id, path=file.path, credential=file.credential,
                                content_type=file.content_type, detail=file.detail, download_url=download_url)
            return self.response.success(content=SuccessResponse[FileResponse](data=data))
        except FileNotFoundError as exc:
            return self.response.error(ErrorResponse(message=Errors.FILE_NOT_FOUND), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    async def get_file(self, file_id: str, credential=Dict[str, Any]) -> JSONResponse:
        try:
            file = await self.service.get_file(id=file_id, credential=credential)
            download_url = await self.service.get_download_link(file)
            data = FileResponse(id=file.id, path=file.path, credential=file.credential,
                                content_type=file.content_type, detail=file.detail, download_url=download_url)
            return self.response.success(SuccessResponse[FileResponse](data=data))
        except BaseException as exception:
            return self.response.error(ErrorResponse(message=exception.message), status=exception.status)

    async def get_upload_status(self, file_id: str, credential=Dict[str, Any]) -> JSONResponse:
        try:
            result = await self.service.get_upload_status(file_id=file_id, credential=credential)
            return self.response.success(SuccessResponse[UploadStatusResponse](data=UploadStatusResponse(status=result)))
        except BaseException as exception:
            return self.response.error(ErrorResponse(message=exception.message), status=exception.status)

    async def retry_upload(self, file_id: str, credential: str):
        if credential:
            credential_dict = parse_json_to_dict(credential, 'credential')
        else:
            credential_dict = None
        payload = RetryUploadFileDTO(id=file_id, credential=credential_dict)
        try:
            file = await self.service.retry_upload(payload=payload)
            download_url = await self.service.get_download_link(file)
            data = FileResponse(id=file.id, path=file.path, credential=file.credential,
                                content_type=file.content_type, detail=file.detail, download_url=download_url)
            return self.response.success(content=SuccessResponse[FileResponse](data=data))
        except BaseException as exception:
            return self.response.error(ErrorResponse(message=exception.message), status=exception.status)
