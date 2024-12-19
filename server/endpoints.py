"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields
from flask_cors import CORS

import werkzeug.exceptions as wz
import data.people as ppl
import data.text as txt
import data.manuscripts.fields as mflds

app = Flask(__name__)
CORS(app)
api = Api(app)

ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
TITLE_EP = '/title'
TITLE_RESP = 'Title'
TITLE = 'KDNC Journal'
RETURN = 'return'

EDITOR_RESP = 'Editor'
EDITOR = 'dg3729@nyu.edu'
DATE_RESP = 'Date'
DATE = '2024-10-09'
PUBLISHER = 'not sure'
PUBLISHER_RESP = 'Publisher'
PEOPLE_EP = '/people'
MESSAGE = 'Message'
TEXT_EP = '/text'
RETURN = 'Return'
MANUSCRIPT_FIELDS_EP = '/manuscripts/fields'


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route(ENDPOINT_EP)
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a sorted list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(TITLE_EP)
class JournalTitle(Resource):
    """
    This class handles creating, reading,
 updating, and deleting our journal title.
    """
    def get(self):
        """
        Retrieve the journal title
        """
        return {
            TITLE_RESP: TITLE,
            EDITOR_RESP: EDITOR,
            DATE_RESP: DATE,
            PUBLISHER_RESP: PUBLISHER,
        }


@api.route(PEOPLE_EP)
class People(Resource):
    def get(self):
        """
        Retrieve all journal people
        """
        try:
            print("Fetching all people from the database...")
            people = ppl.get_people()
            print(f"Fetched people: {people}")
            return people, HTTPStatus.OK
        except Exception as e:
            print(f"Error in /people endpoint: {e}")
            return {
                "error": "Internal Server Error"
            }, HTTPStatus.INTERNAL_SERVER_ERROR


# People/User Delete Class
# will delete valid users, and return 404 User Not Focund for invalid users
@api.route(f'{PEOPLE_EP}/<email>')
class Person(Resource):
    """
    This class handles creating, reading, updating
    and deleting journal people.
    """
    def get(self, email):
        """
        Retrieve a journal person.
        """
        person = ppl.get_one(email)
        if person:
            return person
        else:
            raise wz.NotFound(f'No such record: {email}')

    @api.response(HTTPStatus.OK, 'Sucess.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
    def delete(self, email):
        """
        Delete a person
        """
        ret = ppl.delete_person(email)
        if ret is not None:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such person: {email}')


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.String,
})


@api.route(f'{PEOPLE_EP}/create')
class PeopleCreate(Resource):
    """
    Add a person to the journal db.
    """

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Accesptable')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self):
        """
        Add a person.
        """

        try:
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            email = request.json.get(ppl.EMAIL)
            role = request.json.get(ppl.ROLES)
            ret = ppl.create_person(name, affiliation, email, role)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person added!',
            RETURN: ret,
        }


TEXT_MODEL = api.model(
    'AddNewTextEntry',
    {
        txt.KEY: fields.String(
            required=True,
            description='Unique identifier'
        ),
        txt.TITLE: fields.String(
            required=True,
            description='Title'
        ),
        txt.TEXT: fields.String(
            required=True,
            description='Content'
        ),
        txt.EMAIL: fields.String(
            required=True,
            description='Email'
        ),
    }
)


@api.route(f'{TEXT_EP}/read')
class ReadTexts(Resource):
    def get(self):
        """
        Retrieve all text entries
        """
        try:
            texts = txt.read()
            return texts, HTTPStatus.OK
        except Exception as e:
            return {'error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route(f'{TEXT_EP}/<string:key>')
class GetText(Resource):
    def get(self, key):
        """
        Retrieve text entry by key
        """
        try:
            text_entry = txt.get_one(key)
            if not text_entry:
                return {
                    'error': f'No entry found for key: {key}'
                }, HTTPStatus.NOT_FOUND
            return text_entry, HTTPStatus.OK
        except Exception as e:
            return {'error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route(f'{TEXT_EP}/create')
class CreateText(Resource):
    @api.expect(TEXT_MODEL)
    def put(self):
        """
        Create a new text entry
        """
        try:
            data = request.json
            key = data.get(txt.KEY)
            title = data.get(txt.TITLE)
            text = data.get(txt.TEXT)
            email = data.get(txt.EMAIL)
            new_entry = txt.create(key, title, text, email)
            return {
                'message': 'Text entry created successfully',
                'entry': new_entry
            }, HTTPStatus.CREATED
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route(f'{TEXT_EP}/update/<string:key>')
class UpdateText(Resource):
    @api.expect(TEXT_MODEL)
    def patch(self, key):
        """
        Update an existing text entry
        """
        try:
            data = request.json
            title = data.get(txt.TITLE)
            text = data.get(txt.TEXT)
            email = data.get(txt.EMAIL)
            updated_entry = txt.update(
                key,
                title=title,
                text=text,
                email=email
            )
            return {
                'message': 'Text entry updated successfully',
                'entry': updated_entry
            }, HTTPStatus.OK
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.NOT_FOUND
        except Exception as e:
            return {'error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route(f'{TEXT_EP}/delete/<string:key>')
class DeleteText(Resource):
    def delete(self, key):
        """
        Delete a text entry
        """
        try:
            deleted_key = txt.delete(key)
            return {
                'message': (
                    f'Text entry with key "{deleted_key}" '
                    'deleted successfully'
                )
            }, HTTPStatus.OK
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.NOT_FOUND
        except Exception as e:
            return {'error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


MASTHEAD = 'Masthead'


@api.route(f'{PEOPLE_EP}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {MASTHEAD: ppl.get_masthead()}


FIELDS_FLDS = api.model('AddNewFieldEntry', {
    'field_name': fields.String(
        required=True,
        description='Name'
    ),
    'display_name': fields.String(
        required=True,
        description='Display Name'
    ),
})


@api.route(MANUSCRIPT_FIELDS_EP)
class ManuscriptFields(Resource):
    def get(self):
        """
        Retrieve all fields.
        """
        return mflds.get_flds()

    @api.expect(FIELDS_FLDS)
    def post(self):
        """
        Add a new field.
        """
        data = request.json
        field_name = data.get('field_name')
        display_name = data.get('display_name')
        if not field_name or not display_name:
            return {
                'error': 'Both field_name and display_name are required.'
            }, HTTPStatus.BAD_REQUEST
        if mflds.add_field(field_name, display_name):
            return {
                'message': f'Field "{field_name}" added successfully.'
            }, HTTPStatus.CREATED
        else:
            return {
                'error': 'Field already exists.'
            }, HTTPStatus.BAD_REQUEST


@api.route(f'{MANUSCRIPT_FIELDS_EP}/<field_name>')
class ManuscriptField(Resource):
    """
    Operations on a specific manuscript field.
    """
    @api.expect(FIELDS_FLDS)
    def patch(self, field_name):
        """
        Update a field's display name.
        """
        try:
            data = request.json
            new_display_name = data.get('display_name')

            if not new_display_name:
                return {
                    'error': 'A new display_name is required.'
                }, HTTPStatus.BAD_REQUEST

            if mflds.update_field(field_name, new_display_name):
                return {
                    'message': f'Field "{field_name}" updated successfully.',
                    'field': {
                        'field_name': field_name,
                        'display_name': new_display_name
                    }
                }, HTTPStatus.OK

            return {
                'error': f'Field "{field_name}" not found.'
            }, HTTPStatus.NOT_FOUND
        except Exception as e:
            return {'error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

    def delete(self, field_name):
        """
        Delete a field.
        """
        if mflds.del_field(field_name):
            return {
                'message': f'Field "{field_name}" deleted successfully.'
            }
        else:
            return {
                'error': f'Field "{field_name}" not found.'
            }, HTTPStatus.NOT_FOUND
