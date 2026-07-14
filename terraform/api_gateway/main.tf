terraform {
  backend "s3" {
    # Backend is selected using terraform init -backend-config=path/to/backend-<env>.tfbackend
    # bucket         = "sdp-dev-tf-state"
    # key            = "sdp-dev-tech-audit-tool-api-gateway/terraform.tfstate"
    # region         = "eu-west-2"
    # dynamodb_table = "terraform-state-lock"
  }

}

# Create the API Gateway REST API
resource "aws_api_gateway_rest_api" "main" {
  name = "${var.domain}-${var.service_subdomain}"

  endpoint_configuration {
    types            = ["PRIVATE"]
    vpc_endpoint_ids = [aws_vpc_endpoint.api_gateway.id]
  }

  tags = {
    Project       = var.project_tag
    TeamOwner     = var.team_owner_tag
    BusinessOwner = var.business_owner_tag
  }
}

# Create an authorizer using the Cognito User Pool
resource "aws_api_gateway_authorizer" "cognito" {
  name            = "${var.service_subdomain}-authorizer"
  rest_api_id     = aws_api_gateway_rest_api.main.id
  type            = "COGNITO_USER_POOLS"
  provider_arns   = [data.terraform_remote_state.api_auth.outputs.tech_audit_tool_user_pool_arn]
  identity_source = "method.request.header.Authorization"
}

# Root API resource
resource "aws_api_gateway_resource" "api_resource" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "api"
}

# /api/v1 resource
resource "aws_api_gateway_resource" "api_v1_resource" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.api_resource.id
  path_part   = "v1"
}

# /api/v1/projects resource
resource "aws_api_gateway_resource" "projects_resource" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.api_v1_resource.id
  path_part   = "projects"
}

# /api/v1/projects GET and POST methods
resource "aws_api_gateway_method" "projects_get" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.projects_resource.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito.id

  request_parameters = {
    "method.request.header.Authorization" = true
  }
}

resource "aws_api_gateway_method" "projects_post" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.projects_resource.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito.id

  request_parameters = {
    "method.request.header.Authorization" = true
  }
}

# /api/v1/projects/{proxy+} resource and methods
resource "aws_api_gateway_resource" "projects_proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.projects_resource.id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "projects_proxy_get" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.projects_proxy.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito.id

  request_parameters = {
    "method.request.header.Authorization" = true
    "method.request.path.proxy"           = true
  }
}

resource "aws_api_gateway_method" "projects_proxy_put" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.projects_proxy.id
  http_method   = "PUT"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito.id

  request_parameters = {
    "method.request.header.Authorization" = true
    "method.request.path.proxy"           = true
  }
}

# /api/v1/projects/filter resource and GET method
resource "aws_api_gateway_resource" "projects_filter" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.projects_resource.id
  path_part   = "filter"
}

resource "aws_api_gateway_method" "projects_filter_get" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.projects_filter.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito.id

  request_parameters = {
    "method.request.header.Authorization" = true
  }
}

# /api/v1/user resource and GET method
resource "aws_api_gateway_resource" "user_resource" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.api_v1_resource.id
  path_part   = "user"
}

resource "aws_api_gateway_method" "user_get" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.user_resource.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito.id

  request_parameters = {
    "method.request.header.Authorization" = true
  }
}

# /api/v1/verify resource and GET method
resource "aws_api_gateway_resource" "verify_resource" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.api_v1_resource.id
  path_part   = "verify"
}

resource "aws_api_gateway_method" "verify_get" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.verify_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

# /swagger.json resource and GET method
resource "aws_api_gateway_resource" "swagger_json" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "swagger.json"
}

resource "aws_api_gateway_method" "swagger_json_get" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.swagger_json.id
  http_method   = "GET"
  authorization = "NONE"
}

# /swaggerui resource and GET method
resource "aws_api_gateway_resource" "swaggerui" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "swaggerui"
}

resource "aws_api_gateway_method" "swaggerui_get" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.swaggerui.id
  http_method   = "GET"
  authorization = "NONE"
}

# /swaggerui/{proxy+} resource and GET method
resource "aws_api_gateway_resource" "swaggerui_proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.swaggerui.id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "swaggerui_proxy_get" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.swaggerui_proxy.id
  http_method   = "GET"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.proxy" = true
  }
}

# Add root path ANY method (for "/") to handle all HTTP methods
resource "aws_api_gateway_method" "root_any" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_rest_api.main.root_resource_id
  http_method   = "ANY"
  authorization = "NONE"

  lifecycle {
    create_before_destroy = false
  }
}

# /api/v1/refresh resource and POST method
resource "aws_api_gateway_resource" "refresh_resource" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.api_v1_resource.id
  path_part   = "refresh"
}

resource "aws_api_gateway_method" "refresh_post" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.refresh_resource.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito.id

  request_parameters = {
    "method.request.header.Authorization" = true
  }
}

# Lambda integrations for protected endpoints
resource "aws_api_gateway_integration" "lambda_integration" {
  for_each = {
    "swagger_json_get"    = aws_api_gateway_method.swagger_json_get
    "swaggerui_get"       = aws_api_gateway_method.swaggerui_get
    "swaggerui_proxy_get" = aws_api_gateway_method.swaggerui_proxy_get
    "projects_get"        = aws_api_gateway_method.projects_get
    "projects_post"       = aws_api_gateway_method.projects_post
    "projects_proxy_get"  = aws_api_gateway_method.projects_proxy_get
    "projects_proxy_put"  = aws_api_gateway_method.projects_proxy_put
    "projects_filter_get" = aws_api_gateway_method.projects_filter_get
    "user_get"            = aws_api_gateway_method.user_get
    "refresh_post"        = aws_api_gateway_method.refresh_post
  }

  rest_api_id             = aws_api_gateway_rest_api.main.id
  resource_id             = each.value.resource_id
  http_method             = each.value.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${data.terraform_remote_state.api_lambda.outputs.lambda_function_arn}/invocations"
}

# Lambda integration for verify endpoint (unauthenticated)
resource "aws_api_gateway_integration" "verify_integration" {
  rest_api_id             = aws_api_gateway_rest_api.main.id
  resource_id             = aws_api_gateway_resource.verify_resource.id
  http_method             = aws_api_gateway_method.verify_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${data.terraform_remote_state.api_lambda.outputs.lambda_function_arn}/invocations"
}

# Specific integration for root path
resource "aws_api_gateway_integration" "root_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.main.id
  resource_id             = aws_api_gateway_rest_api.main.root_resource_id
  http_method             = aws_api_gateway_method.root_any.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${data.terraform_remote_state.api_lambda.outputs.lambda_function_arn}/invocations"

  lifecycle {
    create_before_destroy = false
  }
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id

  depends_on = [
    aws_api_gateway_integration.lambda_integration,
    aws_api_gateway_integration.verify_integration,
    aws_api_gateway_integration.root_lambda_integration,
    aws_api_gateway_rest_api_policy.main
  ]

  lifecycle {
    create_before_destroy = true
  }

  // This block will cause a redeployment of the API Gateway whenever the main.tf file changes
  // Since the API routes are defined in this file, any changes to the routes will trigger a redeployment
  triggers = {
    redeployment = sha1(jsonencode([
      file("main.tf"),
      file("iam.tf"),
      file("domain.tf"),
      file("network.tf"),
      file("cloudwatch.tf"),
      file("data.tf"),
      file("variables.tf"),
    ]))
  }
}

# API Gateway Stage
resource "aws_api_gateway_stage" "main" {
  deployment_id = aws_api_gateway_deployment.main.id
  rest_api_id   = aws_api_gateway_rest_api.main.id
  stage_name    = var.stage_name

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      caller         = "$context.identity.caller"
      user           = "$context.identity.user"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      resourcePath   = "$context.resourcePath"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
      errorMessage   = "$context.error.message"
      errorType      = "$context.error.responseType"
    })
  }
}

# Stage settings
resource "aws_api_gateway_method_settings" "all" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  stage_name  = aws_api_gateway_stage.main.stage_name
  method_path = "*/*"

  settings {
    logging_level      = "ERROR"
    data_trace_enabled = false
    metrics_enabled    = true
  }
}

# Lambda permission for API Gateway
resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = data.terraform_remote_state.api_lambda.outputs.lambda_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.main.execution_arn}/*/*/*"
}
