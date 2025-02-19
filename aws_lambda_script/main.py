import awsgi
from app import create_app

app = create_app()


def lambda_handler(event, context):
    """
    AWS Lambda handler function to process incoming API Gateway events using a Flask app.

    This function uses the awsgi library to handle the Flask app request and adds the necessary
    CORS headers to the response.

    Args:
        event (dict): The event dictionary containing details of the request.
        context (object): The context object providing information
            about the invocation, function, and execution environment.

    Returns:
        dict: The response dictionary with the appropriate CORS headers.
    """
    # Call the awsgi response which handles the Flask app request
    response = awsgi.response(app, event, context)
    # Add the necessary CORS headers to the response
    response["headers"]["Access-Control-Allow-Origin"] = "*"
    response["headers"]["Access-Control-Allow-Methods"] = "OPTIONS,PUT,POST,GET"
    response["headers"]["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

    return response
