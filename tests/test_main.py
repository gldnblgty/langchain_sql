from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@patch('backend.main.Chain')  # Mocking the Chain dependency
def test_answer_endpoint(mock_chain):
    mock_chain.return_value.query.return_value = "Mocked response"
    response = client.post("/answer", json={"query": "Test query"})
    assert response.status_code == 200