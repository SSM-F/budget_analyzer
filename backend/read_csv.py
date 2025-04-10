import csv
import logging


def read_csv(csv_file):
    try:
        with open(f'{csv_file}', newline='') as file:
        
            reader = csv.DictReader(file)
            lines = []
            for line in reader:
                lines.append(line)
            logging.info('CSV file succesfully read')
            return {'Invoice_Data': lines}
    except Exception:
        raise Exception ('File Not Found')  
            
        