from fastapi import FastAPI
from app.routes import incidents
from app.routes import metrics
from app.routes import elastic
from app.routes import elasticIncidents
from app.routes import servicenow
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Incident Management API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routes
app.include_router(incidents.router, prefix="/api")
app.include_router(metrics.router, prefix="/api")
app.include_router(elastic.router, prefix="/api")
app.include_router(elasticIncidents.router, prefix="/api")
app.include_router(servicenow.router, prefix="/api")



@app.get("/")
def read_root():
    return {"message": "Welcome to the Incident API"}


