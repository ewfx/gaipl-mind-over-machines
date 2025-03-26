from fastapi import FastAPI, APIRouter, HTTPException, Query
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import pandas as pd
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import calendar
import random

# Initialize FastAPI app and router
app = FastAPI()
router = APIRouter()

# Connect to Elasticsearch (without certificates)
es = Elasticsearch("http://localhost:9200")  # Use "https://localhost:9200" if security is enabled

# Load pre-trained model for generating embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Index name
index_name = "incidents_final"

# Create Elasticsearch index if it doesn't exist
if not es.indices.exists(index=index_name):
    mapping = {
        "mappings": {
            "properties": {
                "sysId": {"type": "text"},
                "IncidentId": {"type": "text"},
                "title": {"type": "text"},
                "description": {"type": "text"},
                "rootCause": {"type": "text"},
                "createdDate": {"type": "date"},  # ISO 8601 format
                "priority": {"type": "keyword"},
                "status": {"type": "keyword"},  # New field for status
                "closedDate": {"type": "date", "null_value": None},  # New field for resolution date
                "embedding": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                }
            }
        }
    }
    es.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created.")
else:
    print(f"Index '{index_name}' already exists.")


# Helper function to generate embeddings
def generate_embedding(text):
    return model.encode(text).tolist()


# Helper function to convert date to ISO 8601 format
def convert_to_iso_date(date_str):
    formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]  # Accepts both formats
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.isoformat()
        except ValueError:
            continue
    raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Expected format: 'YYYY-MM-DD "
                                                f"HH:MM:SS' or 'YYYY-MM-DDTHH:MM:SS'.")


@router.delete("/delete_index")
async def delete_index():
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        return {"message": f"Index '{index_name}' deleted successfully."}
    else:
        return {"error": f"Index '{index_name}' does not exist."}


def calculate_activity(created_date):
    now = datetime.now(timezone.utc)
    created_dt = datetime.strptime(created_date, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    diff = now - created_dt
    seconds = diff.total_seconds()

    if seconds < 60:
        return f"{int(seconds)} sec ago"
    elif seconds < 3600:
        return f"{int(seconds // 60)} min ago"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hrs ago"
    else:
        return f"{int(seconds // 86400)} days ago"


def get_status_color(status):
    status_colors = {
        "New": "blue",
        "Resolved": "green",
        "Unresolved": "red",
        "Closed": "gray"
    }
    return status_colors.get(status, "yellow")  # Default color if status is unknown


def get_progress_value(status):
    if status == "New":
        return 0
    elif status == "Closed":
        return 100
    elif status == "Resolved":
        return random.randint(70, 90)
    elif status == "Unresolved":
        return random.randint(40, 60)
    else:
        return random.randint(10, 30)  # Default for other statuses


@router.get("/incident_list")
async def get_incidents(limit: int = Query(None, description="Number of records to return")):
    try:
        query = {
            "size": limit if limit else 1000,  # Use limit if provided, else return all
            "query": {"match_all": {}},
            "_source": ["IncidentId", "createdDate", "priority", "status"]
        }
        response = es.search(index=index_name, body=query)

        incidents = []
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            created_date = source["createdDate"]
            status = source["status"]
            activity = calculate_activity(created_date)

            incident_data = {
                "avatar": {"src": "avatar1.png", "status": "success"},
                "incident": {
                    "name": source["IncidentId"],
                    "new": source["status"] == "New",
                    "registered": created_date
                },
                "progress": {
                    "value": get_progress_value(status),
                    "period": created_date,
                    "color": get_status_color(status)
                },
                "priority": source["priority"],
                "activity": activity
            }
            incidents.append(incident_data)

        return incidents

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching incidents: {str(e)}")


@router.get("/incidents_elastic")
def get_incident_by_id(incident_id: str):
    query = {
        "query": {
            "match": {
                "IncidentId": incident_id  # Match a specific IncidentId
            }
        },
        "_source": ["IncidentId", "createdDate", "priority", "status", "title", "description", "rootCause", "closedDate"]  # Retrieve all details needed
    }

    try:
        # Execute the query and retrieve the result
        response = es.search(index=index_name, body=query)

        # Check if any hits were returned
        if response["hits"]["total"]["value"] > 0:
            # Return the first matching document
            return response["hits"]["hits"][0]["_source"]
        else:
            print(f"No incident found with IncidentId: {incident_id}")
            return None

    except Exception as e:
        print(f"Error fetching incident from Elasticsearch: {e}")
        return None


def get_incident_color(priority):
    """Return the color based on incident priority."""
    return {
        "High": "danger",
        "Medium": "warning",
        "Low": "success",
        "Planned": "primary"
    }.get(priority, "secondary")  # Default if unknown


category_mapping = {
    "Network": ["router", "latency", "network", "connection"],
    "Hardware": ["server", "malfunction", "hard disk", "power failure"],
    "Software": ["software", "crash", "update", "bug"],
    "Security": ["unauthorized", "hacked", "phishing", "breach"]
}


@router.get("/incidents-overview")
async def get_incidents_overview(limit: int = None):
    """Fetch incident summary and metrics for the dashboard."""
    try:
        query = {
            "size": limit if limit else 1000,  # Fetch limited records if requested, otherwise all
            "query": {"match_all": {}},
            "_source": ["title", "status", "priority", "createdDate", "closedDate", "description"]
        }
        response = es.search(index=index_name, body=query)

        # Severity and type counts
        severity_counts = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        type_counts = {"Network": 0, "Hardware": 0, "Software": 0, "Security": 0}

        # Get last 6 months in 'MMM' format
        current_date = datetime.utcnow()
        last_six_months = [(current_date - timedelta(days=30 * i)).strftime("%b") for i in range(5, -1, -1)]

        # Initialize incident count & resolution times
        incident_count = {month: 0 for month in last_six_months}
        resolution_times = {month: [] for month in last_six_months}

        all_incidents = []  # Store all incidents to sort later

        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            priority = source["priority"]
            status = source["status"]
            created_date = source.get("createdDate")
            closed_date = source.get("closedDate")

            print(f"source === {source}")

            # Ensure valid createdDate
            if not created_date:
                continue

            # Store incident data for sorting
            all_incidents.append({
                "color": get_incident_color(priority),
                "title": source["title"],
                "status": status,
                "priority": priority,
                "system": "Random",
                "reportedTime": created_date,  # Keep full datetime string
                "createdDate": created_date  # Keep full datetime for sorting
            })

            # Convert string date to datetime object
            created_dt = datetime.strptime(created_date, "%Y-%m-%dT%H:%M:%S")
            month = created_dt.strftime("%b")  # Extract month as 'Jan', 'Feb', etc.

            # Count severity levels
            if priority in severity_counts:
                severity_counts[priority] += 1

            # Track incidents over time
            if month in incident_count:
                incident_count[month] += 1

            description = source["description"].lower()
            assigned_category = None

            # Check for keyword matches
            for category, keywords in category_mapping.items():
                if any(keyword in description for keyword in keywords):
                    assigned_category = category
                    break  # Stop checking once a category is assigned

            # Ensure each incident gets exactly one category
            if assigned_category is None:
                assigned_category = random.choice(list(type_counts.keys()))  # Assign randomly if no match

            type_counts[assigned_category] += 1

            # Store resolution time for resolved incidents
            if closed_date:
                closed_dt = datetime.strptime(closed_date, "%Y-%m-%dT%H:%M:%S")
                resolution_time = (closed_dt - created_dt).days  # Resolution time in days
                if month in resolution_times:
                    resolution_times[month].append(max(resolution_time, 1))  # Avoid 0-day resolutions

        # Sort all incidents by `createdDate` (latest first) and pick the latest 4
        incidents_summary = sorted(all_incidents, key=lambda x: x["createdDate"], reverse=True)[:4]

        # Ensure each month has a value (use average if exists, otherwise 0)
        avg_resolution_times = [
            int(sum(times) / len(times)) if times else 0
            for times in resolution_times.values()
        ]

        return {
            "summary": incidents_summary,  # Only the latest 4 incidents
            "metrics": {
                "timestamps": list(incident_count.keys()),
                "incidentCount": list(incident_count.values()),
                "severityLevels": list(severity_counts.keys()),
                "severityCounts": list(severity_counts.values()),
                "resolutionTimes": avg_resolution_times,  # Ensuring last 6 months are included
                "types": list(type_counts.keys()),
                "typeCounts": list(type_counts.values())
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching incidents overview: {str(e)}")


# Endpoint to index incidents from a CSV file
@router.post("/index_incidents")
async def index_incidents(file_path: str):
    """
    Accepts a file path as input, reads the CSV file, and indexes the records into Elasticsearch.
    """
    try:
        # Read the CSV file from the provided file path
        df = pd.read_csv(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    # Ensure required columns are present
    required_columns = ["sysId", "IncidentId", "title", "description", "rootCause", "createdDate", "priority", "status",
                        "closedDate"]
    if not all(col in df.columns for col in required_columns):
        raise HTTPException(status_code=400, detail=f"CSV file must contain the following columns: {required_columns}")

    # Index each incident into Elasticsearch
    for _, row in df.iterrows():
        # Convert dates to ISO 8601 format
        created_date_iso = convert_to_iso_date(row['createdDate'])
        closed_date_iso = convert_to_iso_date(row['closedDate']) if pd.notna(row['closedDate']) else None

        text_to_embed = (f"Title: {row['title']}. Description: {row['description']}. Root Cause: {row['rootCause']}. "
                         f"Priority: {row['priority']}. Status: {row['status']}.")

        embedding = generate_embedding(text_to_embed)

        doc = {
            "sysId": row['sysId'],
            "IncidentId": row['IncidentId'],
            "title": row['title'],
            "description": row['description'],
            "rootCause": row['rootCause'],
            "createdDate": created_date_iso,
            "priority": row['priority'],
            "status": row['status'],
            "closedDate": closed_date_iso,  # Only included if status is 'Resolved' or 'Closed'
            "embedding": embedding
        }
        es.index(index=index_name, id=row['sysId'], body=doc)

    return {"message": "Incidents indexed successfully"}


# Endpoint to get the latest 10 incidents
@router.get("/latest_incidents")
async def latest_incidents():
    response = es.search(
        index=index_name,
        size=10,
        body={
            "query": {
                "match_all": {}
            },
            "sort": [
                {"createdDate": {"order": "desc"}}  # Sort by createdDate in descending order
            ],
            "_source": {
                "excludes": ["embedding"]  # Exclude the 'embedding' field from the response
            }
        }
    )
    results = [
        {"id": hit['_id'], "data": hit['_source']}
        for hit in response["hits"]["hits"]
    ]
    return results


@router.get("/latest_seven_days_incidents")
async def latest_seven_days_incidents():
    """
    Fetches incident counts for the last 7 days, calculates the percentage of incidents
    compared to total incidents, computes the average resolution time,
    calculates the incident resolution rate, and provides a status-wise breakdown.
    """
    try:
        # Query to count total incidents
        total_count_query = {"track_total_hits": True, "query": {"match_all": {}}}
        total_response = es.search(index=index_name, body=total_count_query)
        total_incidents = total_response["hits"]["total"]["value"]

        # Query to fetch last 7 days' incidents
        last_seven_days_query = {
            "size": 10000,
            "query": {
                "range": {
                    "createdDate": {
                        "gte": "now-7d/d",
                        "lte": "now/d"
                    }
                }
            },
            "_source": ["createdDate", "status"],
            "sort": [{"createdDate": {"order": "desc"}}]
        }

        # Query to fetch all resolved/closed incidents
        resolution_time_query = {
            "size": 10000,
            "query": {
                "bool": {
                    "must": [{"exists": {"field": "closedDate"}}]
                }
            },
            "_source": ["createdDate", "closedDate"]
        }

        # Queries to count incidents by status
        status_queries = {
            "New": {"track_total_hits": True, "query": {"term": {"status": "New"}}},
            "Resolved": {"track_total_hits": True, "query": {"term": {"status": "Resolved"}}},
            "Closed": {"track_total_hits": True, "query": {"term": {"status": "Closed"}}},
            "Unresolved": {
                "track_total_hits": True,
                "query": {
                    "bool": {
                        "must_not": [{"exists": {"field": "closedDate"}}]
                    }
                }
            }
        }

        # Execute searches
        last_seven_days_response = es.search(index=index_name, body=last_seven_days_query)
        resolution_time_response = es.search(index=index_name, body=resolution_time_query)

        # Fetch status counts
        status_counts = {}
        for status, query in status_queries.items():
            response = es.search(index=index_name, body=query)
            status_counts[status] = response["hits"]["total"]["value"]

        # Generate last 7 days' weekday labels
        today = datetime.today()
        last_week_dates = [(today - timedelta(days=i)).strftime('%A') for i in range(6, -1, -1)]

        # Initialize data structures
        week_data = {day: 0 for day in last_week_dates}
        resolution_times = []  # Stores resolution durations

        # Process last 7 days' response
        for hit in last_seven_days_response["hits"]["hits"]:
            source = hit["_source"]
            created_date_str = source.get("createdDate")

            if created_date_str:
                try:
                    created_date = datetime.strptime(created_date_str, "%Y-%m-%dT%H:%M:%S")
                    weekday = created_date.strftime('%A')
                    if weekday in week_data:
                        week_data[weekday] += 1
                except ValueError:
                    continue  # Skip malformed dates

        # Total last week incidents
        last_week_incidents = sum(week_data.values())

        # Process resolution time response
        for hit in resolution_time_response["hits"]["hits"]:
            source = hit["_source"]
            created_date_str = source.get("createdDate")
            closed_date_str = source.get("closedDate")

            if created_date_str and closed_date_str:
                try:
                    created_date = datetime.strptime(created_date_str, "%Y-%m-%dT%H:%M:%S")
                    closed_date = datetime.strptime(closed_date_str, "%Y-%m-%dT%H:%M:%S")
                    resolution_time = (closed_date - created_date).total_seconds() / 3600  # Convert to hours
                    resolution_times.append(resolution_time)
                except ValueError:
                    continue  # Skip malformed dates

        # Calculate percentage of last week incidents
        percentage_last_week = (last_week_incidents / total_incidents * 100) if total_incidents > 0 else 0

        # Calculate average resolution time (in hours)
        avg_resolution_time = round(sum(resolution_times) / len(resolution_times), 2) if resolution_times else 0

        # Calculate Incident Resolution Rate
        resolution_rate = (status_counts["Resolved"] + status_counts[
            "Closed"]) / total_incidents * 100 if total_incidents > 0 else 0

        # Format the response
        result_json = {
            "labels": last_week_dates,
            "datasets": [
                {
                    "backgroundColor": "transparent",
                    "borderColor": "#321fdb",
                    "borderWidth": 2,
                    "data": [week_data[day] for day in last_week_dates]
                }
            ],
            "percentage": round(percentage_last_week, 2),  # Rounded percentage
            "averageResolutionTime": avg_resolution_time,  # Average resolution time in hours (for all data)
            "incidentResolutionRate": round(resolution_rate, 2),  # Resolution Rate in percentage
            "incidentStatusCounts": {  # New status-wise breakdown
                "New": status_counts["New"],
                "Resolved": status_counts["Resolved"],
                "Unresolved": status_counts["Unresolved"],
                "Closed": status_counts["Closed"]
            }
        }

        return result_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching incidents: {str(e)}")


@router.get("/latest_six_months_incidents")
async def latest_six_months_incidents():
    try:
        # Define status colors (matching the UI styles)
        status_colors = {
            "New": "info",
            "In Progress": "primary",
            "On Hold": "warning",
            "Resolved": "success",
            "Closed": "secondary",
            "Cancelled": "danger"
        }

        # Get the first day of the current month and subtract 5 months to get the start of the range
        start_date = (datetime.today().replace(day=1) - timedelta(days=150)).strftime("%Y-%m-%d")

        last_six_months_query = {
            "size": 0,
            "query": {
                "range": {
                    "createdDate": {
                        "gte": start_date,  # ✅ Ensures we fetch data from the last 6 months
                        "lte": "now/M"
                    }
                }
            },
            "aggs": {
                "monthly_statuses": {
                    "date_histogram": {
                        "field": "createdDate",
                        "calendar_interval": "month",
                        "format": "yyyy-MM"
                    },
                    "aggs": {
                        status: {"filter": {"term": {"status": status}}} for status in status_colors.keys()
                    }
                }
            }
        }

        last_six_months_response = es.search(index=index_name, body=last_six_months_query)

        # Process last 6 months' response
        monthly_labels = []
        monthly_datasets = {status: [] for status in status_colors.keys()}
        total_incidents_count = 0
        status_counts = {status: 0 for status in status_colors.keys()}  # To track status-wise counts

        for bucket in last_six_months_response["aggregations"]["monthly_statuses"]["buckets"]:
            # Convert "YYYY-MM" to full month name (e.g., "March")
            month_dt = datetime.strptime(bucket["key_as_string"], "%Y-%m")
            month_name = calendar.month_name[month_dt.month]  # ✅ Converts "YYYY-MM" to "March", etc.
            monthly_labels.append(month_name)

            # Collect data for each status
            for status in status_colors.keys():
                count = bucket[status]["doc_count"]
                monthly_datasets[status].append(count)
                status_counts[status] += count  # Accumulate counts for overall percentage calculation

            total_incidents_count += sum(bucket[status]["doc_count"] for status in status_colors.keys())

        # Ensure labels are exactly the last six months, even if some months have no data
        today = datetime.today()
        expected_labels = [
            calendar.month_name[(today.month - i) % 12 or 12] for i in range(5, -1, -1)
        ]

        # Fill missing months with zero counts
        final_datasets = []
        for status in status_colors.keys():
            filled_data = [monthly_datasets[status][monthly_labels.index(month)]
                           if month in monthly_labels else 0
                           for month in expected_labels]

            final_datasets.append({
                "label": status,
                "backgroundColor": "transparent",
                "borderColor": f"getStyle('--cui-{status_colors[status]}')",
                "pointHoverBackgroundColor": f"getStyle('--cui-{status_colors[status]}')",
                "borderWidth": 2,
                "data": filled_data
            })

        # Generate `progressExample` dynamically based on percentages
        progress_data = []
        for status, count in status_counts.items():
            percent = round((count / total_incidents_count * 100), 2) if total_incidents_count > 0 else 0
            progress_data.append({
                "title": status,
                "value": "Incidents",
                "percent": percent,
                "color": status_colors[status]
            })

        # Format the response
        result_json = {
            "labels": expected_labels,  # ✅ Now correctly filled with last 6 months
            "datasets": final_datasets,
            "progress": progress_data  # ✅ Added progressExample dynamically
        }

        return result_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching incidents: {str(e)}")


# Pydantic model for request validation
class ExceptionModel(BaseModel):
    sysId: str
    IncidentId: str
    title: str
    description: str
    rootCause: str
    createdDate: str  # ISO 8601 format (e.g., "2023-10-01T12:34:56")
    priority: str


# Endpoint to add a single exception
@router.post("/add_exception")
async def add_exception(exception: ExceptionModel):
    """
    Accepts a single exception as JSON input, generates an embedding for the description,
    and indexes the record into Elasticsearch.
    """
    try:
        # Convert createdDate to ISO 8601 format
        iso_date = convert_to_iso_date(exception.createdDate)

        # Generate embedding for the description
        embedding = generate_embedding(exception.description)

        # Prepare the document to be indexed
        doc = {
            "sysId": exception.sysId,
            "IncidentId": exception.IncidentId,
            "title": exception.title,
            "description": exception.description,
            "rootCause": exception.rootCause,
            "createdDate": iso_date,  # Use the converted ISO 8601 date
            "priority": exception.priority,
            "embedding": embedding
        }

        # Index the document into Elasticsearch
        es.index(index=index_name, id=exception.sysId, body=doc)

        return {"message": "Exception added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding exception: {str(e)}")


# Endpoint to perform similarity search
@router.post("/similarity_search")
async def similarity_search(query_text: str, size: int = 10):
    if not query_text:
        raise HTTPException(status_code=400, detail="Missing query_text")

    query_embedding = generate_embedding(query_text)
    response = es.search(
        index=index_name,
        size=size,
        body={
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {
                            "query_vector": query_embedding
                        }
                    }
                }
            }
        }
    )
    results = [
        {"id": hit['_id'], "score": hit['_score'], "data": hit['_source']}
        for hit in response["hits"]["hits"]
    ]
    return results
