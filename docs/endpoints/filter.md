# Filter API

## Filter Projects

`GET /api/v1/projects/filter`

Filter projects based on multiple criteria.

### Authorization

Requires a valid Cognito ID token in the Authorization header.

| Header | Type | Description | Required |
|-----------|-------------|-------------|-------------|
| `Authorization` | string | AWS Cognito ID token | Yes |

### Query Parameters

| Parameter | Type | Description | Required |
|-----------|-------------|-------------|-------------|
| `email` | string | User email to filter by (comma-separated) | False |
| `roles` | string | Roles to filter by (comma-separated) | False |
| `name` | string | Project name to filter by (comma-separated) | False |
| `developed` | string | Filter by development type ("In house", "Partnership", "Outsourced") | False |
| `languages` | string | Programming languages to filter by (comma-separated) | False |
| `source_control` | string | Source control systems to filter by (comma-separated) | False |
| `hosting` | string | Hosting platforms to filter by (comma-separated) | False |
| `database` | string | Database types to filter by (comma-separated) | False |
| `frameworks` | string | Frameworks to filter by (comma-separated) | False |
| `cicd` | string | CI/CD tools to filter by (comma-separated) | False |
| `infrastructure` | string | Infrastructure tools to filter by (comma-separated) | False |
| `publishing` | string | Publishing target to filter by (comma-separated) | False |
| `return` | string | Sections to return in response (user, details, developed, source_control, architecture) | False |

### Responses

| Status Code | Description                             |
|-------------|-----------------------------------------|
| `200`         | Returns filtered list of projects matching the specified criteria. If the `return` parameter is specified, only the requested sections will be included in the response. |
| `401`         | Authorization is required               |
| `404`         | Project not found                       |