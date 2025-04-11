import pg8000.native
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='example.env')


def db_connection():
    return pg8000.native.Connection(
        user = os.environ["PGUSER"],
        password = os.environ["PGPASSWORD"],
        database = os.environ["PGDATABASE"],
        host=os.environ["PGHOST"],
        port = int(os.getenv("PGPORT"))
    )
def close_conn(conn):
    conn.close()