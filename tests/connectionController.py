import requests
import json
from typing import Dict, Any

URL = "http://localhost:8000"


def http_get(resource: str):
    response = requests.get(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"})
    return response

def http_delete(resource: str):
    response = requests.delete(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"})
    return response

def http_post(resource: str, data: Dict[str, Any]):
    response = requests.post(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"}, data=json.dumps(data))
    return response

def http_post_qs(resource: str, query_string: str):
    response = requests.post(url=f"{URL}/{resource}?name={query_string}", headers={})
    return response

def http_put(resource: str, data: Dict[str, Any]):
    response = requests.put(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"}, data=json.dumps(data))
    return response
