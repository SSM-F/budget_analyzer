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
        table = 'expenses'
        response = test_client.get(f'/api/summary/{table}')
        assert response.status_code == 200

    def test_server_returns_expenses_info(self,reset_db,test_client):
        table = 'expenses'
        response = test_client.get(f'/api/summary/{table}')
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
                f"/api/upload?table_name={test_table_name}",
                files={'file_path': (test_invoice, f, 'text/csv')})
           
        assert response.status_code == 201
        


    def test_put_new_expenses_return_new_added_invoice(self,reset_db,test_client):
        test_invoice = 'data/invoice_today.csv'
        test_table_name = 'expenses'
        with open(test_invoice,'rb') as f:
            response = test_client.put(f"/api/upload?table_name={test_table_name}",
                                       files={'file_path':(test_invoice,f,"text/csv")})
           
        response_decoded = response.json()
        
        expected_items= {'New_invoice_added': 
                         [{'amount': -109.99,
                        'category': 'Shopping',
                        'date': '2025-03-18',
                        'description': 'Waterstone',
                        'id': 14},
                       {'amount': -302.78,
                        'category': 'Shopping',
                        'date': '2024-02-19',
                        'description': 'IKEA',
                        'id': 17}]}
    
        assert response_decoded == expected_items

    def test_put_endpoint_works_with_json_files(self,reset_db,test_client):
        test_invoice = 'data/invoice_holidays.json'
        test_table = 'expenses'
        with open(test_invoice,'rb') as f:
            response = test_client.put(f'/api/upload?table_name={test_table}',
                                       files={'file_path':(test_invoice,f,'text/json')})
        response_decoded = response.json()
        expected = {'New_invoice_added': [
                       {'amount': -350.0,
                        'category': 'Holiday',
                        'date': '2025-07-15',
                        'description': 'Airbnb - Barcelona trip',
                        'id': 101},
                       {'amount': -180.75,
                        'category': 'Holiday',
                        'date': '2025-07-16',
                        'description': 'Flight to Barcelona',
                        'id': 102},
                       {'amount': -25.0,
                        'category': 'Holiday',
                        'date': '2025-07-18',
                        'description': 'Sagrada Familia tickets',
                        'id': 103
                        }]}
        assert expected == response_decoded

class TestDelete:
    def test_endpoint_delete_status_code(self,reset_db,test_client):
        test_id= 1
        test_table = 'expenses'
        response = test_client.delete(f'/api/delete/{test_table}/{test_id}')
        assert response.status_code == 200

    def test_endpoint_delete_remove_item_from_database(self,reset_db,test_client):
        test_id= 101
        test_table = 'expenses'
        test_invoice = 'data/invoice_holidays.json'
        with open(test_invoice,'rb') as f:
            response_put = test_client.put(f'/api/upload?table_name={test_table}',
                                           files={'file_path':(test_invoice,f,'text/json')})
        response_put_decoded = response_put.json()['New_invoice_added']
        response = test_client.delete(f'/api/delete/{test_table}/{test_id}')
        response_decoded = response.json()
        assert response_decoded not in response_put_decoded
        assert response_decoded == {'Invoice_deleted': [{'amount': -350.0,
                                                        'category': 'Holiday',
                                                        'date': '2025-07-15',
                                                        'description': 'Airbnb - Barcelona trip',
                                                        'id': 101},]}


    

        
    


