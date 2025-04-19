from fastapi import FastAPI, UploadFile, File, Query, HTTPException,Path
from pg8000.exceptions import DatabaseError
from backend.db_conn import db_connection,close_conn
from typing import Union, Annotated
from backend.helper import formated_data, return_data
from backend.parse import populate_db
import tempfile
import shutil
from pprint import pprint



app = FastAPI()

@app.get('/api/summary/{table}',status_code=200)
def get_expenses_info(table: str ):
    conn = None
    try:
        conn= db_connection()
        query = f"SELECT * FROM {table};"
        raw_data = conn.run(query)
        columns = [col['name'] for col in conn.columns]
        formated_expenses = formated_data(raw_data=raw_data,columns=columns)
        return {'Detailed_expenses': formated_expenses}
    finally:
        if conn is not None:
            close_conn(conn)

@app.put('/api/upload', status_code= 201)
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
                    'id': data[0],
                    'date': data[1],
                    'description': data[2],
                    'amount': data[3],
                    'category': data[4]}
            result['New_invoice_added'].append(base)
        
            
        return result
    except DatabaseError:
        raise HTTPException(status_code=404,
                            detail='Invoice already added or wrong format')
    finally:
        if conn is not None:
            close_conn(conn)


@app.delete('/api/delete/{table}/{id}',status_code=200)
def delete_data(table: str,
                id: Annotated[int, Path(title="The ID of the item to delete")]):
    conn = None
    try:
        conn= db_connection()
        query = f"""
                DELETE FROM {table}
                WHERE id=:id
                RETURNING id,date,description,amount,category;
                """
        response = conn.run(query, id=id)
        
        columns = ['id', 'date', 'description', 'amount', 'category']
        formated = formated_data(columns=columns,raw_data=response)
        return {'Invoice_deleted':formated}
    finally:
        if conn is not None:
            close_conn(conn)
    