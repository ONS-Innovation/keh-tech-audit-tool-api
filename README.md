
# KEH | Tech Audit Tool - API

A Flask and Flask_RestX API for the tech audit tool.

## Setting up & Running Locally

Clone the project

```bash
  git clone https://github.com/ONS-Innovation/keh-tech-audit-tool-api
```

Install dependencies

```bash
  make install
```

Install dev dependencies to run linting tools

```bash
  make install-dev
```

Import secrets

```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
export AWS_DEFAULT_REGION=eu-west-2 
export AWS_SECRET_NAME=github-tooling-suite/onsdigital
```

Go to the aws_lambda_script directory

```bash
  cd aws_lambda_script
```

Run the project locally

```bash
	poetry run python3 -m app
```




## API Reference

Before testing the API, you need to use Postman to get your ID token. Follow this [guide](https://medium.com/@shivkaundal/secure-your-apis-with-cognito-authorizers-for-aws-api-gateway-ba15914b64b2#1422) to get your token. Make sure to use the ID token, instead of Access Token.

You need to authenticate with the `keh-tech-audit-tool-pool` to get the correct, authorized token.

### Get user email

```http
  GET /api/user
```

| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. ID Token (Not access) |

Get's the users email.

### Get all user projects

```http
  GET /api/projects
```

| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. ID Token (Not access) |

Get's the projects associated with the users email.

### Get a specific user project

```http
  GET /api/projects/<project_name>
```

| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. ID Token (Not access) |

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `<project_name>`      | `string` | **Required**. The project you want to get |


Get's a specific project from the user.

### Create a new project

```http
  POST /api/projects/
```


| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. ID Token (Not access) |


Send JSON in this format:
```JSON
{"projects": [
        {
            "user": [ 
                {
                    "email": "",
                    "roles": [
                        "owner"
                    ]
                }
            ],
            "details": {
                "name": "Project1",
                "short_name": "This is project 1",
                "documentation_link": ""
            },
            "developed":[  
                "Partnership",
                ["ONS", "GDS"]
            ],
            "source_control":[
                "GitHub"
            ],
            "architecture": {
                "hosting": {"type": "Hybrid", "detail": []},
                "database": {"main": "MongoDB", "others": []},
                "languages": {"main": "Python", "others": ["JavaScript", "Java"]},
                "frameworks": {"main": "React", "others": []},
                "CICD": {"main": "Python", "others": ["JavaScript", "Java"]},
                "infrastructure": {"main": "Python", "others": []}
            }
        }
    ]
}
```
Create's a project. If the language is not in the array_data.json bucket then it is added.


### Get autocomplete from string

```http
  GET /api/autocomplete
```

| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. ID Token (Not access) |

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `type` | `string` | **Required**. The type of array ie. languages. |
| `search` | `string` | **Required**. The string needing autocomplete. |

Returns a list of potential autocomplete.

Example REQUEST: 
```bash
GET http://localhost:5000/api/autocomplete?type=languages&search=script
```

Example RESPONSE:
```JSON
[
  "javascript",
  "typescript",
  "actionscript",
  "postscript",
  "jscript"
]
```


## Authorization with Cognito and API Gateway

Visiting the [Cognito UI](https://keh-tech-audit-tool.auth.eu-west-2.amazoncognito.com/oauth2/authorize?client_id=dm3289s0tqtsr5qn2qm5i9fql&response_type=code&scope=email+openid+phone&redirect_uri=https%3A%2F%2Fdutwj6q915.execute-api.eu-west-2.amazonaws.com%2Fdev%2Fapi%2Fverify), and successfully logging in, will redirect you to:

```bash
/api/verify?code=<code>
```

This returns your token, which you can use in testing the authentication on the API. Use this token in the Authorization header to authenticate your requests.

The /api/verify route get's the client keys and redirect uri from the bucket.

