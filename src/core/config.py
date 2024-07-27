import os

class Config:
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    MINIO_PUBLIC_BUCKET = os.getenv('MINIO_PUBLIC_BUCKET', 'public')
    MINIO_PRIVATE_BUCKET = os.getenv('MINIO_PRIVATE_BUCKET', 'private')

config = Config()