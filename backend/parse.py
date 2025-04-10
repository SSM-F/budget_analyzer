from backend.read_csv import read_csv
from backend.db_conn import db_connection, close_conn

def populate_db(file,table_name):
    conn = None
    try: 
        conn=db_connection()
        data = read_csv(file)
        rows = data['Invoice_Data']
        query = f'''
                INSERT INTO {table_name}
                (date,description,amount,category)
                VALUES (:date,:description,:amount,:category)
                '''
        for row in rows:
            conn.run(query,
                     date=row['Date'],
                     description=row['Description'],
                     amount=row['Amount'],
                     category = row['Category'])
        conn.run(f'SELECT * FROM {table_name}')
    finally:
        if conn is not None:
            close_conn(conn)

    