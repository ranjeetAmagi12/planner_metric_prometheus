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
   
def register_collection_element_gauge():
    return {
        'collection_element_details': Gauge('collection_element_details', 'Details of the collection_element_details', ['id','collection_id','runtime', 'asset_id','external_id','created_at', 'updated_at','is_adbreak_segment','meta'])
    }

def register_collection_pin_gauge():
    return {
        'collection_pin_details': Gauge('collection_pin_details', 'Details of the collection_pin_details', ['id','collection_id','pin_position','runtime', 'asset_id','external_id','created_at', 'updated_at','som','image'])
    }

def register_metadata_gauge():
    return {
        'metadata_details': Gauge('metadata_details', 'Details of the metadata_details', ['id', 'tenant_id','name','name_prefix','description_minor','description_major','rating_code','rating_provider','image_url','genres','publication_date','disabled','created_at', 'updated_at'])
    }

def register_schedule_entry_repeat_gauge():
    return {
        'schedule_entry_repeat_details': Gauge('schedule_entry_repeat_details', 'Details of the schedule_entry_repeat_details', ['id', 'schedule_entry_id', 'start_date','end_date','per_day','frequency','pattern','start_times', 'updated_at'])
    }

def schedule_item_metrics(cursor, metrics):
    cursor.execute("SELECT * FROM schedule_item ORDER BY id ASC LIMIT 100")
    schedule_items = cursor.fetchall()
    for item in schedule_items:
        # print(item)
        metrics['schedule_item_details'].labels(id=item['id'], schedule_entry_id=item['schedule_entry_id'], start_time=item['start_time'], end_time=item['end_time'], collection_id=item['collection_id'], tenant_id=item['tenant_id'], feed_id=item['feed_id'], target_duration=item['target_duration'], created_at=item['created_at'], updated_at=item['updated_at']).set(1)

def cp_and_ms_metrics(cursor, metrics):
    cursor.execute("SELECT * FROM cp_and_ms LIMIT 100")
    cp_and_mss = cursor.fetchall()
    for entry in cp_and_mss:
        metrics['cp_and_ms_details'].labels(tenant_id=entry['tenant_id'], cloudport_feed_id=entry['cloudport_feed_id'], account_name=entry['account_name'], platform_code=entry['platform_code']).set(1)
      
def schedule_entry_metrics(cursor, metrics):
    cursor.execute("SELECT * FROM schedule_entry ORDER BY id ASC LIMIT 100")
    schedule_entrys = cursor.fetchall()
    for entry in schedule_entrys:
        metrics['schedule_entry_details'].labels(id=entry['id'], start_date=entry['start_date'], end_date=entry['end_date'],target_duration=entry['target_duration'],tenant_id=entry['tenant_id'], feed_id=entry['feed_id'], created_at=entry['created_at'], updated_at=entry['updated_at']).set(1)
      
def collection_metrics(cursor, metrics):
    cursor.execute("SELECT * FROM collection ORDER BY id ASC LIMIT 100")
    collections = cursor.fetchall()
    for entry in collections:
        metrics['collection_details'].labels(id=entry['id'], tenant_id=entry['tenant_id'], feed_id=entry['feed_id'], episode_target_duration=entry['episode_target_duration'], collection_type=entry['collection_type'], created_at=entry['created_at'], updated_at=entry['updated_at']).set(1)
    
def collection_element_metrics(cursor, metrics):
    cursor.execute("SELECT * FROM collection_element ORDER BY id ASC LIMIT 100")
    entries = cursor.fetchall()
    for entry in entries:
        metrics['collection_element_details'].labels(id=entry['id'],collection_id=entry['collection_id'],runtime=entry['runtime'], asset_id=entry['asset_id'],external_id=entry['external_id'],created_at=entry['created_at'], updated_at=entry['updated_at'],is_adbreak_segment=entry['is_adbreak_segment'],meta=entry['meta']).set(1)
    
def collection_pin_metrics(cursor, metrics):
    cursor.execute("SELECT * FROM collection_pin ORDER BY id ASC LIMIT 100")
    entries = cursor.fetchall()
    for entry in entries:
        metrics['collection_pin_details'].labels(id=entry['id'],collection_id=entry['collection_id'],pin_position=entry['pin_position'],runtime=entry['runtime'], asset_id=entry['asset_id'],external_id=entry['external_id'],created_at=entry['created_at'], updated_at=entry['updated_at'],som=entry['som'],image=entry['image']).set(1)
    
def metadata_metrics(cursor, metrics):
    cursor.execute("SELECT * FROM metadata ORDER BY id ASC LIMIT 100")
    entries = cursor.fetchall()
    for entry in entries:
        metrics['metadata_details'].labels(id=entry['id'], tenant_id=entry['tenant_id'],name=entry['name'],name_prefix=entry['name_prefix'],description_minor=entry['description_minor'],description_major=entry['description_major'],rating_code=entry['rating_code'],rating_provider=entry['rating_provider'],image_url=entry['image_url'],genres=entry['genres'],publication_date=entry['publication_date'],disabled=entry['disabled'],created_at=entry['created_at'], updated_at=entry['updated_at']).set(1)
    
def schedule_entry_repeat_metrics(cursor, metrics):
    cursor.execute("SELECT * FROM schedule_entry_repeat ORDER BY id ASC LIMIT 100")
    entries = cursor.fetchall()
    for entry in entries:
        metrics['schedule_entry_repeat_details'].labels(id=entry['id'], schedule_entry_id=entry['schedule_entry_id'], start_date=entry['start_date'],end_date=entry['end_date'],per_day=entry['per_day'],frequency=entry['frequency'],pattern=entry['pattern'],start_times=entry['start_times'], updated_at=entry['updated_at']).set(1)