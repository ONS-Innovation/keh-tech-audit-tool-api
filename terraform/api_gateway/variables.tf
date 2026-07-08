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

variable "service_title" {
  description = "Service title"
  type        = string
  default     = "Tech Audit Tool API"
}

variable "domain" {
  description = "Domain"
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

variable "domain_extension" {
  description = "Domain extension"
  type        = string
  default     = "aws.onsdigital.uk"
}

variable "stage_name" {
  description = "Stage name for API Gateway deployment (e.g., dev, prod)"
  type        = string
  default     = "dev"
}

variable "log_retention_days" {
  description = "Log retention days"
  type        = number
  default     = 365
}

variable "internal_allowed_ip_cidrs" {
  description = "Internal CIDR ranges allowed to access the API when internal IP only WAF is enabled"
  type        = list(string)
  default     = []

  validation {
    condition     = length(var.internal_allowed_ip_cidrs) > 0 && alltrue([for cidr in var.internal_allowed_ip_cidrs : can(cidrnetmask(cidr))])
    error_message = "Set internal_allowed_ip_cidrs to at least one valid IPv4 CIDR (for example: 10.0.0.0/8)."
  }
}