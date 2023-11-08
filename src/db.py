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
        )
        """)

    conn.commit()
    return conn
