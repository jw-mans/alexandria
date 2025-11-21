import hashlib
import subprocess
import os
from typing import List, Dict

def hash_file(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def get_tracked_files(file_paths: List[str]) -> List[Dict]:
    return [{
        "path": f, 
        "hash": hash_file(f)
    } for f in file_paths]

def get_all_python_files(root_dir: str, exclude: set = set()) -> List[str]:
    files = []
    for dirpath, _, filenames in os.walk(root_dir):
        if any(excl in dirpath for excl in exclude):
            continue
        for f in filenames:
            if f.endswith(".py"):
                files.append(os.path.join(dirpath, f))
    return files

def get_git_commit() -> str:
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        return commit
    except Exception:
        return "unknown"
