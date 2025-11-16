from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class Run(Base):
    __tablename__ = "runs"
    id = Column(String, primary_key=True)
    experiment_name = Column(String)
    timestamp_start = Column(DateTime, default=datetime.datetime.utcnow)
    timestamp_end = Column(DateTime)
    tags = Column(JSON)

    parameters = relationship("Parameter", back_populates="run")
    metrics = relationship("Metric", back_populates="run")
    dataset = relationship("Dataset", uselist=False, back_populates="run")
    code = relationship("Code", uselist=False, back_populates="run")
    environment = relationship("Environment", uselist=False, back_populates="run")
    artifacts = relationship("Artifact", back_populates="run")


class Parameter(Base):
    __tablename__ = "parameters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("runs.id"))
    key = Column(String)
    value = Column(String)
    run = relationship("Run", back_populates="parameters")


class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("runs.id"))
    key = Column(String)
    value = Column(Float)
    step = Column(Integer, nullable=True)
    run = relationship("Run", back_populates="metrics")


class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("runs.id"))
    name = Column(String)
    path = Column(String)
    num_rows = Column(Integer)
    num_columns = Column(Integer)
    schema = Column(JSON)
    hash = Column(String)
    run = relationship("Run", back_populates="dataset")


class Code(Base):
    __tablename__ = "code"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("runs.id"))
    git_commit = Column(String)
    entrypoint = Column(String)
    tracked_files = Column(JSON)
    run = relationship("Run", back_populates="code")


class Environment(Base):
    __tablename__ = "environment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("runs.id"))
    python_version = Column(String)
    pip_freeze = Column(JSON)
    os = Column(String)
    run = relationship("Run", back_populates="environment")


class Artifact(Base):
    __tablename__ = "artifacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("runs.id"))
    name = Column(String)
    type = Column(String)
    path = Column(String)
    run = relationship("Run", back_populates="artifacts")
