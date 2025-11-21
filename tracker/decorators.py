from functools import wraps
from .logger import create_run
from .client import send_run
from .code_profiler import get_git_commit, get_tracked_files, get_all_python_files
from .model_saver import save_artifact
import os
import pandas as pd

try:
    from datasets import Dataset as HFDataset
except ImportError:
    HFDataset = None

def track(experiment_name, artifacts_dir="runs/run_auto"):
    """
    Autologging decorator run.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            run_data = create_run(experiment_name)
            kwargs["run_data"] = run_data

            result = func(*args, **kwargs) # train func run

            # dataset autodetection
            for v in kwargs.values():
                if isinstance(v, pd.DataFrame) or (HFDataset and isinstance(v, HFDataset)):
                    from .data_profiler import profile_dataset_auto
                    run_data["dataset"] = profile_dataset_auto(v)
                    break  # select first-founded dataset

            # code and git building
            python_files = get_all_python_files(".")
            run_data["code"] = {
                "git_commit": get_git_commit(),
                "entrypoint": func.__code__.co_filename,
                "tracked_files": get_tracked_files(python_files)
            }

            # artifact building
            if os.path.exists(artifacts_dir):
                run_data["artifacts"] = [
                    {"name": f, "type": "model", "path": os.path.join(artifacts_dir, f)}
                    for f in os.listdir(artifacts_dir)
                ]

            # backend sending
            send_run(run_data)
            print(f"Run {run_data['id']} sent to backend")
            return result
        return wrapper
    return decorator

def log_metric(run_data, key: str, value: float, step: int = 0):
    if "metrics" not in run_data or run_data["metrics"] is None:
        run_data["metrics"] = []
    run_data["metrics"].append({
        "key": key, 
        "value": value, 
        "step": step}
    )
