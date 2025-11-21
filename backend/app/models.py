from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class Run(Base):
    __tablename__ = "runs"
    id = Column(String, primary_key=True)
    experiment_name = Column(String)
    timestamp_start = Column(DateTime, default=datetime.datetime.now)
    timestamp_end = Column(DateTime)
    tags = Column(JSON)

    parameters = relationship("Parameter", back_populates="run", cascade="all, delete-orphan")
    metrics = relationship("Metric", back_populates="run", cascade="all, delete-orphan")
    dataset = relationship("Dataset", uselist=False, back_populates="run", cascade="all, delete-orphan")
    code = relationship("Code", uselist=False, back_populates="run", cascade="all, delete-orphan")
    environment = relationship("Environment", uselist=False, back_populates="run", cascade="all, delete-orphan")
    artifacts = relationship("Artifact", back_populates="run", cascade="all, delete-orphan")


class Parameter(Base):
    __tablename__ = "parameters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("runs.id"), index=True)
    key = Column(String)
    value = Column(String)
    run = relationship("Run", back_populates="parameters")


class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("runs.id"), index=True)
    key = Column(String)
    value = Column(Float)
    step = Column(Integer, nullable=True)
    run = relationship("Run", back_populates="metrics")


class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("runs.id"), index=True)
    name = Column(String)
    path = Column(String)
    num_rows = Column(Integer)
    num_columns = Column(Integer)
    table_schema = Column(JSON)
    hash = Column(String)
    run = relationship("Run", back_populates="dataset")


class Code(Base):
    __tablename__ = "code"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("runs.id"), index=True)
    git_commit = Column(String)
    entrypoint = Column(String)
    tracked_files = Column(JSON)
    run = relationship("Run", back_populates="code")


class Environment(Base):
    __tablename__ = "environment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("runs.id"), index=True)
    python_version = Column(String)
    pip_freeze = Column(JSON)
    os = Column(String)
    run = relationship("Run", back_populates="environment")


class Artifact(Base):
    __tablename__ = "artifacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("runs.id"), index=True)
    name = Column(String)
    type = Column(String)
    path = Column(String)
    run = relationship("Run", back_populates="artifacts")
