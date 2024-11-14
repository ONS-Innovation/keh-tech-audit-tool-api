resource "aws_lambda_function" "tech_audit_lambda" {
  function_name = "${var.domain}-${var.service_subdomain}-lambda"
  package_type  = "Image"
  image_uri     = "${var.aws_account_id}.dkr.ecr.${var.region}.amazonaws.com/${var.ecr_repository}:${var.image_tag}"
  
  role = aws_iam_role.lambda_execution_role.arn

  memory_size = 128
  timeout     = 30

  environment {
    variables = {
      BUCKET_NAME = var.tech_audit_data_bucket_name
    }
  }
}

# IAM role for Lambda
resource "aws_iam_role" "lambda_execution_role" {
  name = "${var.domain}-${var.service_subdomain}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Basic Lambda execution policy
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# S3 access policy for Lambda
resource "aws_iam_role_policy" "lambda_s3_access" {
  name = "${var.domain}-${var.service_subdomain}-lambda-s3-policy"
  role = aws_iam_role.lambda_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::${var.tech_audit_data_bucket_name}",
          "arn:aws:s3:::${var.tech_audit_data_bucket_name}/*"
        ]
      }
    ]
  })
}

# Additional policy for Secrets Manager, CloudWatch Logs, API Gateway, and S3
resource "aws_iam_role_policy" "lambda_additional_permissions" {
  name = "${var.domain}-${var.service_subdomain}-lambda-additional-policy"
  role = aws_iam_role.lambda_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup"
        ]
        Resource = "arn:aws:logs:${var.region}:${var.aws_account_id}:*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = [
          "arn:aws:logs:${var.region}:${var.aws_account_id}:log-group:/aws/lambda/${var.domain}-${var.service_subdomain}-lambda:*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "execute-api:Invoke",
          "execute-api:ManageConnections"
        ]
        Resource = "arn:aws:execute-api:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:*",
          "s3-object-lambda:*"
        ]
        Resource = "*"
      }
    ]
  })
} 