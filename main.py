# import schedule
import time
# from db import get_connection, load_classes
from db import get_connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoInspectionAvailable
import uvicorn
from datetime import date

from metrics import (
    # collection_element_metrics,
    # collection_pin_metrics,
    # metadata_metrics,
    # register_collection_element_gauge,
    # register_collection_pin_gauge,
    # register_metadata_gauge,
    # register_schedule_entry_repeat_gauge,
    # schedule_entry_repeat_metrics,
    schedule_item_metrics,
    cp_and_ms_metrics,
    # schedule_entry_metrics,
    # collection_metrics,
    register_schedule_item_gauge,
    register_cp_and_ms_gauge,
    # register_schedule_entry_gauge,
    # register_collection_gauge
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
    # cursor = get_connection_cursor(conn)

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
    # cursor = get_connection_cursor(conn)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    cp_and_ms_metrics(cursor, metrics)
    conn.close()
    return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)

# @app.get("/schedule_entry/metrics")
# def read_root() -> Response:
#     collectors = list(REGISTRY._collector_to_names.keys())
#     for collector in collectors:
#         REGISTRY.unregister(collector)
    
#     metrics = register_schedule_entry_gauge()
#     conn = get_connection()
#     # cursor = get_connection_cursor(conn)
#     cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

#     schedule_entry_metrics(cursor , metrics)
#     conn.close()
#     return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)

# @app.get("/collection/metrics")
# def read_root() -> Response:
#     collectors = list(REGISTRY._collector_to_names.keys())
#     for collector in collectors:
#         REGISTRY.unregister(collector)
    
#     metrics = register_collection_gauge()
#     conn = get_connection()
#     cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
#     collection_metrics(cursor, metrics)
#     conn.close()
#     return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)


# @app.get("/collection_element/metrics")
# def read_root() -> Response:
#     collectors = list(REGISTRY._collector_to_names.keys())
#     for collector in collectors:
#         REGISTRY.unregister(collector)
    
#     metrics = register_collection_element_gauge()
#     conn = get_connection()
#     cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
#     collection_element_metrics(cursor, metrics)
#     conn.close()
#     return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)



# @app.get("/collection_pin/metrics")
# def read_root() -> Response:
#     collectors = list(REGISTRY._collector_to_names.keys())
#     for collector in collectors:
#         REGISTRY.unregister(collector)
    
#     metrics = register_collection_pin_gauge()
#     conn = get_connection()
#     cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
#     collection_pin_metrics(cursor, metrics)
#     conn.close()
#     return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)


# @app.get("/metadata/metrics")
# def read_root() -> Response:
#     collectors = list(REGISTRY._collector_to_names.keys())
#     for collector in collectors:
#         REGISTRY.unregister(collector)
    
#     metrics = register_metadata_gauge()
#     conn = get_connection()
#     cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
#     metadata_metrics(cursor, metrics)
#     conn.close()
#     return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)



# @app.get("/schedule_entry_repeat/metrics")
# def read_root() -> Response:
#     collectors = list(REGISTRY._collector_to_names.keys())
#     for collector in collectors:
#         REGISTRY.unregister(collector)
    
#     metrics = register_schedule_entry_repeat_gauge()
#     conn = get_connection()
#     cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
#     schedule_entry_repeat_metrics(cursor, metrics)
#     conn.close()
#     return Response(prometheus_client.generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    uvicorn.run(app)
