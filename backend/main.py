from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from pg8000.exceptions import DatabaseError
from backend.db_conn import db_connection,close_conn
from typing import Union
from backend.helper import formated_data, return_data
from backend.parse import populate_db
import tempfile
import shutil
from pprint import pprint



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

@app.put('/api/expenses/upload', status_code= 201)
def put_new_expense(file_path : UploadFile = File(...),table_name: str = Query(...)):
    conn=None
    temp = None
    
    try:
        conn= db_connection()
        if file_path.filename.endswith('csv'):
            temp = tempfile.NamedTemporaryFile(delete=False, suffix = 'csv')
        if file_path.filename.endswith('json'):
            temp = tempfile.NamedTemporaryFile(delete=False, suffix = 'json')
        
        with temp as t:
            shutil.copyfileobj(file_path.file, t)
            t_path = t.name
        new_data = populate_db(file_path=t_path,table_name=table_name)
        
        
        data_inserted=return_data(t_path)
        result = {'New_invoice_added': []}
        
        for data in data_inserted:
            base = {
                    'date': data[0],
                    'description': data[1],
                    'amount': data[2],
                    'category': data[3]}
            result['New_invoice_added'].append(base)
        
            
        return result
    except DatabaseError:
        raise HTTPException(status_code=404,
                            detail='Invoice already added or wrong format')
    finally:
        if conn is not None:
            close_conn(conn)