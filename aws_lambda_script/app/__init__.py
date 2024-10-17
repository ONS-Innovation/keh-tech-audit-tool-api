from flask import Flask

from .extensions import api
from .resources import ns

def create_app():
    app = Flask(__name__)

    authorizations = {
    'ID Token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter your id token in the format **&lt;id_token&gt;**'
    }
}

    api.__init__(app, doc="/",
    title="KEH Tech Audit Tool API",
    version="0.1.2",
    authorizations=authorizations,
    security='ID Token',
    description="An API that saves and accesses data from an S3 bucket in AWS saved and queried as JSON. Each route with /api/ must use an Authorization header with a valid Cognito ID token.")
    api.add_namespace(ns)

    return app