from flask_restx import Resource, Namespace, reqparse, abort
from .api_models import get_project_model
from .utils import read_data, write_data, read_array_data, write_array_data, verify_cognito_token, read_client_keys
import boto3
from botocore.exceptions import ClientError
import logging
import os
import requests


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

cognito_settings = read_client_keys()
COGNITO_CLIENT_ID = cognito_settings["AWS_COGNITO_CLIENT_ID"]
COGNITO_CLIENT_SECRET = cognito_settings["AWS_COGNITO_CLIENT_SECRET"]
REDIRECT_URI = cognito_settings["REDIRECT_URI"]

verifyParser = reqparse.RequestParser()
verifyParser.add_argument('code', location='args', required=True, help='Authorization code is required')
@ns.route("/verify")
class VerifyToken(Resource):
    # Route for handling the callback from Cognito
    def get(self):
        # Get the code from the query params
        code = verifyParser.parse_args()['code']
        if not code:
            logger.error("Authorization code not found")
            return {"error": "Authorization code not found"}, 400

        # Exchange the code for tokens
        token_response = self.exchange_code_for_tokens(code)

        if 'id_token' not in token_response:
            logger.error("Failed to retrieve ID Token")
            return {"error": "Failed to retrieve ID Token"}, 400

        # Return the ID token to the client
        id_token = token_response['id_token']
        return {"id_token": id_token}, 200


    def exchange_code_for_tokens(self, code):
        token_url = f"https://keh-tech-audit-tool.auth.eu-west-2.amazoncognito.com/oauth2/token"
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': f'{REDIRECT_URI}/api/verify'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        auth = (COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET)

        response = requests.post(token_url, data=payload, headers=headers, auth=auth)
    
        if response.status_code != 200:
            if response.json()['error'] == 'invalid_grant':
                logger.error("Invalid authorization code")
                return {"error": "Invalid authorization code"}, 404
            logger.error(f"Error: {response.status_code}, {response.text}")
            raise Exception(f"Error: {response.status_code}, {response.text}")

        # Return the parsed JSON response
        return response.json()