import sys
import platform
import subprocess

def get_environment():
    python_version = sys.version.split()[0]
    os_name = platform.system()
    try:
        result = subprocess.run(
            ["pip", "freeze"],
            capture_output=True, text=True, check=True
        )
        pip_freeze = result.stdout.splitlines()
    except Exception:
        pip_freeze = []
    return {
        "python_version": python_version,
        "os": os_name,
        "pip_freeze": pip_freeze
    }
