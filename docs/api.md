# API Documentation

The Tech Audit Tool API provides endpoints for managing project data and authentication. ***Most*** endpoints require authentication using AWS Cognito ID tokens.

### Interactive API Documentation

[Open API Documentation](https://tech-audit-tool-api.sdp-dev.aws.onsdigital.uk) or interact below:

<iframe src="https://tech-audit-tool-api.sdp-dev.aws.onsdigital.uk/" width="100%" height="800px" frameborder="0"></iframe>

    
### Authentication

**Most** API endpoints require a valid AWS Cognito ID token in the Authorization header:

| Header | Type | Description | Required |
|-----------|-------------|-------------|-------------|
| `Authorization` | string | AWS Cognito ID token | Yes |

### Base URL

All endpoints are prefixed with `/api/v1/` as the namespace.

### Available Endpoints

- [Authentication](endpoints/auth.md)
    - Verify tokens
    - Refresh tokens
- [Projects](endpoints/projects.md)
    - Get all projects
    - Create new project
- [Project](endpoints/project.md)
    - Get project details
    - Update project
- [User](endpoints/user.md)
    - Get user information
- [Filters](endpoints/filter.md)
    - Filter projects by criteria