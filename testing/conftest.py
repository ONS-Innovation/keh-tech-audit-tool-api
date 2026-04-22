import pytest
from flask import Flask
from flask_restx import Api
import sys
import os
import json
from unittest.mock import MagicMock, patch

# Add the app directory to the path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../aws_lambda_script"))
)

# Local test defaults so app imports do not depend on real cloud credentials.
os.environ.setdefault("TECH_AUDIT_SECRET_MANAGER", "local/test/secret")
os.environ.setdefault("AZURE_SECRET_NAME", "local/test/azure")
os.environ.setdefault("AWS_DEFAULT_REGION", "eu-west-2")
os.environ.setdefault("MOCK_TOKEN", "local-test-token")
os.environ.setdefault("REDIRECT_URI", "http://localhost:3000/callback")
os.environ.setdefault(
    "AWS_COGNITO_TOKEN_URL",
    "https://example.auth.eu-west-2.amazoncognito.com/oauth2/token",
)

mock_cognito_secret = {
    "COGNITO_POOL_ID": "eu-west-2_local",
    "COGNITO_CLIENT_ID": "local-client-id",
    "COGNITO_CLIENT_SECRET": "local-client-secret",
    "REDIRECT_URI": "http://localhost:3000/callback",
}
mock_azure_secret = {
    "azure_tenant_id": "tenant-id",
    "azure_client_id": "client-id",
    "azure_client_secret": "client-secret",
    "azure_scope": "https://graph.microsoft.com/.default",
    "azure_webhook_url": "https://example.invalid/webhook",
}

mock_s3_client = MagicMock(name="mock_s3_client")

with patch("boto3.client", return_value=mock_s3_client), patch(
    "boto3.session.Session.client"
) as mock_session_client:
    mock_secrets_client = MagicMock(name="mock_secrets_client")

    def _mock_get_secret_value(SecretId):
        if SecretId == os.environ["TECH_AUDIT_SECRET_MANAGER"]:
            return {"SecretString": json.dumps(mock_cognito_secret)}
        if SecretId == os.environ["AZURE_SECRET_NAME"]:
            return {"SecretString": json.dumps(mock_azure_secret)}
        return {"SecretString": "{}"}

    mock_secrets_client.get_secret_value.side_effect = _mock_get_secret_value
    mock_session_client.return_value = mock_secrets_client

    # Import your Flask app/namespace from aws_lambda_script/app
    from app import ns


@pytest.fixture
def client():
    app = Flask(__name__)  # Initialize Flask app
    api = Api(app)  # Create the Api object
    api.add_namespace(ns)  # Register the Namespace with the Api

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
