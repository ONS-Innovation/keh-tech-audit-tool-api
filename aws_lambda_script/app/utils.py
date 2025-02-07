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
    """
    Reads and returns Cognito data from AWS Secrets Manager.
    This function creates a Secrets Manager client using boto3, retrieves the secret value
    specified by SECRET_NAME, and returns the secret data as a JSON object.
    Returns:
        dict: The secret data retrieved from AWS Secrets Manager.
    Raises:
        ClientError: If there is an error retrieving the secret value from AWS Secrets Manager.
    """

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=REGION_NAME)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=SECRET_NAME)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    return json.loads(get_secret_value_response["SecretString"])


cognito_data = read_cognito_data()


# Used for the view project or get projects routes. This reads the data from the S3 bucket.
def read_data(duplicate=False):
    """
    Reads data from an S3 bucket and returns it as a dictionary.

    This function attempts to retrieve an object from an S3 bucket specified by
    BUCKET_NAME and OBJECT_NAME. The object is expected to be a JSON file, which
    is then parsed and returned as a dictionary.

    Returns:
        dict: The data retrieved from the S3 bucket. If the object does not exist,
              returns a dictionary with an empty "projects" list.

    Raises:
        ClientError: If there is an error other than "NoSuchKey"
                                           when accessing the S3 bucket, an HTTP 500
                                           error is raised with a description of the error.
    """
    OBJECT_NAME = "new_project_data.json"
    if duplicate:
        OBJECT_NAME = "duplicates.json"
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
def write_data(new_data, duplicate=False):
    """
    Writes the provided data to an S3 bucket.

    Args:
        new_data (dict): The data to be written to the S3 bucket.

    Raises:
        ClientError: If there is an error writing data to the S3 bucket, a 500 HTTP error is raised with a description of the error.
    """
    OBJECT_NAME = "new_project_data.json"
    if duplicate:
        OBJECT_NAME = "duplicates.json"
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
    """
    Reads array data from an S3 bucket.

    This function attempts to retrieve an object from an S3 bucket and parse its content as JSON.
    If the specified object does not exist, it returns an empty dictionary.
    If any other error occurs, it aborts the operation with a 500 status code and an error description.

    Returns:
        dict: The parsed JSON data from the S3 object, or an empty dictionary if the object does not exist.

    Raises:
        ClientError: If an error occurs while reading the S3 object, other than a missing key.
    """
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
    """
    Writes the provided array data to an S3 bucket as a JSON object.

    Args:
        new_array_data (list): The array data to be written to the S3 bucket.

    Raises:
        ClientError: If there is an error writing the data to S3,
        an HTTP 500 error is raised with a description
        of the error.
    """
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=AUTOCOMPLETE_OBJECT_NAME,
            Body=json.dumps(new_array_data, indent=4).encode("utf-8"),
        )
    except ClientError as e:
        abort(500, description=f"Error writing array data: {e}")


def get_cognito_jwks():
    """
    Fetches the JSON Web Key Set (JWKS) from the specified Amazon Cognito user pool.
    This function constructs the URL for the JWKS endpoint using the region and user pool ID,
    sends a GET request to the endpoint, and returns the JWKS if the request is successful.
    Returns:
        dict: The JWKS as a dictionary if the request is successful.
    Raises:
        ClientError: If the request fails or an exception occurs,
        an HTTP 401 error is raised with a description.
    """

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
    """
    Verifies a Cognito ID token by decoding it and checking its signature against the public keys
    provided by AWS Cognito.

    Args:
        id_token (str): The Cognito ID token to be verified.

    Returns:
        dict: The decoded token containing claims like user attributes if the token is valid.

    Raises:
        jwt.ExpiredSignatureError: If the token is expired.

    Raises:
        jwt.InvalidTokenError: If the token is invalid.
    """
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
