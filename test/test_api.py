from backend.main import app
from backend.db_conn import close_conn,db_connection
from fastapi.testclient import TestClient
import pytest
from pprint import pprint
import json

@pytest.fixture(autouse=True)
def reset_db():
    test_db = db_connection()
    yield test_db
    close_conn(test_db)

@pytest.fixture(autouse=True)
def test_client():
    return TestClient(app)

def test_server_runs(reset_db,test_client):
    response = test_client.get('/api/expenses')
    assert response.status_code == 200

def test_server_returns_expenses_info(reset_db,test_client):
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
