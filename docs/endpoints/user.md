# User API

## Get User Information

`GET /api/v1/user`

Returns the email address and Cognito groups of the authenticated user.

### Authorization

Requires a valid Cognito ID token in the Authorization header.

| Header | Type | Description | Required |
|-----------|-------------|-------------|-------------|
| `Authorization` | string | AWS Cognito ID token | Yes |

### Responses
| Status Code | Description |
|--------|-------------|
| `200` | Success. Returns the user object. `{"email": "string", "groups": []}` |
| `401` | Authorization is required |