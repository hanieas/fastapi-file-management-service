from typing import TypeVar, Generic, Type

T = TypeVar("T")

class BaseService(Generic[T]):
    def __init__(self, repo: Type[T]) -> None:
        self.repo = repo