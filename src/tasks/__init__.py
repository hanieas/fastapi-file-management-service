from infrastructure.celery import celery
from infrastructure.minio import minioStorage
from core.config import config
import os

from . import file_upload_task

