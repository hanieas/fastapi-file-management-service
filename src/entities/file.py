from infrastructure.db.mysql import mysql as db
from sqlalchemy import Column, String, JSON, Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid


class File(db.Base):
    __tablename__ = "files"
    id = Column(VARCHAR(36), nullable=False, primary_key=True, unique=True,
                index=True, default=lambda: str(uuid.uuid4()))
    credential = Column(JSON(none_as_null=True))
    path = Column(VARCHAR(255), nullable=False)
    content_type = Column(String(32), nullable=False)
    size = Column(Integer)
    detail = Column(JSON(none_as_null=True))
    celery_task_id = Column(String(36))