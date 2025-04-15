from backend.read_csv import read_csv
from backend.db_conn import db_connection, close_conn
import logging
from pprint import pprint
from pg8000.exceptions import DatabaseError
from fastapi import HTTPException
def populate_db(csv_file_path,table_name):
    newly_inserted = []
    conn = None
    if csv_file_path.endswith("csv"):
    
        try: 

            conn=db_connection()
            data = read_csv(csv_file_path)
            rows = data['Invoice_Data']
            check_query = f"""
                    SELECT 1 FROM {table_name}
                    WHERE date=:date AND description=:description
                    AND amount=:amount AND category=:category
                    LIMIT 1;
                    """
            insert_query = f'''
                    INSERT INTO {table_name}
                    (date,description,amount,category)
                    VALUES (:date,:description,:amount,:category);

                    '''
            row_count = 0
            
            for row in rows:
                exists = conn.run(check_query,
                         date=row['Date'],
                         description=row['Description'],
                         amount=row['Amount'],
                         category = row['Category'])
                if not exists:
                    inserted = conn.run(insert_query,
                         date=row['Date'],
                         description=row['Description'],
                         amount=row['Amount'],
                         category = row['Category'])
                    
                    newly_inserted.append(inserted)
                
                

                row_count += 1
            logging.info(f"Successfully added {row_count} rows to table {table_name}" )
            query = f"SELECT * FROM {table_name}"
            return conn.run(query)

        finally:
            if conn is not None:
                close_conn(conn)
    else:
        raise Exception('File Not Found')


