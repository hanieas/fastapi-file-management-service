from main import app
from unittest.mock import patch, MagicMock

def test_file_is_required(test_app):
    
    pass

def test_file_size_is_required(test_app):
    pass

def test_credential_is_required(test_app):
    pass

def test_upload_file_invalid_type(test_app):
    pass

def test_upload_file_invalid_size(test_app):
    pass

# @patch("services..minioStorage")
def test_upload_file(test_app):
    # mock_minio_storage.putObject = MagicMock(return_value=None)
    files = {'file': ('testfile.txt', b'This is test file content', 'text/plain')}
    response = test_app.post(
        "/api/upload",
        files=files
    )
    assert response.status_code == 200

def test_upload_public_with_no_credential(test_app):
    pass

def test_upload_private_with_credential(test_app):
    pass
