from api.response.json_response import Response
from typing import TypeVar, Type, Generic

T = TypeVar('T')


class BaseHandler(Generic[T]):
   def __init__(self, service: Type[T]) -> None:
      self.service = service
      self.response = Response()
