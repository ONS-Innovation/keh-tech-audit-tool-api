# Authentication

The API uses AWS Cognito for authentication. This endpoint exchanges a refresh token for a new ID token and does not require an `Authorization` header.

## Refresh Token

`POST /api/v1/refresh`

Exchange a refresh token for a new ID token.

### Request Body

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `refresh_token` | string | Refresh token returned by Cognito | Yes |

### Response 

| Status Code | Description |
|-------------|-------------|
| `200` | Success. Response body contains the new ID token: `{"id_token": "string"}`. |
| `400` | Bad Request |
| `401` | Failed to refresh token |