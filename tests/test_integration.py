import os
import pytest

from .utils.load_sample_data import load_sample_data
from api import create_app
from api.db import init_db, flush_db

@pytest.fixture(scope="session", autouse=True)
def client():
    app = create_app()
    app.config['TESTING'] = True # verbose error logging

    with app.test_client() as client:
        with app.app_context():
            os.environ['RUNNING_LOCALLY'] = 'True'
            init_db()
            load_sample_data()
        yield client
    
    flush_db()

# BAD:
# Bad url
# bad request type
# nonexistent id
# malformed json

# GOOD:
# GET contacts - list all contacts
def test_list_all_contacts(client):
    rv = client.get('/contacts')
    print(rv)


# POST contacts - create new contact
# PUT contact/id - update a contact
# GET contacts/id - get a specific contact
# DELETE contacts/id - delete a contact
# GET contacts/call-list
