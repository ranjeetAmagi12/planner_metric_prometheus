# import schedule
import time
from db import get_connection, load_classes
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoInspectionAvailable

from metrics import (
    schedule_item_metrics,
    cp_and_ms_metrics,
    schedule_entry_metrics,
    collection_metrics,
    register_schedule_item_gauge,
    register_cp_and_ms_gauge,
    register_schedule_entry_gauge,
    register_collection_gauge
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

# generate_report()
# schedule the cost report generation every 1 hour
# schedule.every(12).hours.do(generate_report)

Base = automap_base()
app = FastAPI()

engine = get_connection()

Base.prepare(autoload_with=engine)

schedule_item, cp_and_ms, schedule_entry, collection = load_classes(Base)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/schedule_item/metrics")
def read_root() -> Response:
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)

    metrics = register_schedule_item_gauge()
    conn = get_connection()
    cursor = conn.cursor()
    # cursor = get_connection_cursor(conn)

    schedule_item_metrics(cursor, schedule_item, cp_and_ms, schedule_entry, collection , metrics)
    conn.close()
    return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/cp_and_ms/metrics")
def read_root() -> Response:
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)
    
    metrics = register_cp_and_ms_gauge()
    conn = get_connection()
    # cursor = get_connection_cursor(conn)
    cursor = conn.cursor()

    cp_and_ms_metrics(cursor,schedule_item, cp_and_ms, schedule_entry, collection , metrics)
    conn.close()
    return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/schedule_entry/metrics")
def read_root() -> Response:
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)
    
    metrics = register_schedule_entry_gauge()
    conn = get_connection()
    # cursor = get_connection_cursor(conn)
    cursor = conn.cursor()

    schedule_entry_metrics(cursor,schedule_item, cp_and_ms, schedule_entry, collection , metrics)
    conn.close()
    return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/collection/metrics")
def read_root() -> Response:
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)
    
    metrics = register_collection_gauge()
    conn = get_connection()
    # cursor = get_connection_cursor(conn)
    cursor = conn.cursor()
    
    collection_metrics(cursor, schedule_item, cp_and_ms, schedule_entry, collection, metrics)
    conn.close()
    return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)