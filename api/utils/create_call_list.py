import json
from typing import List

from .types import ContactListEntry

def create_call_list(contacts: List[ContactListEntry]) -> List[ContactListEntry]:
    contacts_dict = json.loads(contacts)
    sorted_contacts = sorted(contacts_dict, key=lambda k: (k['name.last'].lower(), k['name.first'].lower()))
    return sorted_contacts
