# Projects API

## Get a Project

`GET /api/v1/projects/{project_name}`

Returns the project associated with the authenticated user.

### Authorization

Requires a valid Cognito ID token in the Authorization header.

| Header | Type | Description | Required |
|-----------|-------------|-------------|-------------|
| `Authorization` | string | AWS Cognito ID token | Yes |

### Path Variables

| Path Variable | Type | Description | Required |
|-----------|-------------|-------------|-------------|
| `project_name` | string | The name of the project to get | Yes |

### Responses

| Status Code | Description                             |
|-------------|-----------------------------------------|
| `200`         | Returns a project object. |
| `401`         | Authorization is required               |
| `404`         | Project not found                       |


## Update a Project

`PUT /api/v1/projects/{project_name}`

Updates a project.

### Authorization

Requires a valid Cognito ID token in the Authorization header.

| Header | Type | Description | Required |
|-----------|-------------|-------------|-------------|
| `Authorization` | string | AWS Cognito ID token | Yes |

### Path Variables

| Path Variable | Type | Description | Required |
|-----------|-------------|-------------|-------------|
| `project_name` | string | The name of the project to update | Yes |

### Request Body

```json
{
  "user": [
    {
      "email": "string",
      "roles": [
        "string"
      ],
      "grade": "string"
    }
  ],
  "details": [
    {
      "name": "string",
      "short_name": "string",
      "documentation_link": [
        "string"
      ],
      "project_description": "string",
      "project_dependencies": [
        {
          "name": "string",
          "description": "string"
        }
      ]
    }
  ],
  "developed": [
    "string"
  ],
  "source_control": [
    {
      "type": "string",
      "links": [
        {
          "description": "string",
          "url": "string"
        }
      ]
    }
  ],
  "architecture": {
    "hosting": {
      "type": [
        "string"
      ],
      "details": [
        "string"
      ]
    },
    "database": {
      "main": [
        "string"
      ],
      "others": [
        "string"
      ]
    },
    "languages": {
      "main": [
        "string"
      ],
      "others": [
        "string"
      ]
    },
    "frameworks": {
      "main": [
        "string"
      ],
      "others": [
        "string"
      ]
    },
    "cicd": {
      "main": [
        "string"
      ],
      "others": [
        "string"
      ]
    },
    "infrastructure": {
      "main": [
        "string"
      ],
      "others": [
        "string"
      ]
    }
  },
  "stage": "string",
  "supporting_tools": {
        "code_editors": {
          "main": [
            "string"
          ],
          "others": [
            "string"
            ]
        },
        "ui_tools": {
          "main": [
            "string"
          ],
          "others": [
            "string"
          ]
        },
        "diagram_tools": {
          "main": [
            "string"
          ],
          "others": [
            "string"
          ]
        },
        "project_tracking_tools": "string",
        "documentation_tools": {
          "main": [
            "string"
          ],
          "others": [
            "string"
          ]
        },
        "communication_tools": {
          "main": [
            "string"
          ],
          "others": [
            "string"
          ]
        },
        "collaboration_tools": {
          "main": [
            "string"
          ],
          "others": [
            "string"
          ]
        },
        "incident_management": "string"
      }
}
```

### Responses

| Status Code | Description                             |
|-------------|-----------------------------------------|
| `200`         | Returns the same project object as the request body. |
| `401`         | Authorization is required               |
| `404`         | Project not found                       |
| `406`         | Missing JSON data                       |