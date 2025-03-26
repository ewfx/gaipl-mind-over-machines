from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from elasticsearch import Elasticsearch, NotFoundError

# Initialize FastAPI app
router = APIRouter()


# Connect to Elasticsearch
def get_elasticsearch_client():
    es = Elasticsearch("http://localhost:9200")  # Replace with your Elasticsearch URL
    if not es.ping():
        raise ValueError("Connection to Elasticsearch failed")
    return es


# Define the index name
INDEX_NAME = "user_rule_analytics"


# Pydantic model for record validation
class Record(BaseModel):
    id: str
    message: str
    page: str
    dataId: str


# Create the index if it doesn't exist
@router.on_event("startup")
async def startup_event():
    es = get_elasticsearch_client()
    if not es.indices.exists(index=INDEX_NAME):
        # Define the mapping for the index (optional, based on your requirements)
        mapping = {
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "message": {"type": "text"},
                    "page": {"type": "keyword"},
                    "dataId": {"type": "keyword"}
                }
            }
        }
        es.indices.create(index=INDEX_NAME, body=mapping)
        print(f"Index '{INDEX_NAME}' created.")


# Push a record to Elasticsearch
@router.post("/push-record")
async def push_record(record: Record):
    """
    Push a record to Elasticsearch.
    Example request body:
    {
        "id": "1",
        "message": "Welcome to the Incidents Page!",
        "page": "incidents",
        "dataId": "1234"
    }
    """
    es = get_elasticsearch_client()
    try:
        # Convert the Pydantic model to a dictionary
        record_dict = record.dict()

        # Index the record in Elasticsearch
        es.index(index=INDEX_NAME, id=record.id, document=record_dict)
        return {"message": f"Record with ID {record.id} pushed successfully."}
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error pushing record: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error pushing record: {str(e)}")


# Retrieve a record from Elasticsearch by ID
@router.get("/get-record/{record_id}")
async def get_record(record_id: str):
    """
    Retrieve a record from Elasticsearch by ID.
    """
    es = get_elasticsearch_client()
    try:
        # Retrieve the record from Elasticsearch
        response = es.get(index=INDEX_NAME, id=record_id)
        return {"id": record_id, "message": response["_source"]["message"], "page": response["_source"]["page"],
                "dataId": response["_source"]["dataId"]}
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f"Record with ID {record_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving record: {str(e)}")


# Retrieve all records from Elasticsearch
@router.get("/get-all-records")
async def get_all_records():
    """
    Retrieve all records from Elasticsearch.
    """
    es = get_elasticsearch_client()
    try:
        # Search for all records in the index
        response = es.search(index=INDEX_NAME, body={"query": {"match_all": {}}})
        records = [
            {"id": hit["_id"], "message": hit["_source"]["data"]}
            for hit in response["hits"]["hits"]
        ]
        return {"records": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving records: {str(e)}")
