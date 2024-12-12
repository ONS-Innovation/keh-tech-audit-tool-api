# User API

## Get User Information

`GET /api/v1/user`

Returns the email address of the authenticated user.

### Authorization

Requires a valid Cognito ID token in the Authorization header.

| Header | Type | Description | Required |
|-----------|-------------|-------------|-------------|
| `Authorization` | string | AWS Cognito ID token | Yes |

### Responses
| Status Code | Description |
|--------|-------------|
| `200` | Success. Returns the user's email address. ` { "email": "string" }` |
| `401` | Authorization is required |
| `404` | User not found |