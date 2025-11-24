import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any

from . import models, schemas

class __Diffs:

    @staticmethod
    def _diff_params(params1: dict, params2: dict):
        changed_params = {
            k: {'old': params1.get(k), 'new': params2.get(k)}
            for k in set(params1) | set(params2)
            if params1.get(k) != params2.get(k)
        }
        return changed_params

    @staticmethod
    def _diff_metrics(metrics1: dict, metrics2: dict):
        changed_metrics = {}
        for k in set(metrics1) | set(metrics2):
            v1, v2 = metrics1.get(k), metrics2.get(k)
            if v1 != v2:
                changed_metrics[k] = {'old': v1, 'new': v2}
        return changed_metrics

    @staticmethod
    def _diff_datasets(ds1: dict, ds2: dict):
        ds_changed = ds1 != ds2
        return {'changed': ds_changed, 'detail': {'left': ds1, 'right': ds2} if ds_changed else {}}

    @staticmethod
    def _diff_code(code1: dict, code2: dict):
        commit_changes = {}
        code_changes = {}

        if code1.get('git_commit') != code2.get('git_commit'):
            commit_changes['git_commit'] = {'old': code1.get('git_commit'), 'new': code2.get('git_commit')}

        tf1 = {f['path']: f['hash'] for f in code1.get('tracked_files', [])}
        tf2 = {f['path']: f['hash'] for f in code2.get('tracked_files', [])}

        added = set(tf2) - set(tf1)
        removed = set(tf1) - set(tf2)
        modified = [p for p in set(tf1) & set(tf2) if tf1[p] != tf2[p]]

        code_changes['added_files'] = list(added)
        code_changes['removed_files'] = list(removed)
        code_changes['modified_files'] = modified

        return commit_changes, code_changes

    @staticmethod
    def _diff_artifacts(arts1: dict, arts2: dict):
        artifacts_diff = {}
        for k in set(arts1) | set(arts2):
            if arts1.get(k) != arts2.get(k):
                artifacts_diff[k] = {'old': arts1.get(k), 'new': arts2.get(k)}
        return artifacts_diff

    @staticmethod
    def _diff_env(env1: dict, env2: dict):
        return {k: {'old': env1.get(k), 'new': env2.get(k)} for k in set(env1) | set(env2) if env1.get(k) != env2.get(k)}


def diff_runs(db: Session, run1: models.Run, run2: models.Run):
    r1 = serialize_run(run1)
    r2 = serialize_run(run2)

    diff = {
        "parameters_changed": __Diffs._diff_params(r1['parameters'], r2['parameters']),
        "metrics_changed": __Diffs._diff_metrics(r1['metrics'], r2['metrics']),
        "dataset_changed": __Diffs._diff_datasets(r1.get('dataset') or {}, r2.get('dataset') or {}),
        "git_commit": __Diffs._diff_code(r1.get('code') or {}, r2.get('code') or {})[0],
        "code_changed": __Diffs._diff_code(r1.get('code') or {}, r2.get('code') or {})[1],
        "artifacts_changed": __Diffs._diff_artifacts(r1.get('artifacts') or {}, r2.get('artifacts') or {}),
        "environment": __Diffs._diff_env(r1.get('environment') or {}, r2.get('environment') or {}),
    }
    return diff


def serialize_run(db_run):
    """
    Преобразуем SQLAlchemy объект Run и все вложенные объекты
    в обычные словари для Pydantic
    """
    return {
        "id": db_run.id,
        "experiment_name": db_run.experiment_name,
        "timestamp_start": db_run.timestamp_start.isoformat() if db_run.timestamp_start else None,
        "timestamp_end": db_run.timestamp_end.isoformat() if db_run.timestamp_end else None,
        "tags": db_run.tags or [],
        "parameters": dict(db_run.parameters) if db_run.parameters else {},
        "metrics": {
            key: [
                m.value for m in db_run.metrics if m.key == key
            ] for key in set(m.key for m in db_run.metrics)
        } if db_run.metrics else {},
        "dataset": {
            "name": db_run.dataset.name,
            "path": db_run.dataset.path,
            "num_rows": db_run.dataset.num_rows,
            "num_columns": db_run.dataset.num_columns,
            "table_schema": db_run.dataset.table_schema,
            "hash": db_run.dataset.hash,
        } if db_run.dataset else {},
        "code": {
            "git_commit": db_run.code.git_commit,
            "entrypoint": db_run.code.entrypoint,
            "tracked_files": db_run.code.tracked_files,
        } if db_run.code else {},
        "environment": {
            "python_version": db_run.environment.python_version,
            "pip_freeze": db_run.environment.pip_freeze,
            "os": db_run.environment.os,
        } if db_run.environment else {},
        "artifacts": {
            a.name: {
                "name": a.name,
                "type": a.type,
                "path": a.path,
                "hash": getattr(a, "hash", None)
            }
            for a in (db_run.artifacts or [])
        },
    }


def _serialize_metrics(metrics):
    out = {}
    for m in metrics:
        out.setdefault(m.key, []).append(m.value)
    return out


def create_run(db: Session, run_data: Dict[str, Any]):
    params = [models.Parameter(key=k, value=str(v)) for k, v in run_data.get('parameters', {}).items()]

    metrics = []
    for key, values in run_data.get('metrics', {}).items():
        for step, value in enumerate(values):
            metrics.append(models.Metric(key=key, value=value, step=step))

    dataset = models.Dataset(**run_data['dataset']) if run_data.get('dataset') else None
    code = models.Code(**run_data['code']) if run_data.get('code') else None
    environment = models.Environment(**run_data['environment']) if run_data.get('environment') else None
    artifacts = [models.Artifact(name=name, **info) for name, info in run_data.get('artifacts', {}).items()]

    try:
        db_run = models.Run(
            id=run_data['id'],
            experiment_name=run_data["experiment_name"],
            tags=run_data.get("tags", []),
            parameters=params,
            metrics=metrics,
            dataset=dataset,
            code=code,
            environment=environment,
            artifacts=artifacts,
        )
        db.add(db_run)
        db.commit()
        db.refresh(db_run)
        return db_run
    except SQLAlchemyError as ex:
        db.rollback()
        raise


def get_run(db: Session, run_id: str):
    db_run = db.query(models.Run).filter(models.Run.id == run_id).first()
    return db_run


def list_runs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Run).offset(skip).limit(limit).all()
