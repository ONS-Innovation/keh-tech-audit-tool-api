# Authentication

The API uses AWS Cognito for authentication. All API endpoints require a valid ID token in the Authorization header.

## Refresh Token

`GET /api/v1/refresh`

Exchange authorization code for tokens.

### Query Parameters

| Parameter | Description |
|-----------|-------------|
| `refresh_token` | Refresh token from Cognito callback |

### Response 

| Status Code | Description |
|-------------|-------------|
| `200` | Success. Response body contains the new ID token: `{"id_token": "string"}`. |
| `400` | Bad Request |