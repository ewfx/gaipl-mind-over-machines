from pydantic import BaseModel
from typing import List


class IncidentSummary(BaseModel):
    color: str
    title: str
    status: str
    priority: str
    system: str
    reportedTime: str


class IncidentMetrics(BaseModel):
    timestamps: List[str]
    incidentCount: List[int]
    severityLevels: List[str]
    severityCounts: List[int]
    resolutionTimes: List[int]
    types: List[str]
    typeCounts: List[int]


class IncidentTableEntry(BaseModel):
    avatar: dict
    incident: dict
    component: str
    progress: dict
    priority: str
    activity: str
