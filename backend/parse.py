from backend.read_csv import read_csv
from backend.db_conn import db_connection, close_conn
import logging

def populate_db(csv_file_path,table_name):
    conn = None
    try: 
        if csv_file_path is None:
            raise Exception('File Not Found')
        
        conn=db_connection()
        data = read_csv(csv_file_path)
        rows = data['Invoice_Data']
        query = f'''
                INSERT INTO {table_name}
                (date,description,amount,category)
                VALUES (:date,:description,:amount,:category)
                
                '''
        row_count = 0
        for row in rows:
            conn.run(query,
                     date=row['Date'],
                     description=row['Description'],
                     amount=row['Amount'],
                     category = row['Category'])
            row_count += 1
        print(row_count)
        logging.info(f"Successfully added {row_count} rows to table {table_name}" )
        return conn.run(f'SELECT * FROM {table_name}')
        
    finally:
        if conn is not None:
            close_conn(conn)
    

    