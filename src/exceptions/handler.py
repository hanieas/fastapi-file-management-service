from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.response import ErrorResponse, response

class ExceptionHandler:
    def __init__(self, app):
        self.app = app
        self.register_handlers()

    def register_handlers(self):
        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            details = exc.errors()
            modified_details = []
            for error in details:
                message = error['msg'].lower()
                location = "->".join(map(str, error['loc']))
                modified_details.append(f"[{location}] {message}")
            return response.error(
                content=ErrorResponse(errors=modified_details),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
