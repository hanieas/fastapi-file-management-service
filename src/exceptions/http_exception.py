from fastapi import status as http_status
from constants.errors import Errors

class BaseException(Exception):
    def __init__(self, message: str, status: int) -> None:
        self.message = message
        self.status = status
        super().__init__(self.message, self.status)

class PermissionException(BaseException):
    def __init__(self) -> None:
        message = Errors.Permission_DENIED
        status = http_status.HTTP_403_FORBIDDEN
        super().__init__(message, status)

class FileNotFoundException(BaseException):
    def __init__(self) -> None:
        message = Errors.NOT_FOUND
        status = http_status.HTTP_404_NOT_FOUND
        super().__init__(message, status)

class FileUploadedException(BaseException):
    def __init__(self) -> None:
        message = Errors.FILE_UPLOADED_SUCCESSFULLY
        status = http_status.HTTP_400_BAD_REQUEST
        super().__init__(message, status)

class FilePendingUploadException(BaseException):
    def __init__(self) -> None:
        message = Errors.FILE_PENDING_UPLOAD
        status = http_status.HTTP_400_BAD_REQUEST
        super().__init__(message, status)