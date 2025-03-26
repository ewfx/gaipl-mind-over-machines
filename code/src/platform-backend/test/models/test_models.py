import pytest
from app.models.incident_model import IncidentSummary, IncidentMetrics, IncidentTableEntry


# Test IncidentSummary Model
def test_incident_summary():
    # Valid data
    valid_data = {
        "color": "red",
        "title": "Critical Incident",
        "status": "Open",
        "priority": "High",
        "system": "Backend",
        "reportedTime": "2023-10-01T12:00:00Z"
    }
    incident = IncidentSummary(**valid_data)
    assert incident.color == "red"
    assert incident.title == "Critical Incident"

    # Invalid data (missing required fields)
    invalid_data = {
        "color": "red",
        "title": "Critical Incident",
        "status": "Open",
        "priority": "High",
        "system": "Backend"
        # Missing 'reportedTime'
    }
    with pytest.raises(ValueError):
        IncidentSummary(**invalid_data)


# Test IncidentMetrics Model
def test_incident_metrics():
    # Valid data
    valid_data = {
        "timestamps": ["2023-10-01", "2023-10-02"],
        "incidentCount": [5, 10],
        "severityLevels": ["Low", "Medium"],
        "severityCounts": [3, 7],
        "resolutionTimes": [60, 120],
        "types": ["Bug", "Outage"],
        "typeCounts": [2, 8]
    }
    metrics = IncidentMetrics(**valid_data)
    assert metrics.timestamps == ["2023-10-01", "2023-10-02"]
    assert metrics.incidentCount == [5, 10]

# Test IncidentTableEntry Model
def test_incident_table_entry():
    # Valid data
    valid_data = {
        "avatar": {"url": "http://example.com/avatar.png"},
        "incident": {"id": "12345", "name": "Server Down"},
        "component": "Database",
        "progress": {"value": 75, "label": "In Progress"},
        "priority": "High",
        "activity": "Resolved"
    }
    entry = IncidentTableEntry(**valid_data)
    assert entry.avatar == {"url": "http://example.com/avatar.png"}
    assert entry.incident["id"] == "12345"

    # Invalid data (missing required fields)
    invalid_data = {
        "avatar": {"url": "http://example.com/avatar.png"},
        "incident": {"id": "12345", "name": "Server Down"},
        "component": "Database",
        "progress": {"value": 75, "label": "In Progress"},
        "priority": "High"
        # Missing 'activity'
    }
    with pytest.raises(ValueError):
        IncidentTableEntry(**invalid_data)