from infrastructure.mysql import mysql as db
from sqlalchemy import Column, BINARY, String, JSON, Integer, VARCHAR
import uuid

class File(db.Base):
    __tablename__ = "files"
    uuid = Column(BINARY(16),primary_key = True, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    credential = Column(JSON)
    path = Column(VARCHAR(255))
    content_type = Column(String(32))
    size = Column(Integer)
    detail = Column(JSON) 

    