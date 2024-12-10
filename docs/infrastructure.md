# Infrastructure

## AWS Resources

Before terraforming the API, you must have the API Python code containerised, using Docker, and have an elastic container registry (ECR) available.

Please refer to the [deployment](deployment.md) guide for more information.

There are **5** AWS resources that are created by the terraform script:

- Secrets Manager (Secrets)
- S3 Bucket (Storage)
- Cognito User Pool (Authentication)
- Lambda Function (Lambda)
- API Gateway (api_gateway)

Go through the list and deploy each resource one by one.

For each resource, you will need to set the `domain` and `service_subdomain` variables in the `tfvars` file.

### 1. ECR Repository

Make sure you have an ECR repository created in the AWS account. This will be used in the `S3 bucket` and `Lambda function`.

### 2. Secrets Manager

Run like normal. Leave the `cognito_pool_id`, `cognito_client_id`, `cognito_client_secret`, and `redirect_uri` variables blank. 

### 3. S3 Bucket

Set the `ecr_repository_name` variable in the `tfvars` file. Then run the terraform script.

### 4. Cognito User Pool

Run like normal.

### 5. Lambda Function

Set the `tech_audit_data_bucket_name` and `tech_audit_secrets_manager_name` variables in the `tfvars` file. Leave the `aws_cognito_token_url` variable blank. Then run the terraform script.

### 6. API Gateway

Run like normal. Note down the 

### 7. Secrets Manager Re-application

Go back to the `Secrets Manager` resource and set the `cognito_pool_id`, `cognito_client_id`, `cognito_client_secret`, and `redirect_uri` variables.

### 8. Finished

![AWS Resources](assets/explanation.png)

## Terraform Configuration

Flow chart explanation of the Terraform setup and infrastructure components.

![Infrastructure Diagram](assets/creation_flow.png)

