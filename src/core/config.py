import os
from pydantic_core import MultiHostUrl
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_UPLOAD_DIR = os.getenv("APP_UPLOAD_DIR")
    APP_MAX_CHUNK_SIZE = int(os.getenv("APP_MAX_CHUNK_SIZE"))
    ENV = os.getenv("ENV")
    print("ENV:", ENV)

    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
    MINIO_URL = os.getenv("MINIO_URL")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    MINIO_PUBLIC_BUCKET = os.getenv('MINIO_PUBLIC_BUCKET', 'public')
    MINIO_PRIVATE_BUCKET = os.getenv('MINIO_PRIVATE_BUCKET', 'private')

    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD', 'password')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'db-mysql')
    MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "filemanager")
    MYSQL_TEST_DATABASE = os.getenv("MYSQL_TEST_DATABASE", "filemanager_test")

    @property
    def MYSQL_DATABASE_URL(self):
        if self.ENV == "testing":
            path = self.MYSQL_TEST_DATABASE
        else:
            path = self.MYSQL_DATABASE
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_HOST,
            port=int(self.MYSQL_PORT),
            path=path
        )
    @property
    def CELERY_BACKEND_ENDPOINT(self):
        if self.ENV == "testing":
            path = self.MYSQL_TEST_DATABASE
        else:
            path = self.MYSQL_DATABASE
        return MultiHostUrl.build(
            scheme="db+mysql+pymysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_HOST,
            port=int(self.MYSQL_PORT),
            path=path
        )

    RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER', 'root')
    RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS', 'password')
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '5672')

    @property
    def RABBITMQ_ENDPOINT(self):
        return MultiHostUrl.build(
            scheme="pyamqp",
            username=self.RABBITMQ_DEFAULT_USER,
            password=self.RABBITMQ_DEFAULT_PASS,
            host=self.RABBITMQ_HOST,
            port=int(self.RABBITMQ_PORT),
        )

config = Config()
