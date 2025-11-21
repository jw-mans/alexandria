from sqlalchemy.orm import Session
from . import models, schemas
import json

def create_run(db: Session, run: schemas.RunSchema):
    db_run = models.Run(
        id=run.id,
        experiment_name=run.experiment_name,
        timestamp_start=run.timestamp_start,
        timestamp_end=run.timestamp_end,
        tags=run.tags,
    )

    db.add(db_run)
    db.flush()

    # ----- PARAMETERS -----
    for p in run.parameters:
        db.add(models.Parameter(
            run_id=db_run.id,
            key=p.key,
            value=p.value
        ))

    # ----- METRICS -----
    for m in run.metrics:
        db.add(models.Metric(
            run_id=db_run.id,
            key=m.key,
            value=m.value,
            step=m.step
        ))

    # ----- ARTIFACTS -----
    for a in run.artifacts:
        db.add(models.Artifact(
            run_id=db_run.id,
            name=a.name,
            type=a.type,
            path=a.path
        ))

    # ----- DATASET -----
    if run.dataset:
        db.add(models.Dataset(
            run_id=db_run.id,
            name=run.dataset.name,
            path=run.dataset.path,
            num_rows=run.dataset.num_rows,
            num_columns=run.dataset.num_columns,
            table_schema=run.dataset.table_schema,
            hash=run.dataset.hash
        ))

    # ----- CODE -----
    if run.code:
        db.add(models.Code(
            run_id=db_run.id,
            git_commit=run.code.git_commit,
            entrypoint=run.code.entrypoint,
            tracked_files=run.code.tracked_files
        ))

    # ----- ENVIRONMENT -----
    if run.environment:
        db.add(models.Environment(
            run_id=db_run.id,
            python_version=run.environment.python_version,
            pip_freeze=run.environment.pip_freeze,
            os=run.environment.os
        ))

    db.commit()
    db.refresh(db_run)
    return db_run

def get_run(db: Session, run_id: str):
    return db.query(models.Run).filter(models.Run.id == run_id).first()

def list_runs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Run).offset(skip).limit(limit).all()

def diff_runs(run1: models.Run, run2: models.Run):
    diff = {}

    params1 = {p.key: p.value for p in run1.parameters}
    params2 = {p.key: p.value for p in run2.parameters}
    changed_params = {k: {"old": params1.get(k), "new": params2.get(k)}
                      for k in set(params1) | set(params2)
                      if params1.get(k) != params2.get(k)}
    diff["parameters_changed"] = changed_params

    metrics1 = {m.key: m.value for m in run1.metrics}
    metrics2 = {m.key: m.value for m in run2.metrics}
    metrics_diff = {k: {"old": metrics1.get(k), "new": metrics2.get(k)}
                    for k in set(metrics1) | set(metrics2)
                    if metrics1.get(k) != metrics2.get(k)}
    diff["metrics_changed"] = metrics_diff

    diff["dataset_changed"] = run1.dataset.hash != run2.dataset.hash if run1.dataset and run2.dataset else False

    code_diff = []
    if run1.code and run2.code:
        files1 = {f['path'] for f in run1.code.tracked_files}
        files2 = {f['path'] for f in run2.code.tracked_files}
        code_diff = list(files1.symmetric_difference(files2))
    diff["code_changed"] = code_diff

    return diff
