from datetime import datetime
from uuid import uuid4
from .env_profiler import get_environment

def create_run(experiment_name, parameters=None, metrics=None, dataset=None,
               code=None, artifacts=None, tags=None):
    run_id = f"run_{uuid4().hex[:8]}"
    run_data = {
        "id": run_id,
        "experiment_name": experiment_name,
        "timestamp_start": datetime.now(),
        "timestamp_end": None,
        "parameters": parameters or {},
        "metrics": metrics or {},
        "dataset": dataset,
        "code": code,
        "environment": get_environment(),
        "artifacts": artifacts or {},
        "tags": tags or []
    }
    return run_data
