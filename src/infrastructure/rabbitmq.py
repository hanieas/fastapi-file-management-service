from typing import Self


class RabbitMQ:

    _instance: Self = None

    def __new__(cls: Self) -> Self:
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance


rabbitMQ = RabbitMQ()
