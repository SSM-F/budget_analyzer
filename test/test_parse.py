from backend.parse import populate_db
import pytest
from backend.db_conn import db_connection, close_conn
from unittest.mock import MagicMock
from pprint import pprint
from backend.helper import formated_data
import datetime
import logging
from unittest.mock import patch

@pytest.fixture()
def clean_table():
    conn= db_connection()
    try:
         conn.run(f"""
                 TRUNCATE expenses;
                """)
         
         yield conn
    finally:
        close_conn(conn)
         

def test_populate_db_succesfully_populate_table(clean_table):
    test_file = 'data/example_invoice.csv'
    test_table_name = 'expenses'

    response = populate_db(csv_file_path=test_file, table_name=test_table_name)
    
    
    assert 'Starbucks Coffee' in response[0]
    assert -4.50 in response[0]
    assert 'Coffee' in response[0]
    assert datetime.date(2025, 3, 1) in response[0]
    
    assert len(response) == 10
    
    

def test_populate_db_contain_all_columns(clean_table):
    test_file = 'data/example_invoice.csv'
    test_table_name = 'expenses'
    populate_db(csv_file_path=test_file, table_name=test_table_name)
   
    query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{test_table_name}'"
    columns_result = clean_table.run(query)
   
    assert (['date'] in col for col in columns_result)
    assert (['description'] in col for col in columns_result)
    assert (['amount'] in col for col in columns_result)
    assert (['category'] in col for col in columns_result)

def test_parse_db_reads_all_content_of_file_and_adds_it_to_db(clean_table):
    test_file='data/invoice_today.csv'
    test_table= 'expenses'
    response = populate_db(csv_file_path=test_file, table_name=test_table)
    rows = clean_table.run(f"SELECT * FROM {test_table}")
    assert response == rows
    assert len(response) == 2
    

def test_populate_db_raise_exception():
    test_table_name = 'expenses'
    with pytest.raises(Exception) as e:
        populate_db(csv_file_path='',table_name=test_table_name)
    assert 'File Not Found' in str(e)
   
    

@patch('backend.parse.db_connection') 
@patch('backend.parse.close_conn')  
def test_populate_db_logging_info(mock_close, mock_db_conn, caplog):
    mock_conn = MagicMock()
    mock_conn.run = MagicMock()  
    mock_db_conn.return_value = mock_conn 

    test_file = 'data/example_invoice.csv'
    test_table_name = 'expenses'

    with caplog.at_level(logging.INFO):
        populate_db(csv_file_path=test_file, table_name=test_table_name)

    assert "Successfully added 10 rows to table expenses" in caplog.text
   
    mock_close.assert_called_once_with(mock_conn)
    mock_conn.run.assert_called() 