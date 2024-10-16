"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask  # , request
from flask_restx import Resource, Api  # Namespace, fields
from flask_cors import CORS

import werkzeug.exceptions as wz
import data.people as ppl

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
    """
    This class handles creating, reading,
    updating, and deleting our journal people.
    """
    def get(self):
        """
        Retrieve the journal people
        """
        return ppl.get_people()


# People/User Delete Class
# will delete valid users, and return 404 User Not Found for invalid users
@api.route(f'{PEOPLE_EP}/<_id>')
class PersonDelete(Resource):
    @api.response(HTTPStatus.OK, 'Sucess.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')  
    def delete(self, _id):
        ret = ppl.delete_person(_id)
        if ret is not None:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such person: {_id}')


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
})