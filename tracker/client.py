from pydantic_core import to_jsonable_python
import json
import requests
from .schemas import RunSchema
import datetime

BACKEND_URL = 'http://127.0.0.1:8000'

def send_run(run_data: dict):
    run_obj = RunSchema(**run_data)
    run_json = run_obj.model_dump(mode="json") # .dict() in pydantic v1

    response = requests.post(
        f"{BACKEND_URL}/runs",
        json=run_json,
        timeout=20
    )
    response.raise_for_status()
    return response.json()
