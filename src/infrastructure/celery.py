from celery import Celery as CeleryBase
from core.config import config
from typing import Self


class Celery:
    _instance: Self = None

    def __new__(cls: Self) -> Self:
        if cls._instance == None:
            cls._instance = CeleryBase(
                'tasks', broker=str(config.RABBITMQ_ENDPOINT), backend=str(config.CELERY_BACKEND_ENDPOINT))
        return cls._instance


celery = Celery()
celery.conf.database_engine_options = {'echo': True}
celery.conf.database_table_names = {'task': 'celery_tasks'}
celery.conf.update(result_extended=True)