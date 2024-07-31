import os
import pytest
from fastapi.testclient import TestClient
from main import create_application

os.environ["ENV"] = "testing"

@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    with TestClient(app) as test_client:
        yield test_client