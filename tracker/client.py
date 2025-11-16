from pydantic.json import pydantic_encoder
import json
import requests
from .schemas import RunSchema

BACKEND_URL = 'http://127.0.0.1:8000'

def send_run(run_data: dict):
    run_obj = RunSchema(**run_data)
    run_json = json.dumps(run_obj.dict(), default=pydantic_encoder)
    response = requests.post(
        f"{BACKEND_URL}/runs",
        data=run_json,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()
