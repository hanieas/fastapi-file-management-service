import os
import pytest
from fastapi.testclient import TestClient
from main import create_application

os.environ["ENV"] = "testing"

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    os.system("alembic downgrade base")
    os.system("alembic upgrade head")
    yield

@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    with TestClient(app) as test_client:
        yield test_client