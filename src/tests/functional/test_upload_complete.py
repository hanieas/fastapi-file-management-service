from tests.test_utils import *
import uuid
from fastapi import status


def test_init_required_before_upload_complete(test_app):
    response = test_app.post(f"{FILE_ENDPOINT}/upload/complete/", data={
        "total_chunks": 1,
        "upload_id": str(uuid.uuid4()),
        "total_size": CHUNK_SIZE,
        "file_extension": "jpg",
        "content_type": "image/jpeg",
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_total_chunks_is_required(test_app):
    response = test_app.post(f"{FILE_ENDPOINT}/upload/complete/", data={
        "upload_id": str(uuid.uuid4()),
        "total_size": CHUNK_SIZE,
        "file_extension": "jpg",
        "content_type": "image/jpeg",
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_upload_id_is_required(test_app):
    response = test_app.post(f"{FILE_ENDPOINT}/upload/complete/", data={
        "total_chunks": 1,
        "total_size": CHUNK_SIZE,
        "file_extension": "jpg",
        "content_type": "image/jpeg",
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_total_size_is_required(test_app):
    response = test_app.post(f"{FILE_ENDPOINT}/upload/complete/", data={
        "total_chunks": 1,
        "upload_id": str(uuid.uuid4()),
        "file_extension": "jpg",
        "content_type": "image/jpeg",
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_file_extension_is_required(test_app):
    response = test_app.post(f"{FILE_ENDPOINT}/upload/complete/", data={
        "total_chunks": 1,
        "upload_id": str(uuid.uuid4()),
        "total_size": CHUNK_SIZE,
        "content_type": "image/jpeg",
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_file_extension_should_be_valid(test_app):
    response = test_app.post(f"{FILE_ENDPOINT}/upload/complete/", data={
        "total_chunks": 1,
        "upload_id": str(uuid.uuid4()),
        "total_size": CHUNK_SIZE,
        "file_extension": "jpge",
        "content_type": "image/jpeg",
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_content_type_is_required(test_app):
    response = test_app.post(f"{FILE_ENDPOINT}/upload/complete/", data={
        "total_chunks": 1,
        "upload_id": str(uuid.uuid4()),
        "total_size": CHUNK_SIZE,
        "file_extension": "jpg",
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_credential_should_be_valid(test_app):
    response = test_app.post(f"{FILE_ENDPOINT}/upload/complete/", data={
        "total_chunks": 1,
        "upload_id": str(uuid.uuid4()),
        "total_size": CHUNK_SIZE,
        "file_extension": "jpg",
        "content_type": "image/jpeg",
        "credential": '{"user": {"name": "", "id": "1"}}'
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())


def test_detail_should_be_valid(test_app):
    response = test_app.post(f"{FILE_ENDPOINT}/upload/complete/", data={
        "total_chunks": 1,
        "upload_id": str(uuid.uuid4()),
        "total_size": CHUNK_SIZE,
        "file_extension": "jpg",
        "content_type": "image/jpeg",
        "detail": '{"chunk": {"count": 1, "size": 1024}}'
    }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    validate_error_response_structure(response_json=response.json())
