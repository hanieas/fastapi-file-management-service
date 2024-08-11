from infrastructure.db.mysql import mysql as db
from sqlalchemy import Column, Text, TIMESTAMP, String, BLOB, Integer, BigInteger

class CeleryTask(db.Base):
    __tablename__ = "celery_tasks"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(String(255), nullable=False, unique=True, index=True)
    status = Column(String(50), nullable=False)
    result = Column(BLOB)
    date_done = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')
    traceback = Column(Text)
    meta = Column(Text)
    name = Column(String(155))
    args = Column(BLOB)
    kwargs = Column(BLOB)
    worker = Column(String(155))
    retries = Column(Integer)
    queue = Column(String(155))