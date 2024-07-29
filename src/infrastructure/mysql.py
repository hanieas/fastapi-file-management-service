from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.config import config

class MySQLDB:
    def __init__(self) -> None:
        self.engine = create_engine(str(config.MYSQL_DATABASE_URL))
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    @property
    def session(self):
        return self.SessionLocal
    
mysql = MySQLDB()