### DEPENDENCIES ###
from flask import request, abort, jsonify
from pydantic import ValidationError
from redis_om import NotFoundError

from api import create_app
from api.db import init_db
from api.db.models import Contact
from api.utils import create_call_list

### SETUP ###
app = create_app()
init_db()

### ERROR HANDLING ###
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error='Invalid Route'), 404

@app.errorhandler(403)
def prohibited_request_type(e):
    return jsonify(error='Prohibited Request Type'), 403

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=e), 400


### ENDPOINTS ###
@app.route('/contacts', methods = ['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        try:
            new_contact = Contact(**request.json)
        except ValidationError as e:
            abort(400, description=e)
        
        new_contact.save()

        return new_contact.pk
    elif request.method == 'GET':
        all_contacts = Contact.find().all()
        return all_contacts
    else:
        abort(403)

@app.route('/contact/<user_id>', methods = ['GET', 'PUT', 'DELETE'])
def single_contact(user_id):
    if request.method in ['GET', 'PUT', 'DELETE']:
        try:
            contact = Contact.get(str(user_id))
        except NotFoundError:
            abort(400, "User Id Not Found")

        if request.method == 'GET':
            return contact.json
        elif request.method == 'PUT':
            new_values = Contact.parse_obj(**request.json)
            contact.update(new_values)
            return contact.pk
        elif request.method == 'DELETE':
            contact.delete()
            return user_id
    else:
        abort(403)

@app.route('/contacts/call-list', methods = ['GET'])
def call_list():
    if request.method == 'GET':
        sorted_home_phone_only_contacts = Contact.find().sort_by("lastname", "firstname").all()
        call_list = create_call_list(sorted_home_phone_only_contacts)
        return call_list
    else:
        abort(403)
        