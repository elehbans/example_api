from flask.testing import FlaskClient
import json
from typing import Dict

from api.db.models import Contact

APPLICATION_JSON = 'application/json'
CONTACTS_URL = '/contacts'
CONTACT_URL = '/contact'

# TODO: 
# Failure Modes
# Bad url
# bad request type
# nonexistent id
# malformed json

# Success Modes
def test_list_all_contacts(client: FlaskClient, input_data):
    rv = client.get(CONTACTS_URL)
    json_data = rv.get_json()
    print(json_data)

def test_add_contact(client: FlaskClient, contact: Dict):
    rv = client.post(CONTACTS_URL, data=contact, content_type=APPLICATION_JSON)

def test_update_contact(client: FlaskClient, contact):
    new_contact = Contact(**contact)
    new_contact.name.first = 'Arborist'
    new_contact.save()
    new_contact.name.first = 'not-an-arborist'

    rv = client.put(f'{CONTACT_URL}/{new_contact.pk}', data=json.loads(new_contact.json()), content_type=APPLICATION_JSON)
    # assert that pk is returned?

def test_get_specific_contact(client: FlaskClient, contact: Dict):
    new_contact = Contact(**contact)
    new_contact.name.first = 'Jerry'
    new_contact.save()
    rv = client.get(f'{CONTACT_URL}/{new_contact.pk}')

    # assert rv has 'Jerry' in name

def test_delete_contact(client: FlaskClient, contact: Dict):
    new_contact = Contact(**contact)
    new_contact.name.first = 'Zeus'
    new_contact.save()
    rv = client.delete(f'{CONTACT_URL}/{new_contact.pk}')

    # assert rv is pk

def test_get_call_list(client: FlaskClient):
    rv = client.get(f'{CONTACTS_URL}/call-list')

    # assert in order by creating compound key, copying, sorting and checking if equal
