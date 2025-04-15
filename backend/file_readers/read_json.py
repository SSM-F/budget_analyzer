import json
import logging

def read_json(json_file_path):
    if json_file_path.endswith('json'):
        with open(f'{json_file_path}') as f:
            parsed_json = json.load(f)
            data = [data for data in parsed_json]
            logging.info("Succesfully read JSON file")
            return {'Invoice_Data': data}
    else:
        raise Exception ('Wrong file format or file not found')