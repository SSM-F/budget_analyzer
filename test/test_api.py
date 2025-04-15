from backend.main import app
from backend.db_conn import close_conn,db_connection
from fastapi.testclient import TestClient
import pytest
from pprint import pprint
import json

@pytest.fixture(autouse=True)
def reset_db():
    conn= db_connection()
    try:
         conn.run(f"""
                 TRUNCATE expenses;
                """)
                
         yield conn
    finally:
        close_conn(conn)

@pytest.fixture(autouse=True)
def test_client():
    return TestClient(app)


class TestGet:
    def test_server_runs(self,reset_db,test_client):
        response = test_client.get('/api/expenses')
        assert response.status_code == 200

    def test_server_returns_expenses_info(self,reset_db,test_client):
        response = test_client.get('/api/expenses')
        response_decoded = response.json()['Detailed_expenses']
        for dic in response_decoded:
            assert 'amount' in dic
            assert 'category' in dic
            assert 'created_at' in dic
            assert 'date' in dic
            assert 'description' in dic
            assert 'expense_id' in dic
            assert response_decoded[0] == {
                                        'amount': -4.5,
                                        'category': 'Coffee',
                                        'created_at': '2025-04-11T21:41:42.111556',
                                        'date': '2025-03-01',
                                        'description': 'Starbucks Coffee',
                                        'expense_id': 621}
    
class TestPut:

    def test_put_new_expense_status_code_201(self,reset_db,test_client):
        test_invoice = 'data/invoice01.csv'
        test_table_name = 'expenses'
        with open(test_invoice, 'rb') as f:
            response = test_client.put(
                f"/api/expenses/upload?table_name={test_table_name}",
                files={'file_path': (test_invoice, f, 'text/csv')})
           
        assert response.status_code == 201
        


    def test_put_new_expenses_return_new_added_invoice(self,reset_db,test_client):
        test_invoice = 'data/invoice_today.csv'
        test_table_name = 'expenses'
        with open(test_invoice,'rb') as f:
            response = test_client.put(f"/api/expenses/upload?table_name={test_table_name}",
                                       files={'file_path':(test_invoice,f,"text/csv")})
           
        response_decoded = response.json()
        
        expected_items= {'New_invoice_added': 
                         [{'amount': -109.99,
                        'category': 'Shopping',
                        'date': '2025-03-18',
                        'description': 'Waterstone'},
                       {'amount': -302.78,
                        'category': 'Shopping',
                        'date': '2024-02-19',
                        'description': 'IKEA'}]}
    
        assert response_decoded == expected_items

    def test_put_endpoint_works_with_json_files(self,reset_db,test_client):
        test_invoice = 'data/invoice_holidays.json'
        test_table = 'expenses'
        with open(test_invoice,'rb') as f:
            response = test_client.put(f'/api/expenses/upload?table_name={test_table}',
                                       files={'file_path':(test_invoice,f,'text/json')})
        response_decoded = response.json()
        expected = {'New_invoice_added': [
                       {'amount': -350.0,
                        'category': 'Holiday',
                        'date': '2025-07-15',
                        'description': 'Airbnb - Barcelona trip'},
                       {'amount': -180.75,
                        'category': 'Holiday',
                        'date': '2025-07-16',
                        'description': 'Flight to Barcelona'},
                       {'amount': -25.0,
                        'category': 'Holiday',
                        'date': '2025-07-18',
                        'description': 'Sagrada Familia tickets'}]}
        assert expected == response_decoded

    

        
    


