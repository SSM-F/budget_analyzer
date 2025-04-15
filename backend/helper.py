from backend.db_conn import db_connection, close_conn
from backend.read_csv import read_csv

def formated_data(columns,raw_data):
    formated_result = []
    for data in raw_data:
        data_dict = dict(zip(columns,data))
        formated_result.append(data_dict)
    return formated_result

def return_data(file_path):
    query = """SELECT date,description,amount,category FROM expenses
                WHERE date=:date AND description=:description 
                AND amount=:amount AND category=:category;
                """
    conn= db_connection()
    data = read_csv(file_path)
    rows = data['Invoice_Data']

    data_result = []
    for row in rows:
        x = conn.run(query,
                 date=row['Date'],
                 description=row['Description'],
                 amount=row['Amount'],
                 category = row['Category']) 
        
        data_result.append(x[0])
    
    return data_result
    