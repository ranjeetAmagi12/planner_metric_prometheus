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
        'planner_schedule_details': Gauge('planner_schedule_details', 'Details of the Schedule items', ['schedule_date', 'account_name','channel_name', 'tenant_id', 'feed_id'])
    }

def register_cp_and_ms_gauge():
    return {
        'planner_channel_details': Gauge('planner_channel_details', 'Details of the cp_and_ms', ['tenant_id', 'cloudport_feed_id', 'account_name', 'chanel_name'])
    }

def schedule_item_metrics(cursor, metrics):
    cursor.execute("SELECT S.start_time,S.runtime,C.name,C.account_name,S.feed_id,S.tenant_id FROM schedule_item S INNER JOIN cp_and_ms C ON C.cloudport_feed_id = S.feed_id WHERE start_time BETWEEN now() AND (now() + interval '90 day') ORDER BY S.start_time")
    #cursor.execute("SELECT * FROM schedule_item ORDER BY id ASC LIMIT 100")
    schedule_items = cursor.fetchall()
    prevDay = None
    prevItem = None
    duration = 0
    for item in schedule_items:
        start_time = item['start_time']
        day =  start_time.date()
        if prevDay == None:
            prevDay = day
            prevItem = item
            duration =  item['runtime']
        elif prevDay == day:
            duration = duration + item['runtime']
        else:
            metrics['planner_schedule_details'].labels(schedule_date=prevDay,account_name=prevItem['account_name'],channel_name=prevItem['name'],tenant_id=prevItem['tenant_id'],feed_id=prevItem['feed_id']).set(duration/1000)
            duration = item['runtime']
            prevDay = day
            prevItem = item
        
    metrics['planner_schedule_details'].labels(schedule_date=day,account_name=item['account_name'],channel_name=item['name'],tenant_id=item['tenant_id'],feed_id=item['feed_id']).set(duration/1000)
                    
def cp_and_ms_metrics(cursor, metrics):
    cursor.execute("SELECT c.tenant_id,c.cloudport_feed_id,c.account_name,c.name,COUNT(*) as count FROM cp_and_ms As c INNER JOIN schedule_item S ON c.cloudport_feed_id = S.feed_id GROUP BY c.tenant_id,c.cloudport_feed_id,c.account_name,c.name")
    cp_and_mss = cursor.fetchall()
    for entry in cp_and_mss:
         metrics['planner_channel_details'].labels(tenant_id=entry['tenant_id'], cloudport_feed_id=entry['cloudport_feed_id'], account_name=entry['account_name'],chanel_name=entry['name']).set(entry['count'])
