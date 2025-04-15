import csv
import logging
from typing import Union
from fastapi import UploadFile,File


def read_csv(csv_file: Union[str, UploadFile]):
    try:
        if isinstance(csv_file,str):
            with open(f'{csv_file}', newline='') as file:
                reader = csv.DictReader(file)
                lines = [line for line in reader]
                    
        else:
            csv_file.file.seek(0) 
            content = csv_file.file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(content)
            lines = [line for line in reader]

        
        logging.info('CSV file succesfully read')
        return {'Invoice_Data': lines}
    except Exception:
        raise Exception ('File Not Found')  
            
        