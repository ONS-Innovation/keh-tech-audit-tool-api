variable "aws_account_id" {
  description = "AWS Account ID"
  type        = string
}

variable "aws_access_key_id" {
  description = "AWS Access Key ID"
  type        = string
}

variable "aws_secret_access_key" {
  description = "AWS Secret Access Key"
  type        = string
}

variable "service_subdomain" {
  description = "Service subdomain"
  type        = string
  default     = "tech-audit-tool-api-test"
}

variable "api_name" {
  description = "API name"
  type        = string
  default     = "tech-audit-tool-api-test"
}

variable "service_title" {
  description = "Service title"
  type        = string
  default     = "Tech Audit Tool API"
}

variable "domain" {
  description = "Domain"
  type        = string
  default     = "sdp-sandbox"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-2"
}

variable "project_tag" {
  description = "Project"
  type        = string
  default     = "TAT"
}

variable "team_owner_tag" {
  description = "Team Owner"
  type        = string
  default     = "Knowledge Exchange Hub"
}

variable "business_owner_tag" {
  description = "Business Owner"
  type        = string
  default     = "DST"
}

variable "domain_extension" {
  description = "Domain extension"
  type        = string
  default     = "aws.onsdigital.uk"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function to integrate with API Gateway"
  type        = string
}

variable "lambda_function_invoke_arn" {
  description = "Full ARN of the Lambda function (e.g., arn:aws:lambda:REGION:ACCOUNT:function:FUNCTION_NAME)"
  type        = string
}

variable "cognito_user_pool_arn" {
  description = "ARN of the Cognito User Pool for API authorization"
  type        = string
}

variable "stage_name" {
  description = "Stage name for API Gateway deployment (e.g., dev, prod)"
  type        = string
  default     = "dev"
}