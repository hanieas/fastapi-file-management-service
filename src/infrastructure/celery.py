from celery import Celery as CeleryBase
from core.config import config
from typing import Self


class Celery:
    _instance: Self = None

    def __new__(cls: Self) -> Self:
        if cls._instance == None:
            cls._instance = CeleryBase(
                'tasks', broker=str(config.RABBITMQ_ENDPOINT))
        return cls._instance


celery = Celery()
