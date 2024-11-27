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
  default     = "tech-audit-tool-api"
}

variable "domain" {
  description = "Domain name (e.g., sdp-dev)"
  type        = string
  default     = "sdp-dev"
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

variable "container_ver" {
  description = "Container version"
  type        = string
  default     = "v0.0.1"
}

variable "lambda_name" {
  description = "Name of the Lambda function (without environment prefix)"
  type        = string
  default     = "tech-audit-tool-api"
}

variable "ecr_repository_name" {
  description = "Name of the existing ECR repository"
  type        = string
  default     = "tech-audit-tool-api"
}