resource "aws_secretsmanager_secret" "cognito_secrets" {
  name = "${var.domain}-${var.service_subdomain}-cognito-secrets"
  
  tags = {
    Environment = var.domain
    Service     = var.service_subdomain
  }
}

resource "aws_secretsmanager_secret_version" "cognito_secrets_version" {
  secret_id = aws_secretsmanager_secret.cognito_secrets.id
  
  secret_string = jsonencode({
    COGNITO_POOL_ID     = var.cognito_pool_id
    COGNITO_CLIENT_ID   = var.cognito_client_id
    COGNITO_SECRET_ID   = var.cognito_secret_id
    REDIRECT_URI        = var.redirect_uri
  })
}
