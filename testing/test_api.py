import pytest
import json
import os
import datetime
from unittest.mock import patch

# Mock verify_cognito_token for authentication
mocked_user_email = os.getenv("MOCK_USER_EMAIL", "test@ons.gov.uk")


def mock_verify_cognito_token(token):
    return {"email": mocked_user_email}


# Mock reading data function
def mock_read_data():
    return {
        "projects": [
            {
                "details": {"name": "Test Project"},
                "user": [{"email": mocked_user_email}],
                "architecture": {
                    "languages": {"main": "python", "others": ["javascript"]}
                },
            }
        ]
    }


# Mock reading array data
def mock_read_array_data():
    return {
        "languages": ["python", "javascript", "java"],
        "IDEs": ["vscode", "pycharm"],
        "misc": ["git"],
    }


@pytest.fixture
def client():
    from app import create_app

    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Helper to get mock token from environment
def get_mock_token():
    mock_token = os.getenv("MOCK_TOKEN")
    print(mock_token)
    if not mock_token:
        raise EnvironmentError(
            "MOCK_TOKEN environment variable is not set. Please set it to run the tests."
        )
    return mock_token


# Test for "/user" route
@patch("app.utils.verify_cognito_token", side_effect=mock_verify_cognito_token)
def test_get_user(mock_verify_token, client):
    mock_token = get_mock_token()
    response = client.get("/api/v1/user", headers={"Authorization": f"{mock_token}"})
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, {response.data}"
    data = json.loads(response.data)
    assert data["email"] == mocked_user_email


# Test for "/projects" route - GET
@patch("app.utils.read_data", side_effect=mock_read_data)
@patch("app.utils.verify_cognito_token", side_effect=mock_verify_cognito_token)
def test_get_projects(mock_verify_token, mock_read, client):
    mock_token = get_mock_token()
    response = client.get(
        "/api/v1/projects", headers={"Authorization": f"{mock_token}"}
    )
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, {response.data}"
    data = json.loads(response.data)
    assert "Test Project" in data[-1]["details"][0]["name"]


# Test for POSTing a new project with a timestamp in the name
@patch("app.utils.read_data", side_effect=mock_read_data)
@patch("app.utils.verify_cognito_token", side_effect=mock_verify_cognito_token)
@patch("app.utils.write_data")
def test_post_and_get_project_with_timestamp(
    mock_write_data, mock_verify_token, mock_read, client
):
    mock_token = get_mock_token()

    # Create a unique project name using time.time()
    project_name = f"Test Project {datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d-%H-%M-%S')}"

    new_project = {
        "user": [
            {
                "email": mocked_user_email,
                "roles": ["Technical Contact", "Editor"],
                "grade": "SEO",
            },
            {
                "email": "Dariana.Ethel.Sipes@ons.gov.uk",
                "roles": ["Delivery Manager Contact"],
                "grade": "HEO",
            },
        ],
        "details": [
            {
                "name": f"Test Project {datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d-%H-%M-%S')}",
                "short_name": "Principal",
                "documentation_link": ["https://hollis.biz.ons.gov.uk"],
                "project_description": "Operative hybrid instruction set",
                "project_dependencies": [
                    {"name": "Blaise 5", "description": "For Testing"}
                ],
            }
        ],
        "developed": ["In-house", []],
        "source_control": [
            {
                "type": "GitHub",
                "links": [{"description": "systematic", "url": "http://dell.name"}],
            }
        ],
        "architecture": {
            "hosting": {"type": ["Hybrid"], "details": ["AWS", "Local"]},
            "database": {"main": [], "others": ["DocumentDB"]},
            "languages": {"main": ["Python"], "others": ["JavaScript", "Java"]},
            "frameworks": {"main": [], "others": ["Flask"]},
            "cicd": {"main": [], "others": ["Github Actions"]},
            "infrastructure": {"main": [], "others": ["Jenkins"]},
            "publishing": {"main": [], "others": ["Pypi"]},
        },
        "stage": "Development",
        "supporting_tools": {
            "code_editors": ["VSCode"],
            "ui_tools": ["Figma"],
            "diagram_tools": ["Draw.io"],
            "project_tracking_tools": ["Jira"],
            "documentation_tools": ["Confluence"],
            "communication_tools": ["Teams"],
            "collaboration_tools": ["Github"],
            "incident_management": "ServiceNow",
        },
    }

    # POST the new project
    post_response = client.post(
        "/api/v1/projects",
        data=json.dumps(new_project),
        headers={"Authorization": f"{mock_token}", "Content-Type": "application/json"},
    )
    print(post_response.data)

    assert (
        post_response.status_code == 201
    ), f"Unexpected status code: {post_response.status_code}, {post_response.data}"

    # GET the project by name
    get_response = client.get(
        f"/api/v1/projects/{project_name}", headers={"Authorization": f"{mock_token}"}
    )
    assert (
        get_response.status_code == 200
    ), f"Unexpected status code: {get_response.status_code}, {get_response.data}"
    data = json.loads(get_response.data)
    assert data["details"][0]["name"] == project_name
    assert data["user"][0]["email"] == mocked_user_email


# Test for "/verify" route
@patch(
    "app.resources.exchange_code_for_tokens",
    return_value={"id_token": "mockidtoken", "refresh_token": "mockrefreshtoken"},
)
def test_verify_token(mock_exchange, client):
    mock_token = get_mock_token()
    response = client.get(
        "/api/v1/verify",
        query_string={"code": "mockcode"},
        headers={"Authorization": f"{mock_token}"},
    )
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, {response.data}"
    data = json.loads(response.data)
    assert data["id_token"] == "mockidtoken"
