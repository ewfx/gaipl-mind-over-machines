import io

from fastapi import HTTPException, APIRouter, Response
import csv
import requests
from typing import Dict, Any
from requests.auth import HTTPBasicAuth

# Initialize FastAPI app
router = APIRouter()

# ServiceNow Configuration - Replace with your details
INSTANCE = "dev267328"  # Your ServiceNow instance name
USERNAME = "mindovermachines.ai@gmail.com"  # Your ServiceNow username
PASSWORD = "Mom@5Mom@5"  # Your ServiceNow password
username = "admin"
password = "PjWf%@7hYoX9"
API_URL = f"https://{INSTANCE}.service-now.com/api/now/table/incident"
URL = f"https://{INSTANCE}.service-now.com/api/now/table/kb_knowledge"


# Function to fetch incidents from ServiceNow
def fetch_incidents() -> Dict[str, Any]:
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(API_URL, headers=headers, auth=HTTPBasicAuth(username, password))
        response.raise_for_status()  # Raise error for 4xx/5xx responses
        return response.json()  # Return JSON response

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"ServiceNow API error: {str(e)}")


# Mapping function
def map_incident_fields(incident_json):
    # Priority mapping based on severity
    priority_map = {
        "1": "Critical",
        "2": "High",
        "3": "Medium",
        "4": "Low"
    }

    # Status mapping based on incident_state
    status_map = {
        "1": "New",
        "2": "Active",
        "3": "Awaiting Problem",
        "4": "Awaiting User Info",
        "5": "Awaiting Evidence",
        "6": "Resolved",
        "7": "Closed"
    }

    # Extract and map fields
    return {
        "sysId": incident_json.get("sys_id", ""),
        "IncidentId": incident_json.get("number", ""),
        "title": incident_json.get("short_description", ""),
        "description": incident_json.get("description", ""),
        "rootCause": incident_json.get("cause", ""),
        "createdDate": incident_json.get("opened_at", ""),
        "priority": priority_map.get(incident_json.get("severity", ""), "Unknown"),
        "status": status_map.get(incident_json.get("incident_state", ""), "Unknown"),
        "closedDate": incident_json.get("closed_at", "")
    }


# FastAPI route to get incidents
@router.get("/servicenow_incidents")
def get_incidents():
    try:
        # Fetch incidents from the mock function
        incidents_data = fetch_incidents()

        # Map each incident to the desired format
        mapped_incidents = [map_incident_fields(incident) for incident in incidents_data.get("result", [])]

        if not mapped_incidents:
            raise ValueError("No incidents found in the response.")

        # Use StringIO as a file-like object for CSV generation
        output = io.StringIO()
        writer = csv.DictWriter(output,
                                fieldnames=["sysId", "IncidentId", "title", "description", "rootCause", "createdDate",
                                            "priority", "status", "closedDate"])
        writer.writeheader()
        writer.writerows(mapped_incidents)

        # Get the CSV content as a string
        csv_content = output.getvalue()
        output.close()  # Close the StringIO object

        # Return the CSV file as a downloadable response
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=incidents.csv"}
        )

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error generating CSV: {str(e)}")

        # Raise an HTTP exception with a user-friendly message
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the request: {str(e)}")
