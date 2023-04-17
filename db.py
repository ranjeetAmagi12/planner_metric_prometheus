import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus


import psycopg2

def get_connection():
    #establishing the connection
    # conn_string = "os.getenv('Postgres_HOST', 'localhost') os.getenv('Postgres_User', 'newuser') os.getenv('password', 'newuser') os.getenv('database', 'postgres') os.getenv('port', 5432)"
    # conn = psycopg2.connect(conn_string)
    conn = psycopg2.connect(
        database="postgres",
        user='newuser',
        password='newuser',
        host='localhost',
        port= '5432'
    )
    return conn

def get_connection_cursor(conn):
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    return cursor

# def get_connection():
#     url="mysql+mysqldb://{0}:%s@{1}:{2}/{3}".format(
#         os.getenv('MYSQL_USERNAME', 'root'), os.getenv('MYSQL_HOST', 'localhost'), os.getenv('MYSQL_PORT', '3306'), os.getenv('MYSQL_DB', 'amaginow')
#     )
#     return create_engine(url % quote_plus(os.getenv('MYSQL_PASSWORD', 'Amagi@560076')))

def load_classes(Base):
    schedule_item = Base.classes.schedule_item
    cp_and_ms = Base.classes.cp_and_ms
    schedule_entry = Base.classes.schedule_entry
    collection = Base.classes.collection
    return schedule_item, cp_and_ms, schedule_entry, collection