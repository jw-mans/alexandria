from pydantic import BaseModel, Field
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
    table_schema: Dict
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
    id: str = Field(..., min_length=1, max_length=64, pattern=r'^[a-zA-Z0-9_-]+$')
    experiment_name: str = Field(..., min_length=1, max_length=255)
    timestamp_start: Optional[datetime] = None
    timestamp_end: Optional[datetime] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    parameters: Optional[List[ParameterSchema]] = Field(default_factory=list)
    metrics: Optional[List[MetricSchema]] = Field(default_factory=list)
    dataset: Optional[DatasetSchema] = None
    code: Optional[CodeSchema] = None
    environment: Optional[EnvironmentSchema] = None
    artifacts: Optional[List[ArtifactSchema]] = Field(default_factory=list)

    class Config:
        from_attributes = True