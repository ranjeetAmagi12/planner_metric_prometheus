import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from prometheus_client import Gauge
from sqlalchemy import select

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# def register_schedule_item_gauge():
#     return {
#         'schedule_item_details': Gauge('schedule_item', 'scheduled programs in the app', ['state']),
#         # 'account_count': Gauge('account_count', 'amagi now account metrics', ['state']),
#         # 'channel_count': Gauge('channel_count', 'amagi now channel metrics', ['state']),
#         # 'ingest_count': Gauge('ingest_count', 'amagi now ingest metrics', ['state']),
#         # 'delivery_count': Gauge('delivery_count', 'amagi now delivery metrics', ['state']),
#         # 'intent_count': Gauge('intent_count', 'amagi now intent metrics', ['state'])
#     }

def register_schedule_item_gauge():
    return {
        'schedule_item_details': Gauge('schedule_item_details', 'Details of the Schedule items', ['id', 'schedule_entry_id', 'start_time', 'end_time', 'collection_id', 'tenant_id', 'feed_id', 'target_duration', 'created_at', 'updated_at'])
    }

def register_cp_and_ms_gauge():
    return {
        'cp_and_ms_details': Gauge('cp_and_ms_details', 'Details of the cp_and_ms', ['tenant_id', 'cloudport_feed_id', 'account_name', 'platform_code'])
    }

def register_schedule_entry_gauge():
    return {
        'schedule_entry_details': Gauge('schedule_entry_details', 'Details of the schedule_entry)', ['id', 'start_date', 'end_date', 'target_duration','tenant_id', 'feed_id', 'created_at', 'updated_at'])
    }

def register_collection_gauge():
    return {
        'collection_details': Gauge('collection_details', 'Details of the collection_details', ['id', 'tenant_id', 'feed_id','episode_target_duration','collection_type','created_at', 'updated_at'])
    }
   
def schedule_item_metrics(cursor, schedule_item, cp_and_ms, schedule_entry, collection , metrics):
    schedule_items = cursor.execute(schedule_item).all()
    for item in schedule_item:
        metrics['schedule_item_details'].labels(id=item.id, schedule_entry_id=item.schedule_entry_id, start_time=item.start_time, end_time=item.end_time, collection_id=item.collection_id, tenant_id=item.tenant_id, feed_id=item.feed_id, target_duration=item.target_duration, created_at=item.created_at, updated_at=item.updated_at).set(1)
       
def cp_and_ms_metrics(cursor,schedule_item, cp_and_ms, schedule_entry, collection , metrics):
    cp_and_mss = cursor.execute(cp_and_ms).all()
    for entry in cp_and_mss:
        metrics['cp_and_ms_details'].labels(tenant_id=entry.tenant_id, cloudport_feed_id=entry.cloudport_feed_id, account_name=entry.account_name, platform_code=entry.platform_code).set(1)
      
def schedule_entry_metrics(cursor,schedule_item, cp_and_ms, schedule_entry, collection, metrics):
    schedule_entrys = cursor.execute(schedule_entry).all()
    for entry in schedule_entrys:
        metrics['schedule_entry_details'].labels(id=entry.id, start_date=entry.start_date, end_date=entry.end_date,target_duration=entry.target_duration,tenant_id=entry.tenant_id, feed_id=entry.feed_id, created_at=entry.created_at, updated_at=entry.updated_at).set(1)
      
def collection_metrics(cursor, schedule_item, cp_and_ms, schedule_entry, collection, metrics):
    collections = cursor.execute(collection).all()
    for entry in collections:
        metrics['schedule_entry_details'].labels(id=entry.id, tenant_id=entry.tenant_id, feed_id=entry.feed_id, episode_target_duration=entry.episode_target_duration, collection_type=entry.collection_type, created_at=entry.created_at, updated_at=entry.updated_at).set(1)
    