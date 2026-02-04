terraform {
  backend "s3" {
    # Backend is selected using terraform init -backend-config=path/to/backend-<env>.tfbackend
    # bucket         = "sdp-dev-tf-state"
    # key            = "sdp-dev-tech-audit-tool-api-lambda/terraform.tfstate"
    # region         = "eu-west-2"
    # dynamodb_table = "terraform-state-lock"
  }

}
#1. IAM Role and Security Group for Lambda
module "lambda_role_and_sg" {
  source = "git::https://github.com/ONSdigital/ons-terraform-modular.git//terraform/lambda/lambda_role_and_sg?ref=KEH-1797-shared-terraform-repo"

  domain            = var.domain
  service_subdomain = var.service_subdomain
  region            = var.region
  aws_account_id    = var.aws_account_id

  vpc_id        = data.terraform_remote_state.vpc.outputs.vpc_id
  s3_bucket_name = data.terraform_remote_state.storage.outputs.tech_audit_data_bucket_name
  secret_arn     = data.terraform_remote_state.secrets.outputs.secret_arn

  ingress_https_cidr_blocks = ["10.0.0.0/16"]

  # Optional: extra broad S3 stanza
  extra_s3_resource_arn = "arn:aws:s3:::${var.domain}-${var.service_subdomain}/*"

  tags = {
    Service = var.service_subdomain
    Domain  = var.domain
  }
}

locals {
  lambda_image_digest = var.container_digest != null ? var.container_digest : data.aws_ecr_image.lambda_image[0].image_digest
  lambda_image_uri    = "${var.aws_account_id}.dkr.ecr.${var.region}.amazonaws.com/${var.ecr_repository}@${local.lambda_image_digest}"
}

# 2. Create the Lambda function
module "tech_audit_lambda" {
  source = "git::https://github.com/ONSdigital/ons-terraform-modular.git//terraform/lambda?ref=KEH-1797-shared-terraform-repo"

  function_name = "${var.domain}-${var.service_subdomain}-lambda"
  image_uri      = local.lambda_image_uri

  role_arn  = module.lambda_role_and_sg.role_arn

  subnet_ids          = data.terraform_remote_state.vpc.outputs.private_subnets
  security_group_ids  = [module.lambda_role_and_sg.security_group_id] // Dedicated security group for Lambda function

  environment_variables = {
    TECH_AUDIT_DATA_BUCKET     = data.terraform_remote_state.storage.outputs.tech_audit_data_bucket_name
    TECH_AUDIT_SECRET_MANAGER  = data.terraform_remote_state.secrets.outputs.secret_name
    AWS_COGNITO_TOKEN_URL      = "https://${var.domain}-${var.service_subdomain}.auth.${var.region}.amazoncognito.com/oauth2/token"
    IMAGE_DIGEST               = local.lambda_image_digest
    IMAGE_TAG                  = var.container_ver
  }

  depends_on = [
    module.lambda_role_and_sg,
    data.aws_ecr_image.lambda_image
  ]
}

# Add VPC access policy to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = basename(module.lambda_role_and_sg.role_arn)
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
  depends_on = [module.lambda_role_and_sg]
}

# Resolve the pushed image (must exist before terraform apply)
data "aws_ecr_image" "lambda_image" {
  count           = var.container_digest == null ? 1 : 0
  repository_name = var.ecr_repository
  image_tag       = var.container_ver
  registry_id     = var.aws_account_id
}

# CloudWatch log group for the Lambda
resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${var.domain}-${var.service_subdomain}-lambda"
  retention_in_days = var.log_retention_days
  tags = {
    Name      = "${var.domain}-${var.service_subdomain}-lambda-log-group"
  }
}
