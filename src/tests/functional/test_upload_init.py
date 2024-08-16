from fastapi import status
from tests.test_utils import *


def test_upload_initialize(test_app):
    response = test_app.post(f"{FILE_ENDPOINT}/upload/init")
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    validate_success_response_structure(response_json=response_json)
    assert "chunk_size" in response_json["data"]
    assert "upload_id" in response_json["data"]
