import pytest
from fastapi import HTTPException, APIRouter
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

router = APIRouter()
client = TestClient(router)


# Mock Elasticsearch client
@pytest.fixture
def mock_elasticsearch():
    with patch("app.main.es") as mock_es:
        yield mock_es


# Mock SentenceTransformer model
@pytest.fixture
def mock_sentence_transformer():
    with patch("app.main.model") as mock_model:
        mock_model.encode.return_value = [0.1] * 384  # Mock embedding vector
        yield mock_model


# Test index creation
def test_index_creation(mock_elasticsearch):
    mock_elasticsearch.indices.exists.return_value = False
    mock_elasticsearch.indices.create.return_value = {"acknowledged": True}

    # Simulate index creation logic
    from app.routes.elasticIncidents import index_name
    assert not mock_elasticsearch.indices.exists(index=index_name)
    mock_elasticsearch.indices.create.assert_called_once()


# Test delete_index endpoint
def test_delete_index(mock_elasticsearch):
    mock_elasticsearch.indices.exists.return_value = True
    mock_elasticsearch.indices.delete.return_value = {"acknowledged": True}

    response = client.delete("/delete_index")
    assert response.status_code == 200
    assert response.json() == {"message": f"Index 'incidents_final' deleted successfully."}


# Test get_incidents endpoint
def test_get_incidents(mock_elasticsearch):
    mock_elasticsearch.search.return_value = {
        "hits": {
            "hits": [
                {
                    "_source": {
                        "IncidentId": "123",
                        "createdDate": "2023-10-01T12:00:00",
                        "priority": "High",
                        "status": "Resolved"
                    }
                }
            ]
        }
    }

    response = client.get("/incident_list?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["incident"]["name"] == "123"


# Test get_incident_by_id endpoint
def test_get_incident_by_id(mock_elasticsearch):
    mock_elasticsearch.search.return_value = {
        "hits": {
            "total": {"value": 1},
            "hits": [
                {
                    "_source": {
                        "IncidentId": "123",
                        "title": "Test Incident",
                        "description": "Test Description",
                        "rootCause": "Test Root Cause",
                        "createdDate": "2023-10-01T12:00:00",
                        "closedDate": "2023-10-02T12:00:00",
                        "priority": "High",
                        "status": "Resolved"
                    }
                }
            ]
        }
    }

    response = client.get("/incidents_elastic?incident_id=123")
    assert response.status_code == 200
    assert response.json()["IncidentId"] == "123"


# Test incidents_overview endpoint
def test_incidents_overview(mock_elasticsearch):
    mock_elasticsearch.search.return_value = {
        "hits": {
            "hits": [
                {
                    "_source": {
                        "title": "Test Incident",
                        "status": "Resolved",
                        "priority": "High",
                        "createdDate": "2023-10-01T12:00:00",
                        "closedDate": "2023-10-02T12:00:00",
                        "description": "network issue"
                    }
                }
            ]
        }
    }

    response = client.get("/incidents-overview")
    assert response.status_code == 200
    assert "summary" in response.json()
    assert "metrics" in response.json()


# Test index_incidents endpoint
@patch("pandas.read_csv")
def test_index_incidents(mock_read_csv, mock_elasticsearch, mock_sentence_transformer):
    mock_read_csv.return_value = MagicMock(
        columns=["sysId", "IncidentId", "title", "description", "rootCause", "createdDate", "priority", "status"],
        iterrows=lambda: [
            (
                0,
                {
                    "sysId": "1",
                    "IncidentId": "123",
                    "title": "Test Incident",
                    "description": "Test Description",
                    "rootCause": "Test Root Cause",
                    "createdDate": "2023-10-01 12:00:00",
                    "priority": "High",
                    "status": "Resolved",
                    "closedDate": None
                }
            )
        ]
    )

    response = client.post("/index_incidents", json={"file_path": "dummy.csv"})
    assert response.status_code == 200
    assert response.json() == {"message": "Incidents indexed successfully"}


# Test latest_incidents endpoint
def test_latest_incidents(mock_elasticsearch):
    mock_elasticsearch.search.return_value = {
        "hits": {
            "hits": [
                {
                    "_id": "1",
                    "_source": {
                        "IncidentId": "123",
                        "title": "Test Incident",
                        "description": "Test Description",
                        "rootCause": "Test Root Cause",
                        "createdDate": "2023-10-01T12:00:00",
                        "priority": "High",
                        "status": "Resolved"
                    }
                }
            ]
        }
    }

    response = client.get("/latest_incidents")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["data"]["IncidentId"] == "123"


# Test latest_seven_days_incidents endpoint
def test_latest_seven_days_incidents(mock_elasticsearch):
    mock_elasticsearch.search.side_effect = [
        {"hits": {"total": {"value": 100}}},  # Total incidents
        {"hits": {"hits": [{"_source": {"createdDate": "2023-10-01T12:00:00", "status": "Resolved"}}]}},  # Last 7 days
        {"hits": {"hits": [{"_source": {"createdDate": "2023-10-01T12:00:00", "closedDate": "2023-10-02T12:00:00"}}]}}  # Resolution times
    ]

    response = client.get("/latest_seven_days_incidents")
    assert response.status_code == 200
    assert "labels" in response.json()
    assert "datasets" in response.json()
    assert "percentage" in response.json()


# Test latest_six_months_incidents endpoint
def test_latest_six_months_incidents(mock_elasticsearch):
    mock_elasticsearch.search.return_value = {
        "aggregations": {
            "monthly_statuses": {
                "buckets": [
                    {
                        "key_as_string": "2023-10",
                        "New": {"doc_count": 5},
                        "Resolved": {"doc_count": 10},
                        "Closed": {"doc_count": 3}
                    }
                ]
            }
        }
    }

    response = client.get("/latest_six_months_incidents")
    assert response.status_code == 200
    assert "labels" in response.json()
    assert "datasets" in response.json()
    assert "progress" in response.json()


# Test add_exception endpoint
def test_add_exception(mock_elasticsearch, mock_sentence_transformer):
    exception_data = {
        "sysId": "1",
        "IncidentId": "123",
        "title": "Test Exception",
        "description": "Test Description",
        "rootCause": "Test Root Cause",
        "createdDate": "2023-10-01 12:00:00",
        "priority": "High"
    }

    response = client.post("/add_exception", json=exception_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Exception added successfully"}


# Test similarity_search endpoint
def test_similarity_search(mock_elasticsearch, mock_sentence_transformer):
    mock_elasticsearch.search.return_value = {
        "hits": {
            "hits": [
                {
                    "_id": "1",
                    "_score": 0.9,
                    "_source": {
                        "IncidentId": "123",
                        "title": "Test Incident",
                        "description": "Test Description",
                        "rootCause": "Test Root Cause",
                        "createdDate": "2023-10-01T12:00:00",
                        "priority": "High",
                        "status": "Resolved"
                    }
                }
            ]
        }
    }

    response = client.post("/similarity_search", json={"query_text": "Test Query", "size": 1})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == "1"