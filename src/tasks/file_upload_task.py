from . import celery, minioStorage, config, os


@celery.task
def upload_file_task(bucket: str, upload_id: str, total_chunks: int, filename: str):
    upload_dir = os.path.join(config.APP_UPLOAD_DIR, upload_id)
    final_file_path = os.path.join(upload_dir, "final_file")
    with open(final_file_path, "wb") as final_file:
        for i in range(total_chunks):
            chunk_path = os.path.join(upload_dir, f"{i}.part")
            with open(chunk_path, "rb") as chunk_file:
                content = chunk_file.read()
                final_file.write(content)
            os.remove(chunk_path)
    with open(final_file_path, 'rb') as file:
        minioStorage.put_object(bucket, filename, file,
                                length=-1, part_size=10 * 1024 * 1024)

    os.remove(final_file_path)
    os.removedirs(upload_dir)
