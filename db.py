import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus


import psycopg2

def get_connection():
    #establishing the connection
    conn = psycopg2.connect(
        database='postgres',
        user='newuser',
        password='newuser',
        host='localhost',
        port=5432
    )
    return conn

def get_connection_cursor(conn):
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    return cursor
