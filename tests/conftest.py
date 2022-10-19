import os
import pytest

from .utils.data_management import load_sample_data, save_sample_data
from api.routes import create_app
from api.db import init_db, flush_db

# Avoiding autouse=True for transparency of dependencies
@pytest.fixture(scope="module")
def client():
    app = create_app()
    app.config['TESTING'] = True # verbose error logging

    with app.test_client() as client:
        with app.app_context():
            yield client
    
    flush_db()

@pytest.fixture(scope="module")
def input_data():
    os.environ['RUNNING_LOCALLY'] = 'True'
    init_db()
    sample_data = load_sample_data()
    save_sample_data(sample_data)


@pytest.fixture(scope="module")
def contact():
    sample_data = load_sample_data()
    contact = sample_data['sample_data'][0]
    contact['name']['first'] = 'Joseph'
    return contact
