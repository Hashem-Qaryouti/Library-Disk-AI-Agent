import sqlite3
from typing import List, Dict, Any

DB_PATH = "db/library.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def query_db(query: str, params=()) -> List[Dict[str, Any]]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, params)
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows

def execute_db(query: str, params=()) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id