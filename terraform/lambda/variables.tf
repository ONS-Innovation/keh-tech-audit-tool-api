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
  description = "Domain"
  type        = string
  default     = "sdp-sandbox"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-2"
}

variable "ecr_repository" {
  description = "Name of the ECR repository containing the Lambda image"
  type        = string
}

variable "image_tag" {
  description = "Tag of the container image to deploy"
  type        = string
  default     = "latest"
}

variable "tech_audit_data_bucket_name" {
  description = "Name of the S3 bucket for tech audit data"
  type        = string
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