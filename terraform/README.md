# Terraform Infrastructure Management

This repository contains Terraform configurations for managing various AWS services including storage, Lambda functions, authentication, and API Gateway.

## Getting Started

### Prerequisites
- Terraform installed (version >= 1.0.0)
- AWS credentials configured
- Appropriate `.tfvars` and `.tfbackend` files in the `env/sandbox/` directory

### Directory Structure
The infrastructure is organized into separate services:
- `terraform/storage/` - S3 buckets and DynamoDB tables
- `terraform/lambda/` - Lambda functions
- `terraform/authentication/` - Cognito user pools
- `terraform/api_gateway/` - API Gateway configuration

### Common Commands

```bash
cd terraform/<storage/lambda/authentication/api_gateway> 

terraform init -backend-config=env/sandbox/backend-sandbox.tfbackend -reconfigure

terraform refresh -var-file=env/sandbox/sandbox.tfvars

terraform validate

terraform plan -var-file=env/sandbox/sandbox.tfvars

terraform apply -var-file=env/sandbox/sandbox.tfvars
```