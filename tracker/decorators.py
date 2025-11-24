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

"""
Instead of embedding run_data in kwargs (which 
broke the signatures of train functions), we use 
contextvar for the current run. This does not 
require changing the API train functions.
# TODO: check is it safe
"""
current_run: ContextVar[dict] = ContextVar('current_run', default=None)

class __Prof:
    def _code_profiling(func):
        root_dir = os.path.dirname(os.path.abspath(func.__code__.co_filename))
        python_files = get_all_python_files(root_dir)
        output = {
            "git_commit": get_git_commit(),
            "entrypoint": func.__code__.co_filename,
            "tracked_files": get_tracked_files(python_files)
        }
        return output

    def _artifacts_profiling(func, artifacts_dir):
        output = {}
        if os.path.exists(artifacts_dir):
            for f in os.listdir(artifacts_dir):
                full = os.path.join(artifacts_dir, f)
                output[f] = {
                    "path": full,
                    "type": "model" 
                    if f.lower().endswith((".pt", ".pth", ".pkl")) 
                    else "file",
                    # optionally add file hash
                }
        return output
    
    def _env_profiling():
        output = get_environment()
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
                run_data['timestamp_start'] = datetime\
                    .datetime.now().isoformat()
            
            try:
                result = func(*args, **kwargs) # train func run
            finally:
                run_data['timestamp_end'] = datetime\
                    .datetime.now().isoformat()
                
                total_args = list(args) + list(kwargs.values())

                # dataset autodetection
                # search args + kwargs
                for v in total_args:
                    def __mkcol():
                        from .data_profiler import profile_dataset_auto
                        run_data["dataset"] = profile_dataset_auto(v)

                    try:
                        # CSV file (path provided as string)
                        if isinstance(v, str) and v.endswith(".csv") and os.path.exists(v):
                            __mkcol()
                            break

                        # pandas DataFrame
                        if isinstance(v, pd.DataFrame):
                            __mkcol()
                            break

                        # HF Dataset
                        if HFDataset and isinstance(v, HFDataset):
                            __mkcol()
                            break
                    except Exception:
                        # profiling failed - ignore & continue ?
                        pass

                # code profiling
                run_data['code'] = __Prof._code_profiling(func)

                # artifact profiling
                run_data['artifacts'] = __Prof._artifacts_profiling(func, artifacts_dir)

                # environment profiling
                run_data['environment'] = __Prof._env_profiling()

                # backend sending
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
            """
            No active run in context.
            Use @track or start a run.
            """
        )
    if 'metrics' not in run or run['metrics'] is None:
        run['metrics'] = {}
    if name not in run['metrics']:
        run['metrics'][name] = []
    run['metrics'][name].append(value)