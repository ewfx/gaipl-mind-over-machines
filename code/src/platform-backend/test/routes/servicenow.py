import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException, APIRouter
from app.main import router  # Adjust the import based on your file structure

# Create a TestClient instance for simulating HTTP requests
router = APIRouter()
client = TestClient(router)



# Mock ServiceNow API response
@pytest.fixture
def mock_servicenow_api():
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": [
                {
                    "sys_id": "12345",
                    "number": "INC00001",
                    "short_description": "Critical Incident",
                    "description": "This is a test incident.",
                    "cause": "Unknown",
                    "opened_at": "2023-10-01T12:00:00Z",
                    "severity": "1",
                    "incident_state": "6",
                    "closed_at": "2023-10-02T12:00:00Z"
                }
            ]
        }
        mock_get.return_value = mock_response
        yield mock_get


# Test fetch_incidents function
def test_fetch_incidents(mock_servicenow_api):
    incidents = fetch_incidents()
    assert isinstance(incidents, dict)
    assert "result" in incidents
    assert len(incidents["result"]) > 0
    assert incidents["result"][0]["number"] == "INC00001"


# Test map_incident_fields function
def test_map_incident_fields():
    incident_json = {
        "sys_id": "12345",
        "number": "INC00001",
        "short_description": "Critical Incident",
        "description": "This is a test incident.",
        "cause": "Unknown",
        "opened_at": "2023-10-01T12:00:00Z",
        "severity": "1",
        "incident_state": "6",
        "closed_at": "2023-10-02T12:00:00Z"
    }

    mapped_incident = map_incident_fields(incident_json)
    assert mapped_incident["sysId"] == "12345"
    assert mapped_incident["IncidentId"] == "INC00001"
    assert mapped_incident["priority"] == "Critical"
    assert mapped_incident["status"] == "Resolved"


# Test /servicenow_incidents endpoint
def test_servicenow_incidents(mock_servicenow_api):
    response = client.get("/servicenow_incidents")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/csv"
    assert response.headers["Content-Disposition"] == "attachment; filename=incidents.csv"

    # Decode CSV content
    csv_content = response.content.decode("utf-8")
    lines = csv_content.splitlines()

    # Verify CSV header
    assert lines[0] == "sysId,IncidentId,title,description,rootCause,createdDate,priority,status,closedDate"

    # Verify CSV data
    assert "12345,INC00001,Critical Incident,This is a test incident.,Unknown,2023-10-01T12:00:00Z,Critical,Resolved,2023-10-02T12:00:00Z" in csv_content


# Test error handling in fetch_incidents
def test_fetch_incidents_error():
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Mocked error")

        with pytest.raises(HTTPException) as exc_info:
            fetch_incidents()

        assert exc_info.value.status_code == 500
        assert "ServiceNow API error" in exc_info.value.detail


# Test error handling in /servicenow_incidents endpoint
def test_servicenow_incidents_error(mock_servicenow_api):
    mock_servicenow_api.side_effect = Exception("Mocked error")

    response = client.get("/servicenow_incidents")
    assert response.status_code == 500
    assert "An error occurred while processing the request" in response.json()["detail"]