from io import BytesIO

FILE_ENDPOINT = "/api/v1/file"
CHUNK_SIZE = 1024

def validate_success_response_structure(response_json):
    assert "data" in response_json, "Missing 'data' in response JSON"
    assert "message" in response_json, "Missing 'message' in response JSON"
    assert "success" in response_json, "Missing 'success' in response JSON"
    assert response_json["success"] == True


def validate_error_response_structure(response_json):
    assert "errors" in response_json, "Missing 'errors' in response JSON"
    assert "message" in response_json, "Missing 'message' in response JSON"
    assert "success" in response_json, "Missing 'success' in response JSON"
    assert response_json["success"] == False


def generate_file(chunk_size):
    file_content = b"0" * chunk_size
    file = BytesIO(file_content)
    file.name = "chunka"
    return file
