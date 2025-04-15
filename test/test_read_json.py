from backend.file_readers.read_json import read_json
import pytest
import logging

def test_read_json_reads_and_parse_file():
    test_input = 'data/invoice_holidays.json'
    response = read_json(test_input)
    assert response['Invoice_Data'][0] == {
                                          'amount': -350.0,
                                          'category': 'Holiday',
                                          'date': '2025-07-15',
                                          'description': 'Airbnb - Barcelona trip',
                                           }
    
def test_read_json_raise_exception_if_wrong_file_format_passed():
    test_input = 'data/example_invoice.csv'

    with pytest.raises(Exception) as e:
        read_json(test_input)
    assert 'Wrong file format or file not found' in str(e)

def test_read_json_loggs_succesfull_message(caplog):
    test_input = 'data/invoice_holidays.json'
    with caplog.at_level(logging.INFO):
        read_json(test_input)
    assert "Succesfully read JSON file" in caplog.text


    
