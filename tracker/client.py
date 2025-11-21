from pydantic_core import to_jsonable_python
import json
import requests
from .schemas import RunSchema
import datetime

BACKEND_URL = 'http://127.0.0.1:8000'

def send_run(run_data: dict):
    # print(f'''
    #       Sending run {run_data['id']} with: 
    #         Parameters: {run_data.get('parameters', [])}
    #         Metrics: {run_data.get('metrics', [])}
    #         Artifacts: {run_data.get('artifacts', [])}
    #       '''
    # )

    run_obj = RunSchema(**run_data)
    run_json = run_obj.model_dump(mode="json")

    response = requests.post(
        f"{BACKEND_URL}/runs",
        json=run_json
    )
    response.raise_for_status()
    return response.json()
