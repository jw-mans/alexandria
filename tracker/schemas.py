from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class ParameterSchema(BaseModel):
    key: str
    value: str

class MetricSchema(BaseModel):
    key: str
    value: float
    step: Optional[int] = None

class DatasetSchema(BaseModel):
    name: str
    path: str
    num_rows: int
    num_columns: int
    schema: Dict
    hash: str

class CodeSchema(BaseModel):
    git_commit: str
    entrypoint: str
    tracked_files: List[Dict]

class EnvironmentSchema(BaseModel):
    python_version: str
    pip_freeze: List[str]
    os: str

class ArtifactSchema(BaseModel):
    name: str
    type: str
    path: str

class RunSchema(BaseModel):
    id: str
    experiment_name: str
    timestamp_start: Optional[datetime] = None
    timestamp_end: Optional[datetime] = None
    tags: Optional[List[str]] = []
    parameters: Optional[List[ParameterSchema]] = []
    metrics: Optional[List[MetricSchema]] = []
    dataset: Optional[DatasetSchema] = None
    code: Optional[CodeSchema] = None
    environment: Optional[EnvironmentSchema] = None
    artifacts: Optional[List[ArtifactSchema]] = [] 
