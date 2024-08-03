from services.file_service import FileService
from fastapi import UploadFile
from dto.file_dto import UploadFilePayload, FileResponseDTO
from handlers.base_handler import BaseHandler
from api.response.errors import ValidatonErrors, ResponseErrors
from fastapi.responses import JSONResponse
import json


class FileHandler(BaseHandler[FileService]):
    def __init__(self, service: FileService) -> None:
        super().__init__(service=service)

    async def upload_file(self, file: UploadFile, credential: str, detail: str, size: int) -> JSONResponse:
        if credential:
            try:
                credential_dict = json.loads(credential)
            except json.JSONDecodeError:
                return self.response.error(data={}, error=ValidatonErrors.INVALID_JSON_CREDENTIAL, status=422)
        else:
            credential_dict = None

        if detail:
            try:
                detail_dict = json.loads(detail)
            except json.JSONDecodeError:
                return self.response.error(data={}, error=ValidatonErrors.INVALID_JSON_DETAIL, status=422)
        else:
            detail_dict = None

        payload = UploadFilePayload(file=file.file, filename=file.filename, content_type=file.content_type, detail=detail_dict,
                                    credential=credential_dict, size=size)
        file, error = await self.service.file_upload(payload=payload)
        if error:
            return self.response.error(data={}, error=ResponseErrors.BAD_REQUEST)
        download_url = await self.service.generate_download_link(file)
        data = FileResponseDTO(id=file.id, path=file.path, credential=file.credential,
                               content_type=file.content_type, detail=file.detail, download_url=download_url)
        return self.response.success(data=data.to_dict())
