import sqlite3

def get_initialized_database_connection():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS hashtags (word text, doc text, phrase text)')
    return c