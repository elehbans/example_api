import json
import os
from typing import Dict

from api.db.models import Contact

def load_sample_data():
    example_api_dir = os.path.dirname( os.path.realpath(__name__))
    sample_data_file = os.path.join(example_api_dir, 'tests/utils/sample_data.json')
    json_file = open(sample_data_file)
    data = json.load(json_file)
    json_file.close()
    
    return data

def save_sample_data(data) -> Dict:
    for contact in data['sample_data']:
        new_contact = Contact(**contact)
        new_contact.save()