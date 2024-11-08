import json
import os
import boto3
import jwt
import requests
from flask_restx import abort
from botocore.exceptions import ClientError
from jwt.algorithms import RSAAlgorithm

# Connecting to S3
BUCKET_NAME = os.getenv("TECH_AUDIT_DATA_BUCKET")
SECRET_NAME = os.getenv("TECH_AUDIT_SECRET_MANAGER")
REGION_NAME = os.getenv("AWS_DEFAULT_REGION")
OBJECT_NAME = "new_project_data.json"
AUTOCOMPLETE_OBJECT_NAME = "array_data.json"

# Create an S3 client
s3 = boto3.client("s3", region_name=REGION_NAME)

def read_cognito_data():

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=REGION_NAME
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=SECRET_NAME
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    return json.loads(get_secret_value_response['SecretString'])

cognito_data = read_cognito_data()

def return_cognito_data():
    return cognito_data

# Used for the view project or get projects routes. This reads the data from the S3 bucket.
def read_data():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_NAME)
        data = json.loads(response["Body"].read().decode("utf-8"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            data = {"projects": []}
        else:
            abort(500, description=f"Error reading data: {e}")
    return data


# Used for the POST request to add a new project to the S3 bucket.
def write_data(new_data):
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=OBJECT_NAME,
            Body=json.dumps(new_data, indent=4).encode("utf-8"),
        )
    except ClientError as e:
        abort(500, description=f"Error writing data: {e}")


# This is for the autocomplete feature. The 'array_data.json'
# file in the S3 stores the data for the autocomplete.
# Although, this is now only used to update the json file if
# a user adds a new type of architecture that isn't in the list.
def read_array_data():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=AUTOCOMPLETE_OBJECT_NAME)
        array_data = json.loads(response["Body"].read().decode("utf-8"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            array_data = {}
        else:
            abort(500, description=f"Error reading array data: {e}")
    return array_data


def write_array_data(new_array_data):
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=AUTOCOMPLETE_OBJECT_NAME,
            Body=json.dumps(new_array_data, indent=4).encode("utf-8"),
        )
    except ClientError as e:
        abort(500, description=f"Error writing array data: {e}")


def get_cognito_jwks():
    # Get the JWKS from the cognito user pool
    # Includes the region (eu-west-2) and user pool ID (eu-west-2_cv6SLP60y)
    try:
        response = requests.get(
            f"https://cognito-idp.{REGION_NAME}.amazonaws.com/{cognito_data['COGNITO_POOL_ID']}/.well-known/jwks.json",
            timeout=16,
        )
        if response.status_code == 200:
            return response.json()
        else:
            return abort(401, description="Unable to fetch JWKS")
    except Exception as e:
        abort(401, description=f"{e.__class__.__name__}: Unable to fetch JWKS")


def verify_cognito_token(id_token):
    jwks = get_cognito_jwks()

    try:
        # Decode the ID token without verification to get the header and find the key ID
        unverified_header = jwt.get_unverified_header(id_token)
        key_id = unverified_header["kid"]

        # Find the correct public key in the JWKS
        public_key = None
        for key in jwks["keys"]:
            if key["kid"] == key_id:
                public_key = RSAAlgorithm.from_jwk(json.dumps(key))
                break

        if public_key is None:
            abort(401, description="Public key not found in JWKS")

        # Now verify the token
        decoded_token = jwt.decode(
            id_token,
            public_key,
            algorithms=["RS256"],
            audience=cognito_data["COGNITO_CLIENT_ID"],
            issuer=f"https://cognito-idp.{REGION_NAME}.amazonaws.com/{cognito_data['COGNITO_POOL_ID']}",
        )
        return decoded_token  # Return the decoded token (contains claims like user attributes)

    except jwt.ExpiredSignatureError:
        abort(401, description="Token is expired")
    except jwt.InvalidTokenError as e:
        abort(401, description=f"Invalid token: {str(e)}")