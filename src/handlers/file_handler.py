from services.file_service import FileService
from fastapi import UploadFile
from dto.file_dto import UploadFilePayload, FileResponseDTO
from handlers.base_handler import BaseHandler
from constants.errors import ValidatonErrors
from api.response import SuccessResponse, ErrorResponse
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from exceptions.http_exception import BaseException
import json
from minio.error import MinioException
from constants.errors import Errors
from typing import Dict, Any


class FileHandler(BaseHandler[FileService]):
    def __init__(self, service: FileService) -> None:
        super().__init__(service=service)

    async def upload_file(self, file: UploadFile, credential: str, detail: str, size: int) -> JSONResponse:
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

        payload = UploadFilePayload(file=file.file, filename=file.filename, content_type=file.content_type, detail=detail_dict,
                                    credential=credential_dict, size=size)
        try:
            file = await self.service.file_upload(payload=payload)
            download_url = await self.service.generate_download_link(file)
            data = FileResponseDTO(id=file.id, path=file.path, credential=file.credential,
                                   content_type=file.content_type, detail=file.detail, download_url=download_url)
            return self.response.success(content=SuccessResponse[FileResponseDTO](data=data))
        except MinioException as exc:
            return self.response.error(ErrorResponse(message=Errors.BAD_REQUEST))

    async def get_file(self, id: str, query_params=Dict[str, Any]) -> JSONResponse:
        try:
            file = await self.service.get_file(id=id, query_params=query_params)
            download_url = await self.service.generate_download_link(file)
            data = FileResponseDTO(id=file.id, path=file.path, credential=file.credential,
                                   content_type=file.content_type, detail=file.detail, download_url=download_url)
            return self.response.success(SuccessResponse[FileResponseDTO](data=data))

        except BaseException as exception:
            return self.response.error(ErrorResponse(message=exception.message, status=exception.status))
