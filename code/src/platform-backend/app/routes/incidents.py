import logging

from fastapi import APIRouter, HTTPException
from app.services.service_now import fetch_incidents
from app.models.incident_model import IncidentSummary
from app.models.incident_model import IncidentMetrics
from app.models.incident_model import IncidentTableEntry
from app.routes.elasticclient import get_elasticsearch_client

router = APIRouter()

es = get_elasticsearch_client()

incident_status = {
    "labels": ["October", "November", "December", "January", "February", "March"],
    "datasets": [
        {
            "label": "New",
            "backgroundColor": "rgba(0, 123, 255, 0.1)",  # Example RGB color
            "borderColor": "#007bff",
            "pointHoverBackgroundColor": "#007bff",
            "borderWidth": 2,
            "data": [19, 25, 24, 20, 25, 26],
            "fill": True
        },
        {
            "label": "In Progress",
            "backgroundColor": "transparent",
            "borderColor": "#6610f2",
            "pointHoverBackgroundColor": "#6610f2",
            "borderWidth": 2,
            "data": [11, 13, 12, 10, 9, 7]
        },
        {
            "label": "On Hold",
            "backgroundColor": "transparent",
            "borderColor": "#ffc107",
            "pointHoverBackgroundColor": "#ffc107",
            "borderWidth": 1,
            "borderDash": [8, 5],
            "data": [5, 7, 8, 3, 9, 2]
        },
        {
            "label": "Resolved",
            "backgroundColor": "transparent",
            "borderColor": "#28a745",
            "pointHoverBackgroundColor": "#28a745",
            "borderWidth": 1,
            "borderDash": [8, 5],
            "data": [15, 20, 21, 16, 15, 18]
        },
        {
            "label": "Closed",
            "backgroundColor": "transparent",
            "borderColor": "#6610f2",
            "pointHoverBackgroundColor": "#6610f2",
            "borderWidth": 1,
            "borderDash": [8, 5],
            "data": [18, 26, 25, 19, 27, 29]
        },
        {
            "label": "Cancelled",
            "backgroundColor": "transparent",
            "borderColor": "#dc3545",
            "pointHoverBackgroundColor": "#dc3545",
            "borderWidth": 1,
            "borderDash": [8, 5],
            "data": [5, 8, 3, 9, 2, 8]
        }
    ]
}


def get_incident_color(priority):
    """Return the color based on incident priority."""
    return {
        "High": "danger",
        "Medium": "warning",
        "Low": "success",
        "Planned": "primary"
    }.get(priority, "secondary")  # Default color if priority is unknown


@router.get("/incidents-data", response_model=list[IncidentSummary])
def get_incidents():
    """Fetch incidents and transform the data."""
    incidents = fetch_incidents()

    incidents_summary = []
    for inc in incidents["result"][:4]:
        incidents_summary.append(
            IncidentSummary(
                color=get_incident_color(inc["priority"]),
                title=inc["short_description"],
                status=inc["state"],
                priority=inc["priority"],
                system=inc["category"],
                reportedTime=inc["opened_at"]
            )
        )
    return incidents_summary


@router.get("/incident-metrics", response_model=IncidentMetrics)
def get_incident_metrics():
    """Return incident statistics for dashboard visualization."""
    return IncidentMetrics(
        timestamps=["Jan", "Feb", "Mar", "Apr", "May"],
        incidentCount=[10, 20, 15, 30, 25],
        severityLevels=["Low", "Medium", "High", "Critical"],
        severityCounts=[5, 12, 8, 4],
        resolutionTimes=[5, 8, 6, 12, 10, 4, 7],
        types=["Network", "Hardware", "Software", "Security"],
        typeCounts=[15, 10, 25, 5]
    )


@router.get("/incidents", response_model=list[IncidentTableEntry])
def get_table_data():
    """Fetch table data for UI rendering."""
    service_now_data = fetch_incidents()

    # Convert ServiceNow response to IncidentTableEntry format
    incidents = []
    for incident in service_now_data["result"]:
        incidents.append(
            IncidentTableEntry(
                avatar={"src": "avatar1.png", "status": "success"},
                incident={
                    "name": incident["number"],
                    "new": True,
                    "registered": incident["sys_updated_on"]
                },
                component="Inbound Kafka",
                progress={
                    "value": 0,
                    "period": incident["sys_updated_on"],
                    "color": "success"
                },
                priority="L2",
                activity="10 sec ago"
            )
        )

    return incidents


@router.get("/incidents/{incident_id}", response_model=IncidentTableEntry)
def get_incident_detail(incident_id: str):
    """Fetch incident details by ID."""

    logging.info(f"Fetching incident details for ID: {incident_id}")

    service_now_data = fetch_incidents()

    # Find the matching incident
    incident = next(
        (inc for inc in service_now_data["result"] if inc["number"] == incident_id),
        None
    )

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return IncidentTableEntry(
        avatar={"src": "avatar1.png", "status": "success"},
        incident={
            "name": incident["number"],
            "new": True,
            "registered": incident["sys_updated_on"]
        },
        component="Inbound Kafka",
        progress={
            "value": 0,
            "period": incident["sys_updated_on"],
            "color": "success"
        },
        priority="L2",
        activity="10 sec ago"
    )


@router.get("/incidents-status")
def get_all_status_metrics():
    """Fetch telemetry data for all data centers."""
    return incident_status
