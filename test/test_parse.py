from backend.parse import populate_db
import pytest
from backend.db_conn import db_connection, close_conn
from unittest.mock import MagicMock

@pytest.fixture
def mock_db_conn(mocker):
    mock_conn = MagicMock()
    mock_conn.run = MagicMock()
    mock_conn.fetchall = MagicMock(return_value=[('2025-03-01','Starbucks Coffee',-4.50,'Coffee')])
    mocker.patch('backend.db_conn.db_connection',return_value = mock_conn())
    return mock_conn



def test_populate_db_succesfully_populate_table(mock_db_conn,mocker):
    test_file = 'data/example_invoice.csv'
    test_table_name = 'expenses'
    
    mock_data = {'Invoice_Data':[{
        'Date': '2025-03-01',
        'Description': 'Starbucks Coffee',
        'Amount': -4.50,
        'Category': 'Coffee'
    }]}
    mocker.patch('backend.read_csv.read_csv',return_value = mock_data)
    populate_db(file=test_file,table_name=test_table_name) 
    mock_db_conn.run.assert_called_with(
        "INSERT INTO expenses (date,description,amount,category) " \
        "VALUES (:date,:description,:amount,:category)",
        date = '2025-03-01',
        description='Starbucks Coffee',
        amount= -4.50,
        category= 'Coffee'
    )