import os
import shutil
from typing import Dict

def save_artifact(src_path: str, dst_dir: str, artifact_name: str) -> Dict:
    os.makedirs(dst_dir, exist_ok=True)
    dst_path = os.path.join(dst_dir, artifact_name)
    shutil.copy2(src_path, dst_path)
    return {
        "name": artifact_name, 
        "type": "model", 
        "path": dst_path
    }
