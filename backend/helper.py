from backend.db_conn import db_connection, close_conn
from backend.file_readers.read_csv import read_csv
from backend.file_readers.read_json import read_json
from fastapi import File,UploadFile

def formated_data(columns,raw_data):
    formated_result = []
    for data in raw_data:
        data_dict = dict(zip(columns,data))
        formated_result.append(data_dict)
    return formated_result

def return_data(file_path):
    data = None
    try:
        
        if file_path.endswith('csv'):
            data = read_csv(file_path)
        if file_path.endswith('json'):
            data = read_json(file_path)

        query = """SELECT id,date,description,amount,category FROM expenses
                    WHERE id=:id AND description=:description 
                    AND amount=:amount AND category=:category AND date=:date;
                    """
        conn= db_connection()

        rows = data['Invoice_Data']

        data_result = []
        for row in rows:
            x = conn.run(query,
                     id=row['id'],
                     date=row['Date'],
                     description=row['Description'],
                     amount=row['Amount'],
                     category = row['Category']) 

            data_result.append(x[0])

        return data_result
    finally:
        close_conn(conn)