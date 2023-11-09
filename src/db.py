from sqlite3 import Connection, connect

def get_conn() -> Connection:

    conn = connect("log.db")
    cursor = conn.cursor()

    # create a table for storing logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            object_id TEXT, 
            sector_id TEXT,
            payload TEXT,
            data TEXT
        )""")

    cursor.execute("""CREATE INDEX timestamp_object_id_index
        ON logs(timestamp, object_id)""")

    cursor.execute("""CREATE INDEX timestamp_sector_id_index
        ON logs(timestamp, sector_id)""")

    conn.commit()
    return conn
