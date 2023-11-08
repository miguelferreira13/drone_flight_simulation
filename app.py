import json
import sqlite3

from fastapi import FastAPI

app = FastAPI()

conn = sqlite3.connect("log.db", check_same_thread=False)

@app.get("/details")
def get_details():
    cursor = conn.cursor()

    # Create a table for storing logs
    cursor.execute("""
        select 
            object_id, 
            min(timestamp) min_timestamp,
            max(timestamp) max_timestamp,
            '/trajectory/' || object_id || '/' || min(timestamp) || '/' || max(timestamp) example_trajectory_query,
            '/snapshot/' || max(sector_id) || '/' || min(timestamp) || '/' || max(timestamp) example_sector_query,
            count(*) records
        from logs
        group by 1
        """)

    data = []
    for row in cursor.fetchall():
        dict_row = {}
        for i, col in enumerate(row):
            dict_row.update({cursor.description[i][0]:col})
        data.append(dict_row)

    return data


@app.get("/trajectory/{object_id}/{start_time}/{end_time}")
def get_object_trajectory(object_id, start_time, end_time):

    cursor = conn.cursor()
    cursor.execute("""
        select 
            timestamp,
            object_id,
            payload,
            sector_id,
            data
        from logs
        where 
            object_id = ?
            and timestamp between ? and ?
        """, (object_id, start_time, end_time))

    data = []
    for row in cursor.fetchall():
        dict_row = {}
        for i, col in enumerate(row):
            col_name = cursor.description[i][0]
            if col_name == "data":
                dict_row.update({"details":json.loads(col)})
            else:
                dict_row.update({col_name:col})
        data.append(dict_row)

    return data

@app.get("/snapshot/{sector_id}/{start_time}/{end_time}")
def get_sector_snapshot(sector_id, start_time, end_time):

    cursor = conn.cursor()
    cursor.execute("""
        select 
            timestamp,
            object_id,
            sector_id,
            data
        from logs
        where 
            sector_id = ?
            and timestamp between ? and ?
        order by timestamp asc
        """, (sector_id, start_time, end_time))

    data = []
    for row in cursor.fetchall():
        dict_row = {}
        for i, col in enumerate(row):
            col_name = cursor.description[i][0]
            if col_name == "data":
                dict_row.update({"details":json.loads(col)})
            else:
                dict_row.update({col_name:col})
        data.append(dict_row)

    return data
    