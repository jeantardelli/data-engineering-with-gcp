"""Create the stations table in Cloud SQL"""
#!/usr/bin/env python3

import os
import sqlalchemy
import pymysql

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String

import google.cloud.sql.connector.pymysql
from google.cloud.sql.connector import Connector

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
CLOUD_SQL_REGION = os.environ.get("CLOUD_SQL_REGION")
CLOUD_SQL_INSTANCE_NAME = os.environ.get("CLOUD_SQL_INSTANCE_NAME")
CLOUD_SQL_DATABASE_NAME = os.environ.get("CLOUD_SQL_DATABASE_NAME")

metadata_obj = MetaData()
stations = Table(
    "stations",
    metadata_obj,
    Column("station_id", String(255), primary_key=True),
    Column("name", String(255)),
    Column("region_id", String(10)),
    Column("capacity", Integer()),
)

# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    """Configure and create connections to Cloud SQL instances"""
    conn: pymysql.connections.Connection = connector.connect(
        f"{GCP_PROJECT_ID}:{CLOUD_SQL_REGION}:{CLOUD_SQL_INSTANCE_NAME}",
        "pymysql",
        user="root",
        password=os.environ.get("CLOUD_SQL_ROOT_PASSWORD"),
        db=os.environ.get("CLOUD_SQL_DATABASE_NAME"),
    )
    return conn


# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

with pool.connect() as db_conn:
    # create table
    metadata_obj.create_all(db_conn)

connector.close()
