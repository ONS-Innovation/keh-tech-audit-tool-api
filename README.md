
# Tech Audit Tool - API

A Flask and flask-restx API for the tech audit tool.

## Contents

- [Tech Audit Tool - API](#tech-audit-tool---api)
  - [Contents](#contents)
  - [Setting up \& Running Locally](#setting-up--running-locally)
  - [Testing](#testing)
  - [Testing with Postman](#testing-with-postman)
  - [MkDocs Documentation](#mkdocs-documentation)
    - [Running the MkDocs locally](#running-the-mkdocs-locally)
    - [Deploying the MkDocs](#deploying-the-mkdocs)
      - [Deployment GitHub Action](#deployment-github-action)
      - [Manual Deployment](#manual-deployment)
  - [API Reference](#api-reference)
    - [Get user email](#get-user-email)
    - [Get new ID token from refresh token](#get-new-id-token-from-refresh-token)
    - [Get all user projects](#get-all-user-projects)
    - [Get a specific user project](#get-a-specific-user-project)
    - [Create a new project](#create-a-new-project)
    - [Get autocomplete from string \[REMOVED\]](#get-autocomplete-from-string-removed)
    - [Get filtered projects](#get-filtered-projects)
    - [Edit a project](#edit-a-project)
  - [Authorization with Cognito and API Gateway](#authorization-with-cognito-and-api-gateway)


## Setting up & Running Locally

Clone the project

```bash
git clone https://github.com/ONS-Innovation/keh-tech-audit-tool-api.git
```

Install dependencies

```bash
make install
```

Install dev dependencies to run linting tools

```bash
make install-dev
```

Set environment variables:

```bash
export TECH_AUDIT_DATA_BUCKET='<sdp-dev-tech-audit-tool-api-testing/sdp-dev-tech-audit-tool-api>' # The latter bucket should be used in production
export TECH_AUDIT_SECRET_MANAGER='sdp-dev-tech-audit-tool-api/secrets'
export AWS_COGNITO_TOKEN_URL='https://tech-audit-tool-api-sdp-dev.auth.eu-west-2.amazoncognito.com/oauth2/token'
export AWS_DEFAULT_REGION='eu-west-2'
export REDIRECT_URI='http://localhost:8000'
```

Go to the aws_lambda_script directory

```bash
cd aws_lambda_script
```

Run the project locally (with UI)
```bash
make run-local
```
or
```bash
poetry run flask --app app run --port=5000
```
This will run the API on port 5000, to which the UI can now access

Run the project locally (without UI)
```bash
make run-no-ui
```
or
```bash
poetry run flask --app app run --port=8000
```

## Testing

This repo utilises PyTest for the testing. Please make sure you have installed dev dependencies before running tests.

To test you need a mock token. Visit the Cognito UI with the redirect URL set to your local environment. Once successully logged in, copy the `id_token`.

Then import the token into your environment and set the email of the user you want to test with:

```bash
export MOCK_TOKEN=<id_token>
export MOCK_USER_EMAIL=<email>
```

Make sure dev dependencies are installed:
```bash
make install-dev
```

When in root directory, run the testing command. If you are in `aws_lambda_script` it will fail.
```bash
make pytest
```

If all tests fail, please relogin to the Cognito and use a new token.

Once you have finished testing, clean the temp files with:
```bash
make clean
```

## Testing with Postman

View the Postman workspace for this project [here](https://www.postman.com/science-pilot-55892832/workspace/keh-tech-audit-tool-api/collection/38871441-e42f661e-6430-4f46-8182-083e9e0fd4ad?action=share&creator=38871441&active-environment=38871441-7c5e3795-74f5-46b3-9034-637561aba746).

Please read the description or README to understand how to use this workspace. You need to get a mock_token to authenticate yourself in each request.

## MkDocs Documentation

### Running the MkDocs locally

To install the dependencies for the MkDocs, run the following command:

```bash
make install-docs
```

Then run the following command to run the MkDocs:

```bash
make mkdocs
```

### Deploying the MkDocs

#### Deployment GitHub Action

The MkDocs documentation is automatically deployed to the `gh-pages` branch of the repository using a GitHub Action. The action is triggered on every push to the `main` branch. This action is defined within `./.github/workflows/deploy_mkdocs.yml`.

#### Manual Deployment

Deploying the MkDocs is done by running the following command:

```bash
make mkdocs-deploy
```

This will build the MkDocs documentation and deploy it to the `gh-pages` branch of the repository. The documentation will be available at [https://ons-innovation.github.io/keh-tech-audit-tool-api](https://ons-innovation.github.io/keh-tech-audit-tool-api).

## API Reference

Before testing the API, you need to use the above instructions at **Testing** to get a mock token, as all requests need to be authenticated.

| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. ID Token (Not access) |
 
### Get user email

```http
GET /api/v1/user
```

Get's the users email.

### Get new ID token from refresh token

```http
POST /api/v1/refresh
```

| Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `refresh_token`      | `string` | **Required**. The refresh token |

Get's a new id_token from a refresh token. Old id_token is killed, refresh_token
can be used multiple times to get a new id_token.

### Get all user projects

```http
GET /api/v1/projects
```

Get's the projects associated with the users email.

### Get a specific user project

```http
GET /api/v1/projects/<project_name>
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `<project_name>`      | `string` | **Required**. The project you want to get |


Get's a specific project from the user.

### Create a new project

```http
POST /api/v1/projects/
```

Send JSON in this format:
```JSON
{
    "user": [
      {
        "email": "Email",
        "roles": ["Technical Contact"],
        "grade": "Grade"
      },
      {
        "email": "Email",
        "roles": ["Delivery Manager Contact"],
        "grade": "Grade"
      }
    ],
    "details":[ 
      {
        "name": "Name",
        "short_name": "Short Name",
        "documentation_link": ["List of strings"],
        "project_description": "Description"
      }]
    ,
    "developed": ["In-house", []],
    "source_control": [
      {
        "type": "GitHub",
        "links": [
          {
            "description": "Description",
            "url": "URL"
          }
        ]
      }
    ],
    "architecture": {
      "hosting": {
        "type": ["Hybrid"],
        "details": ["List of strings"]
      },
      "database": {
        "main": [],
        "others": ["List of strings"]
      },
      "languages": {
        "main": ["List of strings"],
        "others": ["List of strings"]
      },
      "frameworks": {
        "main": [],
        "others": ["List of strings"]
      },
      "cicd": {
        "main": [],
        "others": ["List of strings"]
      },
      "environments": {
        "dev": "Boolean",
        "int": "Boolean",
        "uat": "Boolean",
        "preprod": "Boolean",
        "prod": "Boolean",
        "postprod": "Boolean",
      },
      "infrastructure": {
        "main": [],
        "others": ["List of strings"]
      },
      "publishing": {
        "main": [],
        "others": ["List of strings"]
      }
    },
    "stage":"Development",
    "project_dependencies":[
      {
        "name": "string",
        "description": "string"
      }
    ],
    "supporting_tools": {
          "code_editors": {
            "main": [],
            "others": [
              "List of strings"
              ]
          },
          "ui_tools": {
            "main": [],
            "others": [
              "List of strings"
            ]
          },
          "diagram_tools": {
            "main": [],
            "others": [
              "List of strings"
            ]
          },
          "project_tracking_tools": "string",
          "documentation_tools": {
            "main": [],
            "others": [
              "List of strings"
            ]
          },
          "communication_tools": {
            "main": [],
            "others": [
              "List of strings"
            ]
          },
          "collaboration_tools": {
            "main": [],
            "others": [
              "List of strings"
            ]
          },
          "incident_management": "string"
        }
  }
```
Creates a project. If the languages, database, frameworks, cicd, infrastructure or source control is not in the `array_data.json` bucket, then it is added.


### Get autocomplete from string [REMOVED]

```http
GET /api/v1/autocomplete
```
Removed as autocomplete is processed on front-end.


### Get filtered projects 

```http
GET /api/v1/projects/filter
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `<filter>`      | `string` | **Required**. The specific filter. Multiple filter seperated by a comma (,) |
| `<return>`      | `string` | What you want returned from the project. Multiple return filter seperated by a comma (,) |


Get's projects using a filter.

Filter can be one or more of: email, roles, name, developed, source_control, hosting, database, languages, frameworks, cicd, infrastructure.

Return can be one or more of: user, details, developed, source_control, architecture.


### Edit a project

```http
PUT /api/v1/projects/{project_name}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `<project_name>`      | `string` | **Required**. The project you want to get |


Send JSON in this format:
```JSON
{
    "user": [
      {
        "email": "Email",
        "roles": ["Technical Contact"],
        "grade": "Grade"
      },
      {
        "email": "Email",
        "roles": ["Delivery Manager Contact"],
        "grade": "Grade"
      }
    ],
    "details":[ 
      {
        "name": "Name",
        "short_name": "Short Name",
        "documentation_link": ["List of strings"],
        "project_description": "Description"
      }]
    ,
    "developed": ["In-house", []],
    "source_control": [
      {
        "type": "GitHub",
        "links": [
          {
            "description": "Description",
            "url": "URL"
          }
        ]
      }
    ],
    "architecture": {
      "hosting": {
        "type": ["Hybrid"],
        "details": ["List of strings"]
      },
      "database": {
        "main": [],
        "others": ["List of strings"]
      },
      "languages": {
        "main": ["List of strings"],
        "others": ["List of strings"]
      },
      "frameworks": {
        "main": [],
        "others": ["List of strings"]
      },
      "cicd": {
        "main": [],
        "others": ["List of strings"]
      },
      "environments": {
        "dev": "Boolean",
        "int": "Boolean",
        "uat": "Boolean",
        "preprod": "Boolean",
        "prod": "Boolean",
        "postprod": "Boolean",
      },
      "infrastructure": {
        "main": [],
        "others": ["List of strings"]
      },
      "publishing": {
        "main": [],
        "others": ["List of strings"]
      }
    },
    "stage":"Development",
    "project_dependencies":[
      {
        "name": "string",
        "description": "string"
      }
    ],
    "supporting_tools": {
          "code_editors": {
            "main": [],
            "others": [
              "List of strings"
              ]
          },
          "ui_tools": {
            "main": [],
            "others": [
              "List of strings"
            ]
          },
          "diagram_tools": {
            "main": [],
            "others": [
              "List of strings"
            ]
          },
          "project_tracking_tools": "string",
          "documentation_tools": {
            "main": [],
            "others": [
              "List of strings"
            ]
          },
          "communication_tools": {
            "main": [],
            "others": [
              "List of strings"
            ]
          },
          "collaboration_tools": {
            "main": [],
            "others": [
              "List of strings"
            ]
          },
          "incident_management": "string"
        }
  }
```
Edits a project by checking if the languages, database, frameworks, cicd, environments, infrastructure, publishing or source control are missing from the `array_data.json` bucket. If any are missing, they are added.


## Authorization with Cognito and API Gateway

Visiting the Cognito UI and successfully logging in, will redirect you to:

```bash
/api/v1/verify?code=<code>
```

This returns your token, which you can use in testing the authentication on the API. Use this token in the Authorization header to authenticate your requests.

The /api/v1/verify route get's the client keys and redirect uri from the bucket.

### Deployments with Concourse

#### Allowlisting your IP
To setup the deployment pipeline with concourse, you must first allowlist your IP address on the Concourse
server. IP addresses are flushed everyday at 00:00 so this must be done at the beginning of every working day
whenever the deployment pipeline needs to be used. Follow the instructions on the Confluence page (SDP Homepage > SDP Concourse > Concourse Login) to
login. All our pipelines run on sdp-pipeline-prod, whereas sdp-pipeline-dev is the account used for
changes to Concourse instance itself. Make sure to export all necessary environment variables from sdp-pipeline-prod (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN).

#### Setting up a pipeline
When setting up our pipelines, we use ecs-infra-user on sdp-dev to be able to interact with our infrastructure on AWS. The credentials for this are stored on
AWS Secrets Manager so you do not need to set up anything yourself.

To set the pipeline, run the following script:
```bash
chmod u+x ./concourse/scripts/set_pipeline.sh
./concourse/scripts/set_pipeline.sh KEH-TAT-API
```
Note that you only have to run chmod the first time running the script in order to give permissions.
This script will set the branch and pipeline name to whatever branch you are currently on. It will also set the image tag on ECR to the current commit hash at the time of setting the pipeline.

The pipeline name itself will usually follow a pattern as follows: `<repo-name>-<branch-name>`
If you wish to set a pipeline for another branch without checking out, you can run the following:
```bash
./concourse/scripts/set_pipeline.sh KEH-TAT-API <branch_name>
```

If the branch you are deploying is "main" or "master", it will trigger a deployment to the sdp-prod environment. To set the ECR image tag, you must draft a Github release pointing to the latest release of the main/master branch that has a tag in the form of vX.Y.Z. Drafting up a release will automatically deploy the latest version of the main/master branch with the associated release tag, but you can also manually trigger a build through the Concourse UI or the terminal prompt.

#### Triggering a pipeline
Once the pipeline has been set, you can manually trigger a build on the Concourse UI, or run the following command:
```bash
fly -t aws-sdp trigger-job -j KEH-TAT-API-<branch-name>/build-and-push
```

