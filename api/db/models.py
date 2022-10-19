import os
from pydantic import EmailStr
from redis_om import EmbeddedJsonModel, JsonModel, Field, get_redis_connection
from typing import List

from api.config import Config

# Managing the redis connection within the default docker bridge network
# is a bit complicated. The hostname must be the one given in the docker-compose.yml file.
# This connection config is passed as meta-data when Migrator().run() is called.
# Connection docs: https://github.com/redis/redis-om-python/blob/bc2199f2d4a54062414b6cfc7b2eaccd980716be/docs/connections.md
print(os.environ.get('RUNNING_LOCALLY'))
if os.environ.get('RUNNING_LOCALLY') == 'True':
    hostname = 'localhost'
else:
    hostname = Config.REDIS_SERVICE_NAME

redis_meta = get_redis_connection(host=hostname, port=Config.REDIS_PORT)

class Name(EmbeddedJsonModel):
    first: str = Field(index=True, full_text_search=True),
    middle: str
    last: str = Field(index=True, full_text_search=True)

class Address(EmbeddedJsonModel):
    street: str
    city: str
    state: str
    zip: str

class PhoneNumber(EmbeddedJsonModel):
    number: str
    type: str = Field(index=True)

class Contact(JsonModel):
    name: Name
    address: Address
    phone: List[PhoneNumber]
    email: EmailStr

    class Meta:
        database = redis_meta