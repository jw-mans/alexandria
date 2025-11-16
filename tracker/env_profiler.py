import sys
import platform
import subprocess

def get_environment():
    python_version = sys.version.split()[0]
    os_name = platform.system()
    pip_freeze = subprocess.getoutput("pip freeze").splitlines()
    return {
        "python_version": python_version,
        "os": os_name,
        "pip_freeze": pip_freeze
    }
