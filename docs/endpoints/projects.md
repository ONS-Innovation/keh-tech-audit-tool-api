# Projects API

## Get Projects

`GET /api/v1/projects`

Returns all projects associated with the authenticated user.

### Authorization

Requires a valid Cognito ID token in the Authorization header.

| Header | Type | Description | Required |
|-----------|-------------|-------------|-------------|
| `Authorization` | string | AWS Cognito ID token | Yes |

### Responses

| Status Code | Description                             |
|-------------|-----------------------------------------|
| `200`         | Returns a list of project objects. |
| `401`         | Authorization is required               |
| `404`         | Projects not found |

## Create a Project

`POST /api/v1/projects`

Creates a new project.

### Authorization

Requires a valid Cognito ID token in the Authorization header.

| Header | Type | Description | Required |
|-----------|-------------|-------------|-------------|
| `Authorization` | string | AWS Cognito ID token | Yes |

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

| Status Code | Description                                             |
|-------------|---------------------------------------------------------|
| `201`         | Created project. Returns the same project object as the request body.                                        |
| `401`         | Authorization is required                              |
| `406`         | Missing JSON data                                      |
| `409`         | Project with the same name and owner already exists    |