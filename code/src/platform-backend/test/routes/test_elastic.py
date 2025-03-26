import pytest
from fastapi import HTTPException, APIRouter
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Create a TestClient instance for simulating HTTP requests
router = APIRouter()
client = TestClient(router)


# Mock Elasticsearch client
@pytest.fixture
def mock_elasticsearch():
    with patch("app.main.get_elasticsearch_client") as mock_es:
        es_instance = MagicMock()
        mock_es.return_value = es_instance
        yield es_instance


# Test startup event (index creation)
def test_startup_event_creates_index(mock_elasticsearch):
    mock_elasticsearch.indices.exists.return_value = False
    mock_elasticsearch.indices.create.return_value = {"acknowledged": True}

    # Simulate the startup event
    from app.routes.elastic import startup_event
    startup_event()

    # Assertions
    mock_elasticsearch.indices.exists.assert_called_once_with(index="user_rule_analytics")
    mock_elasticsearch.indices.create.assert_called_once()


# Test pushing a record
def test_push_record_success(mock_elasticsearch):
    mock_elasticsearch.index.return_value = {"result": "created"}

    # Simulate a POST request to push a record
    response = client.post(
        "/push-record",
        json={
            "id": "1",
            "message": "Welcome to the Incidents Page!",
            "page": "incidents",
            "dataId": "1234"
        }
    )

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Record with ID 1 pushed successfully."}
    mock_elasticsearch.index.assert_called_once()


# Test retrieving a record by ID
def test_get_record_success(mock_elasticsearch):
    mock_elasticsearch.get.return_value = {
        "_id": "1",
        "_source": {
            "message": "Welcome to the Incidents Page!",
            "page": "incidents",
            "dataId": "1234"
        }
    }

    # Simulate a GET request to retrieve a record
    response = client.get("/get-record/1")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "message": "Welcome to the Incidents Page!",
        "page": "incidents",
        "dataId": "1234"
    }
    mock_elasticsearch.get.assert_called_once_with(index="user_rule_analytics", id="1")


# Test retrieving a non-existent record
def test_get_record_not_found(mock_elasticsearch):
    mock_elasticsearch.get.side_effect = Exception("NotFoundError")

    # Simulate a GET request to retrieve a non-existent record
    response = client.get("/get-record/999")

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "Record with ID 999 not found."}


# Test retrieving all records
def test_get_all_records_success(mock_elasticsearch):
    mock_elasticsearch.search.return_value = {
        "hits": {
            "hits": [
                {"_id": "1", "_source": {"message": "Record 1"}},
                {"_id": "2", "_source": {"message": "Record 2"}}
            ]
        }
    }

    # Simulate a GET request to retrieve all records
    response = client.get("/get-all-records")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "records": [
            {"id": "1", "message": "Record 1"},
            {"id": "2", "message": "Record 2"}
        ]
    }
    mock_elasticsearch.search.assert_called_once()


# Test error handling in push_record
def test_push_record_error(mock_elasticsearch):
    mock_elasticsearch.index.side_effect = Exception("Some error")

    # Simulate a POST request to push a record
    response = client.post(
        "/push-record",
        json={
            "id": "1",
            "message": "Welcome to the Incidents Page!",
            "page": "incidents",
            "dataId": "1234"
        }
    )

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"detail": "Error pushing record: Some error"}


# Test error handling in get_all_records
def test_get_all_records_error(mock_elasticsearch):
    mock_elasticsearch.search.side_effect = Exception("Some error")

    # Simulate a GET request to retrieve all records
    response = client.get("/get-all-records")

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"detail": "Error retrieving records: Some error"}