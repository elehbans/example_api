from pydantic import BaseModel

class Name(BaseModel):
    first: str
    middle: str
    last: str

class ContactListEntry(BaseModel):
    name: Name
    phone: str
    