from backend.read_csv import read_csv
import pytest
import logging

def test_read_csv_succesfully_reads_file():
    test_file = 'data/example_invoice.csv'
    assert read_csv(test_file) == {'Invoice_Data': 
                                   [{'Date': '2025-03-01', 'Description': 'Starbucks Coffee', 'Amount': '-4.50', 'Category': 'Coffee'}, 
                                   {'Date': '2025-03-02', 'Description': 'Amazon Purchase', 'Amount': '-49.99', 'Category': 'Shopping'}, 
                                   {'Date': '2025-03-03', 'Description': 'Uber Ride', 'Amount': '-15.75', 'Category': 'Transport'}, 
                                   {'Date': '2025-03-05', 'Description': 'Salary', 'Amount': '+2500.00', 'Category': 'Income'},
                                   {'Date': '2025-03-06', 'Description': 'Netflix Subscription', 'Amount': '-12.99', 'Category': 'Entertainment'}, 
                                   {'Date': '2025-03-07', 'Description': 'Grocery Store', 'Amount': '-76.20', 'Category': 'Groceries'}, 
                                   {'Date': '2025-03-09', 'Description': 'Spotify', 'Amount': '-9.99', 'Category': 'Entertainment'},
                                   {'Date': '2025-03-10', 'Description': 'Electricity Bill', 'Amount': '-89.30', 'Category': 'Utilities'}, 
                                   {'Date': '2025-03-12', 'Description': 'Gas Station', 'Amount': '-40.00', 'Category': 'Transport'}, 
                                   {'Date': '2025-03-15', 'Description': 'Dinner at Italian Bistro', 'Amount': '-67.00', 'Category': 'Food'}]
                                    }

def test_exception():
    test_file = 'not_a_file'
    with pytest.raises(Exception) as e:
        read_csv(test_file)
    assert 'File Not Found' in str(e)

def test_logging_info(caplog):
    test_file = 'data/example_invoice.csv'
    with caplog.at_level(logging.INFO):
        read_csv(test_file)
    assert 'CSV file succesfully read' in caplog.text

