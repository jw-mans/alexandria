try:
    from datasets import Dataset as HFDataset
except ImportError:
    HFDataset = None

from functools import wraps
from contextvars import ContextVar
import os
import pandas as pd
import datetime

from .logger import create_run
from .client import send_run
from .code_profiler import (
    get_git_commit, get_tracked_files, get_all_python_files
)
from .env_profiler import get_environment
from .data_profiler import profile_dataset_auto
from .model_saver import save_artifact

# Instead of embedding run_data in kwargs (which broke the signatures of
# train functions), we use a ContextVar for the current run. This does not
# require changing the API of train functions.
current_run: ContextVar[dict] = ContextVar('current_run', default=None)


def _profile_code(func):
    root_dir = os.path.dirname(os.path.abspath(func.__code__.co_filename))
    python_files = get_all_python_files(root_dir)
    return {
        "git_commit": get_git_commit(),
        "entrypoint": func.__code__.co_filename,
        "tracked_files": get_tracked_files(python_files)
    }


def _profile_artifacts(artifacts_dir):
    output = {}
    if os.path.exists(artifacts_dir):
        for f in os.listdir(artifacts_dir):
            full = os.path.join(artifacts_dir, f)
            output[f] = {
                "path": full,
                "type": "model"
                if f.lower().endswith((".pt", ".pth", ".pkl"))
                else "file",
            }
    return output


def track(experiment_name, artifacts_dir="runs/run_auto"):
    """
    Autologging decorator run.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            run_data = create_run(experiment_name)
            token = current_run.set(run_data)

            if not run_data.get('timestamp_start'):
                run_data['timestamp_start'] = datetime.datetime.now().isoformat()

            try:
                result = func(*args, **kwargs)
            finally:
                run_data['timestamp_end'] = datetime.datetime.now().isoformat()

                total_args = list(args) + list(kwargs.values())

                # dataset autodetection — search args + kwargs
                for v in total_args:
                    try:
                        if isinstance(v, str) and v.endswith(".csv") and os.path.exists(v):
                            run_data["dataset"] = profile_dataset_auto(v)
                            break
                        if isinstance(v, pd.DataFrame):
                            run_data["dataset"] = profile_dataset_auto(v)
                            break
                        if HFDataset and isinstance(v, HFDataset):
                            run_data["dataset"] = profile_dataset_auto(v)
                            break
                    except Exception:
                        pass

                # code, artifacts, environment profiling — each wrapped
                # individually so a failure in one doesn't mask the original
                # exception from func or skip the backend send
                try:
                    run_data['code'] = _profile_code(func)
                except Exception as ex:
                    print(f"Code profiling failed: {ex}")

                try:
                    run_data['artifacts'] = _profile_artifacts(artifacts_dir)
                except Exception as ex:
                    print(f"Artifact profiling failed: {ex}")

                try:
                    run_data['environment'] = get_environment()
                except Exception as ex:
                    print(f"Environment profiling failed: {ex}")

                try:
                    send_run(run_data)
                    print(f"Run {run_data['id']} sent to backend")
                except Exception as ex:
                    print(f"Failed to send run to backend: {ex}")

                current_run.reset(token)

            return result
        return wrapper
    return decorator


def log_metric(
    name: str,
    value: float,
    step: int = None
):
    run = current_run.get()
    if not run:
        raise RuntimeError(
            "No active run in context. Use @track or start a run."
        )
    if 'metrics' not in run or run['metrics'] is None:
        run['metrics'] = {}
    if name not in run['metrics']:
        run['metrics'][name] = []
    run['metrics'][name].append(value)
