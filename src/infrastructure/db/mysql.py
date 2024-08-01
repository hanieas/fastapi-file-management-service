from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.config import config
from typing import TypeVar, Type

T = TypeVar('T', bound='MySQLDB')

class MySQLDB:
    _instance: T = None

    def __new__(cls: Type[T]) -> T:
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialize()
        return cls._instance

    def __initialize(self) -> None:
        self.engine = create_engine(str(config.MYSQL_DATABASE_URL))
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    @property
    def session(self):
        return self.SessionLocal
    
mysql = MySQLDB()