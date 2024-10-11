from flask_restx import Resource, Namespace, reqparse, abort
from .api_models import get_project_model
from .utils import read_data, write_data, read_array_data, write_array_data, verify_cognito_token
import boto3
from botocore.exceptions import ClientError
import logging


ns = Namespace('/api/', path="/api/", description="")


parser = reqparse.RequestParser()
parser.add_argument('Authorization', location='headers', required=True, help='Authorization header is required')

required_param = {'Authorization': 'ID Token required'}

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_user_email(args):
    token = args['Authorization']    
    try:
        user_attributes = verify_cognito_token(token)
        owner_email = user_attributes['email']        
        if not owner_email:
            logger.error("No email found in user attributes")
            abort(401, description="Not authorized")
        
        return owner_email
    except Exception as e:
        logger.exception("Error verifying token")
        abort(401, description="Not authorized")


@ns.route("/user")
@ns.doc(params=required_param)
class User(Resource):
    @ns.doc(responses={200: 'Success', 401: 'Authorization is required'})
    def get(self):
        owner_email = get_user_email(parser.parse_args())
        return {'email': owner_email}, 200

@ns.route("/projects")
@ns.doc(params=required_param)
class Projects(Resource):
    @ns.doc(responses={200: 'Success', 401: 'Authorization is required'})
    @ns.marshal_with(get_project_model(), as_list=True)
    def get(self):
        owner_email = get_user_email(parser.parse_args())
        data = read_data()
        user_projects = [proj for proj in data['projects'] if proj["user"][0]['email'] == owner_email]
        return user_projects, 200
    
    @ns.expect(get_project_model())
    @ns.doc(responses={201: 'Created project', 401: 'Authorization is required', 406: 'Missing JSON data', 409: 'Project with the same name and owner already exists'})
    def post(self):
        owner_email = get_user_email(parser.parse_args())

        new_project = ns.payload
        if 'user' not in new_project or 'details' not in new_project or 'email' not in new_project['user'][0] or 'name' not in new_project['details']:
            abort(406, description="Missing JSON data")
        
        # Ensure the email is set to owner_email
        new_project['user'][0]['email'] = owner_email
        
        data = read_data()

        if any(proj['details']['name'] == new_project['details']['name'] and proj['user'][0]['email'] == new_project['user'][0]['email'] for proj in data['projects']):
            abort(409, description="Project with the same name and owner already exists")
        
        data['projects'].append(new_project)
        write_data(data)
        
        # Check if the language is in the array_data, if not add it
        if 'languages' in new_project["architecture"]:
            array_data = read_array_data()
            languages = []
            if 'main' in new_project["architecture"]['languages']:
                languages.append(new_project["architecture"]['languages']['main'])
            if 'others' in new_project["architecture"]['languages']:
                languages.extend(new_project["architecture"]['languages']['others'])
            if 'languages' not in array_data:
                array_data['languages'] = []
            array_data['languages'] = [lang.lower() for lang in array_data['languages']]
            for language in languages:
                language = language.lower()
                if language not in array_data['languages']:
                    array_data['languages'].append(language)
            write_array_data(array_data)
        
        return new_project, 201


@ns.doc(params=required_param,
responses={200: 'Success', 401: 'Authorization is required', 404: 'Project not found.'})
@ns.route("/projects/<string:project_name>")
class ProjectDetail(Resource):
    @ns.marshal_list_with(get_project_model())
    def get(self, project_name):
        owner_email = get_user_email(parser.parse_args())

        data = read_data()
        project = next((proj for proj in data['projects'] if proj["details"]['name'] == project_name and proj["user"][0]['email'] == owner_email), None)
        if not project:
            abort(404, description="Project not found")
        return project, 200

autoCompleteParser = reqparse.RequestParser()
autoCompleteParser.add_argument('type', type=str, required=True, help='type is required')
autoCompleteParser.add_argument('search', type=str, required=True, help='search is required')

@ns.doc(params={'type':'Type of array', 'search':'Search query'}, 
responses={200: 'Success', 400: 'type and search are required', 404: 'No matches found.', 406: 'Invalid type', 411: 'Search query is too long'})
@ns.route("/autocomplete")
class Autocomplete(Resource):
    def get(self):
        owner_email = get_user_email(parser.parse_args())

        args = autoCompleteParser.parse_args()
        search_type = args['type']
        search_query = args['search']

        if not search_type or not search_query:
            abort(400, description="type and search are required")
        
        if search_type not in ['languages', 'IDEs', 'misc']:
            abort(406, description="Invalid type")
        
        if len(search_query) > 16:
            abort(411, description="Search query is too long")
        
        array_data = read_array_data()
        
        if search_type not in array_data:
            abort(406, description=f"Invalid type: {search_type}")
        
        results = [item for item in array_data[search_type] if search_query.lower() in item.lower()]

        if not results:
            abort(404, description="No matches found")
        
        return results, 200