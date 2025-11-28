import os
import httpx

BACKEND_URL = os.environ.get(
    'TRAINLOG_BACKED',
    'http://127.0.0.1:8000'   
).rstrip('/')

def __mkurl(path: str) -> str:
    if not path.startswith('/'):
        path = '/' + path
    return f"{BACKEND_URL}{path}"

def get(
    path: str,
    timeout: float = 10.0
):
    url = __mkurl(path)
    with httpx.Client(timeout=timeout) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.json()