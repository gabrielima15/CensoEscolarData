import sqlite3
from flask import g
DATABASE = 'censo.db'


def get_connection():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(DATABASE)
    return conn

