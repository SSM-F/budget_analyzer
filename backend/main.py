from fastapi import FastAPI
from backend.db_conn import db_connection,close_conn
from typing import Union
from backend.helper import formated_data

app = FastAPI()

@app.get('/api/expenses',status_code=200)
def get_expenses_info():
    conn = None
    try:
        conn= db_connection()
        query = f"SELECT * FROM expenses;"
        raw_data = conn.run(query)
        columns = [col['name'] for col in conn.columns]
        formated_expenses = formated_data(raw_data=raw_data,columns=columns)
        return {'Detailed_expenses': formated_expenses}
    finally:
        if conn is not None:
            close_conn(conn)