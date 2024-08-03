from typing import Type, Generic, TypeVar
from infrastructure.db.mysql import MySQLDB

T = TypeVar("T")

class BaseRepo(Generic[T]):
    def __init__(self, model: Type[T], db: MySQLDB) -> None:
        self.model = model
        self.db = db
        self.session = self.db.session
        
    def create(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity
    
    def get(self, id: str) -> T:
        return self.session.query(self.model).filter(self.model.id == id).first()