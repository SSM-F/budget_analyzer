from backend.file_readers.read_csv import read_csv
from backend.file_readers.read_json import read_json
from backend.db_conn import db_connection, close_conn
import logging
from pprint import pprint


def populate_db(file_path,table_name):
    newly_inserted = []
    conn = None
    data = None
    try: 
        conn=db_connection()

        if file_path.endswith("csv"):
            data = read_csv(file_path)
        if file_path.endswith("json"):
            data = read_json(file_path)

        rows = data['Invoice_Data']
        check_query = f"""
                SELECT 1 FROM {table_name}
                WHERE id=:id AND description=:description
                AND amount=:amount AND category=:category
                AND date=:date
                LIMIT 1;
                """
        insert_query = f'''
                INSERT INTO {table_name}
                (id,date,description,amount,category)
                VALUES (:id,:date,:description,:amount,:category);
                '''
        
        row_count = 0
        for row in rows:
            exists = conn.run(check_query,
                     id=row['id'],
                     date=row['Date'],
                     description=row['Description'],
                     amount=row['Amount'],
                     category = row['Category'])
            if not exists:
                inserted = conn.run(insert_query,
                     id=row['id'],
                     date=row['Date'],
                     description=row['Description'],
                     amount=row['Amount'],
                     category = row['Category'])
                newly_inserted.append(inserted)
            row_count += 1
        logging.info(f"Successfully added {row_count} rows to table {table_name}" )
        query = f"SELECT * FROM {table_name}"
        return conn.run(query)
    except:
        acceptable_files = ['json','csv']
        if file_path is None or not file_path.endswith(tuple(acceptable_files)):
            raise Exception("Wrong file type or path not found")
        
    finally:
        
        if conn is not None:
            close_conn(conn)
        


