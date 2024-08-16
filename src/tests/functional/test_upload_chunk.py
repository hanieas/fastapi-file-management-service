from fastapi import status
from tests.test_utils import *
import uuid


def test_init_required_before_upload_chunk(test_app):
    file = generate_file(CHUNK_SIZE)
    response = test_app.post(f"{FILE_ENDPOINT}/upload/chunk/", files={
        "file": (file.name, file, "application/octet-stream")}, data={
        "chunk_size": CHUNK_SIZE,
        "upload_id": str(uuid.uuid4()),
        "chunk_index": 0
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_chunk_file_is_required(test_app):
    response = test_app.post(f"{FILE_ENDPOINT}/upload/chunk/", data={
        "chunk_size": CHUNK_SIZE,
        "upload_id": str(uuid.uuid4()),
        "chunk_index": 0
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_chunk_size_is_required(test_app):
    file = generate_file(CHUNK_SIZE)
    response = test_app.post(f"{FILE_ENDPOINT}/upload/chunk/", files={
        "file": (file.name, file, "application/octet-stream")}, data={
        "upload_id": str(uuid.uuid4()),
        "chunk_index": 0
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_upload_id_is_required(test_app):
    file = generate_file(CHUNK_SIZE)
    response = test_app.post(f"{FILE_ENDPOINT}/upload/chunk/", files={
        "file": (file.name, file, "application/octet-stream")}, data={
        "chunk_size": CHUNK_SIZE,
        "chunk_index": 0
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_chunk_index_is_required(test_app):
    file = generate_file(CHUNK_SIZE)
    response = test_app.post(f"{FILE_ENDPOINT}/upload/chunk/", files={
        "file": (file.name, file, "application/octet-stream")}, data={
        "upload_id": str(uuid.uuid4()),
        "chunk_size": CHUNK_SIZE,
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_chunk_upload(test_app):
    init_upload_response = test_app.post(f"{FILE_ENDPOINT}/upload/init")
    upload_id = init_upload_response.json()['data']['upload_id']
    file = generate_file(CHUNK_SIZE)

    response = test_app.post(f"{FILE_ENDPOINT}/upload/chunk/", files={
        "file": (file.name, file, "application/octet-stream")}, data={
        "upload_id": upload_id,
        "chunk_size": CHUNK_SIZE,
        "chunk_index": 0
    }
    )
    assert response.status_code == status.HTTP_200_OK
    validate_success_response_structure(response_json=response.json())
