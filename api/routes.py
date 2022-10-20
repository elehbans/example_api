### DEPENDENCIES ###
from flask import request, abort, jsonify, Blueprint, Flask
from pydantic import ValidationError
from redis_om import NotFoundError, get_redis_connection
from werkzeug.exceptions import BadRequest

from api.db import init_db
from api.db.models import Contact
from api.utils import create_call_list

blueprint = Blueprint('example_api', __name__)

### ERROR HANDLING ###
@blueprint.errorhandler(404)
def resource_not_found(e):
    return jsonify(error='Invalid Route'), 404

@blueprint.errorhandler(403)
def prohibited_request_type(e):
    return jsonify(error='Prohibited Request Type'), 403

@blueprint.errorhandler(400)
def bad_request(e: BadRequest):
    return e


### ENDPOINTS ###
@blueprint.route('/contacts', methods = ['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        try:
            new_contact = Contact(**request.json)
        except ValidationError as e:
            abort(400, description=e)
        
        new_contact.save()

        return jsonify(new_contact.pk), 200
    elif request.method == 'GET':
        try:
            all_contacts = Contact.find('*')
            return jsonify(all_contacts), 200
        except:
            return jsonify([]), 200
    else:
        abort(403)

@blueprint.route('/contact/<user_id>', methods = ['GET', 'PUT', 'DELETE'])
def single_contact(user_id):
    if request.method in ['GET', 'PUT', 'DELETE']:
        try:
            contact = Contact.get(str(user_id))
        except NotFoundError:
            abort(400, description="User Id Not Found")

        if request.method == 'GET':
            return contact.json(), 200
        elif request.method == 'PUT':
            new_values = Contact.parse_obj(**request.json)
            contact.update(new_values)
            return jsonify(contact.pk), 200
        elif request.method == 'DELETE':
            contact.delete(user_id)
            return jsonify(user_id), 200
    else:
        abort(403)

@blueprint.route('/contacts/call-list', methods = ['GET'])
def call_list():
    if request.method == 'GET':
        # ensure return format is the expected minimal representation
        r = get_redis_connection() 
        home_phone_contacts = r.ft().search('@type:(home)').docs
        call_list = create_call_list(home_phone_contacts)
        return jsonify(call_list), 200
    else:
        abort(403)

def create_app(config='dev'):
    app = Flask(__name__) 
    app.register_blueprint(blueprint) 
    return app

if __name__ == "__main__":
    create_app()
    init_db()
    