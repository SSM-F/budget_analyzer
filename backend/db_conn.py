import pg8000.native
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='example.env')


def db_connection():
    return pg8000.native.Connection(
        user = os.environ["PG_USER"],
        password = os.environ["PG_PASSWORD"],
        database = os.environ["PG_DATABASE"],
        host=os.environ["PG_HOST"],
        port = int(os.getenv("PG_PORT"))
    )
def close_conn(conn):
    conn.close()