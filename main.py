
import time
from db import get_connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoInspectionAvailable
import uvicorn
from datetime import date

from metrics import (
    schedule_item_metrics,
    cp_and_ms_metrics,
    register_schedule_item_gauge,
    register_cp_and_ms_gauge
)

import prometheus_client
from typing import Union
from fastapi import FastAPI
from starlette.responses import Response
from prometheus_client import (
    CONTENT_TYPE_LATEST
)
from prometheus_client.core import REGISTRY
from sqlalchemy.ext.automap import automap_base

Base = automap_base()
app = FastAPI()

engine = get_connection()
import psycopg2.extras

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/planner_schedule_details/metrics")
def read_root() -> Response:
    # reset the registry (or set it to an empty registry) of the 
    # Prometheus Python client library..Now, it will start with own registry
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)

    metrics = register_schedule_item_gauge()
    conn = get_connection()
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    schedule_item_metrics(cursor, metrics)
    conn.close()
    return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/planner_channel_details/metrics")
def read_root() -> Response:
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)
    
    metrics = register_cp_and_ms_gauge()
    conn = get_connection()
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    cp_and_ms_metrics(cursor, metrics)
    conn.close()
    return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    uvicorn.run(app)
