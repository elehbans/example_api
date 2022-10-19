import json
import os

from api.db.models import Contact

def load_sample_data():
    test_utils_dir = os.path.dirname( os.path.realpath(__file__))
    sample_data_file = os.path.join(test_utils_dir, 'sample_data.json')
    with open(sample_data_file) as json_file:
        data = json.load(json_file)
        for contact in data['sample_data']:
            new_contact = Contact(**contact)
            new_contact.save()