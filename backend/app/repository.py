from sqlalchemy.orm import Session
from app import models, schemas
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
    db.commit()
    db.refresh(db_run)
    return run

def get_run(db: Session, run_id: str):
    return db.query(models.Run).filter(models.Run.id == run_id).first()

def list_runs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Run).offset(skip).limit(limit).all()

def diff_runs(run1: models.Run, run2: models.Run):
    diff = {}

    # Параметры
    params1 = {p.key: p.value for p in run1.parameters}
    params2 = {p.key: p.value for p in run2.parameters}
    changed_params = {k: {"old": params1.get(k), "new": params2.get(k)}
                      for k in set(params1) | set(params2)
                      if params1.get(k) != params2.get(k)}
    diff["parameters_changed"] = changed_params

    # Метрики
    metrics1 = {m.key: m.value for m in run1.metrics}
    metrics2 = {m.key: m.value for m in run2.metrics}
    metrics_diff = {k: {"old": metrics1.get(k), "new": metrics2.get(k)}
                    for k in set(metrics1) | set(metrics2)
                    if metrics1.get(k) != metrics2.get(k)}
    diff["metrics_changed"] = metrics_diff

    # Датасет
    diff["dataset_changed"] = run1.dataset.hash != run2.dataset.hash if run1.dataset and run2.dataset else False

    # Код
    code_diff = []
    if run1.code and run2.code:
        files1 = {f['path'] for f in run1.code.tracked_files}
        files2 = {f['path'] for f in run2.code.tracked_files}
        code_diff = list(files1.symmetric_difference(files2))
    diff["code_changed"] = code_diff

    return diff
