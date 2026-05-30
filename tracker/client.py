import os
import requests
from .schemas import RunSchema

_BACKEND_URL = os.environ.get("ALEXANDRIA_BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

def send_run(run_data: dict):
    run_obj = RunSchema(**run_data)
    run_json = run_obj.model_dump(mode="json")

    response = requests.post(
        f"{_BACKEND_URL}/runs",
        json=run_json,
        timeout=20
    )
    response.raise_for_status()
    return response.json()
