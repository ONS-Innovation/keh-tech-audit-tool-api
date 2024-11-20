# Terraform Infrastructure Management

This repository contains Terraform configurations for managing various AWS services including storage, Lambda functions, authentication, API Gateway and CloudWatch.

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

### Authentication

You must create the Cognito user pool (authentication) then create the API Gateway (api_gateway) then define the `cognito_user_pool_arn` and `lambda_function_invoke_arn` variables in the `api_gateway` directory.

Once you have setup all the services, you must configure the redirect URLs in the Cognito user pool to point to the API Gateway endpoint.

Go to your [user pools](https://eu-west-2.console.aws.amazon.com/cognito/v2/idp/user-pools?region=eu-west-2) and click on the user pool you created.

Follow these steps:

1. Click on the `App Integrations` tab.
2. Scroll down to `App clients and analytics` and click on your App client.
3. Scroll down to `Hosted UI` and click on the `Edit` button.
4. Click `Add another URL` and add the redirect URLs to the `Callback URLs`. These will be the URLs of the API Gateway endpoint. For example: 
    - https://tech-audit-tool-api-test.sdp-sandbox.aws.onsdigital.uk
    - https://0123456789.execute-api.eu-west-2.amazonaws.com/dev
5. Click `Save changes`.


# Secrets and Environments

The app in aws_lambda_script uses environment variables set in the Dockerfile.