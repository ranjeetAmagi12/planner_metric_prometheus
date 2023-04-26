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
        'planner_schedule_details': Gauge('planner_schedule_details', 'Details of the Schedule items', ['schedule_date', 'collection_id', 'tenant_id', 'feed_id','name'])
    }

def register_cp_and_ms_gauge():
    return {
        'planner_channel_details': Gauge('planner_channel_details', 'Details of the cp_and_ms', ['tenant_id', 'cloudport_feed_id', 'account_name', 'name'])
    }

# def register_schedule_entry_gauge():
#     return {
#         'schedule_entry_details': Gauge('schedule_entry_details', 'Details of the schedule_entry)', ['id', 'start_date', 'end_date', 'target_duration','tenant_id', 'feed_id', 'created_at', 'updated_at'])
#     }

# def register_collection_gauge():
#     return {
#         'collection_details': Gauge('collection_details', 'Details of the collection_details', ['id', 'tenant_id', 'feed_id','episode_target_duration','collection_type','created_at', 'updated_at'])
#     }
   
# def register_collection_element_gauge():
#     return {
#         'collection_element_details': Gauge('collection_element_details', 'Details of the collection_element_details', ['id','collection_id','runtime', 'asset_id','external_id','created_at', 'updated_at','is_adbreak_segment','meta'])
#     }

# def register_collection_pin_gauge():
#     return {
#         'collection_pin_details': Gauge('collection_pin_details', 'Details of the collection_pin_details', ['id','collection_id','pin_position','runtime', 'asset_id','external_id','created_at', 'updated_at','som','image'])
#     }

# def register_metadata_gauge():
#     return {
#         'metadata_details': Gauge('metadata_details', 'Details of the metadata_details', ['id', 'tenant_id','name','name_prefix','description_minor','description_major','rating_code','rating_provider','image_url','genres','publication_date','disabled','created_at', 'updated_at'])
#     }

# def register_schedule_entry_repeat_gauge():
#     return {
#         'schedule_entry_repeat_details': Gauge('schedule_entry_repeat_details', 'Details of the schedule_entry_repeat_details', ['id', 'schedule_entry_id', 'start_date','end_date','per_day','frequency','pattern','start_times', 'updated_at'])
#     }

def schedule_item_metrics(cursor, metrics):
    cursor.execute("SELECT * FROM schedule_item WHERE start_time BETWEEN now() AND (date_trunc('day', now()) + interval '90 day') ORDER BY start_time")
    #cursor.execute("SELECT * FROM schedule_item ORDER BY id ASC LIMIT 100")
    schedule_items = cursor.fetchall()
    prevDay = None
    duration = 0
    variantType = None

    for item in schedule_items:
        start_time = item['start_time']
        day =  start_time.date()
        if prevDay == None:
            prevDay = day
            duration =  item['runtime']
        elif prevDay == day:
            duration = duration + item['runtime']
        else:
            metrics['planner_schedule_details'].labels(schedule_date=prevDay, collection_id=item['collection_id'], tenant_id=item['tenant_id'], feed_id=item['feed_id'], name=item['name']).set(duration/1000)
            duration = item['runtime']
            prevDay = day
        
    metrics['planner_schedule_details'].labels( schedule_date=day, collection_id=item['collection_id'], tenant_id=item['tenant_id'], feed_id=item['feed_id'], name=item['name']).set(duration/1000)
            
        # print(item)
        # duration = get_scheduled_seconds(item['target_duration'],cursor)
        # metrics['schedule_item_details'].labels( start_time=item['start_time'], end_time=item['end_time'], collection_id=item['collection_id'], tenant_id=item['tenant_id'], feed_id=item['feed_id'], target_duration=item['target_duration'], created_at=item['created_at'], updated_at=item['updated_at'],name=item['name'],meta=item['meta']).set(duration)

def cp_and_ms_metrics(cursor, metrics):
   # cursor.execute("SELECT * FROM cp_and_ms ")
    cursor.execute("SELECT c.tenant_id,c.cloudport_feed_id,c.account_name,c.name,COUNT(*) as count FROM cp_and_ms As c INNER JOIN schedule_item S ON c.cloudport_feed_id = S.feed_id GROUP BY c.tenant_id,c.cloudport_feed_id,c.account_name,c.name")
    cp_and_mss = cursor.fetchall()
    for entry in cp_and_mss:
         metrics['planner_channel_details'].labels(tenant_id=entry['tenant_id'], cloudport_feed_id=entry['cloudport_feed_id'], account_name=entry['account_name'],name=entry['name']).set(entry['count'])
        # metrics['planner_channel_details'].labels(tenant_id=entry['tenant_id'], cloudport_feed_id=entry['cloudport_feed_id'], account_name=entry['account_name'],name=entry['name']).set(getNoOfTimesScheduled(entry['cloudport_feed_id']))
      
# def schedule_entry_metrics(cursor, metrics):
#     cursor.execute("SELECT * FROM schedule_entry ORDER BY id ASC LIMIT 100")
#     schedule_entrys = cursor.fetchall()
#     for entry in schedule_entrys:
#         metrics['schedule_entry_details'].labels(id=entry['id'], start_date=entry['start_date'], end_date=entry['end_date'],target_duration=entry['target_duration'],tenant_id=entry['tenant_id'], feed_id=entry['feed_id'], created_at=entry['created_at'], updated_at=entry['updated_at']).set(1)
      
# def collection_metrics(cursor, metrics):
#     cursor.execute("SELECT * FROM collection ORDER BY id ASC LIMIT 100")
#     collections = cursor.fetchall()
#     for entry in collections:
#         metrics['collection_details'].labels(id=entry['id'], tenant_id=entry['tenant_id'], feed_id=entry['feed_id'], episode_target_duration=entry['episode_target_duration'], collection_type=entry['collection_type'], created_at=entry['created_at'], updated_at=entry['updated_at']).set(1)
    
#def collection_element_metrics(cursor, metrics):
#     cursor.execute("SELECT * FROM collection_element ORDER BY id ASC LIMIT 100")
#     entries = cursor.fetchall()
#     for entry in entries:
#         metrics['collection_element_details'].labels(id=entry['id'],collection_id=entry['collection_id'],runtime=entry['runtime'], asset_id=entry['asset_id'],external_id=entry['external_id'],created_at=entry['created_at'], updated_at=entry['updated_at'],is_adbreak_segment=entry['is_adbreak_segment'],meta=entry['meta']).set(1)
    
# def collection_pin_metrics(cursor, metrics):
#     cursor.execute("SELECT * FROM collection_pin ORDER BY id ASC LIMIT 100")
#     entries = cursor.fetchall()
#     for entry in entries:
#         metrics['collection_pin_details'].labels(id=entry['id'],collection_id=entry['collection_id'],pin_position=entry['pin_position'],runtime=entry['runtime'], asset_id=entry['asset_id'],external_id=entry['external_id'],created_at=entry['created_at'], updated_at=entry['updated_at'],som=entry['som'],image=entry['image']).set(1)
    
# def metadata_metrics(cursor, metrics):
#     cursor.execute("SELECT * FROM metadata ORDER BY id ASC LIMIT 100")
#     entries = cursor.fetchall()
#     for entry in entries:
#         metrics['metadata_details'].labels(id=entry['id'], tenant_id=entry['tenant_id'],name=entry['name'],name_prefix=entry['name_prefix'],description_minor=entry['description_minor'],description_major=entry['description_major'],rating_code=entry['rating_code'],rating_provider=entry['rating_provider'],image_url=entry['image_url'],genres=entry['genres'],publication_date=entry['publication_date'],disabled=entry['disabled'],created_at=entry['created_at'], updated_at=entry['updated_at']).set(1)
    
# def schedule_entry_repeat_metrics(cursor, metrics):
#     cursor.execute("SELECT * FROM schedule_entry_repeat ORDER BY id ASC LIMIT 100")
#     entries = cursor.fetchall()
#     for entry in entries:
#         metrics['schedule_entry_repeat_details'].labels(id=entry['id'], schedule_entry_id=entry['schedule_entry_id'], start_date=entry['start_date'],end_date=entry['end_date'],per_day=entry['per_day'],frequency=entry['frequency'],pattern=entry['pattern'],start_times=entry['start_times'], updated_at=entry['updated_at']).set(1)


def get_scheduled_seconds(target_duration,cursor):
    cursor.execute("SELECT * FROM schedule_entry_repeat ORDER BY id ASC LIMIT 100")
    entries = cursor.fetchall()
    for entry in entries:
        metrics['schedule_entry_repeat_details'].labels(id=entry['id'], schedule_entry_id=entry['schedule_entry_id'], start_date=entry['start_date'],end_date=entry['end_date'],per_day=entry['per_day'],frequency=entry['frequency'],pattern=entry['pattern'],start_times=entry['start_times'], updated_at=entry['updated_at']).set(1)



def getNoOfTimesScheduled(cloudport_feed_id):
    cursor.execute("SELECT COUNT(*) FROM schedule_item WHERE feed_id = cloudport_feed_id")
    entries = cursor.fetchall()
    for entry in entries:
        metrics['schedule_entry_repeat_details'].labels(id=entry['id'], schedule_entry_id=entry['schedule_entry_id'], start_date=entry['start_date'],end_date=entry['end_date'],per_day=entry['per_day'],frequency=entry['frequency'],pattern=entry['pattern'],start_times=entry['start_times'], updated_at=entry['updated_at']).set(1)

