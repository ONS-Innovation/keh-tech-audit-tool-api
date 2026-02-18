terraform {
  backend "s3" {
    # Backend is selected using terraform init -backend-config=path/to/backend-<env>.tfbackend
    # bucket         = "sdp-dev-tf-state"
    # key            = "sdp-dev-tech-audit-tool-dev-infra/terraform.tfstate"
    # region         = "eu-west-2"
    # dynamodb_table = "terraform-state-lock"
  }
}

# Managed policy for S3 access
resource "aws_iam_policy" "s3_access_policy" {
  name = "${var.domain}-${var.service_subdomain}-s3-access-policy"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ]
      Resource = [
        "arn:aws:s3:::${data.terraform_remote_state.storage.outputs.tech_audit_data_bucket_name}",
        "arn:aws:s3:::${data.terraform_remote_state.storage.outputs.tech_audit_data_bucket_name}/*"
      ]
    }]
  })
}

# Managed policy for Secrets Manager access
resource "aws_iam_policy" "secrets_manager_policy" {
  name = "${var.domain}-${var.service_subdomain}-secrets-manager-policy"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue"
      ]
      Resource = data.terraform_remote_state.secrets.outputs.secret_arn
    }]
  })
}

# IAM User Group
resource "aws_iam_group" "group" {
  name = "${var.domain}-${var.service_subdomain}-user-group"
  path = "/"
}

# Attach managed policies to user group
resource "aws_iam_group_policy_attachment" "group_secrets_manager_policy_attachment" {
  group = aws_iam_group.group.name
  policy_arn = aws_iam_policy.secrets_manager_policy.arn
}

resource "aws_iam_group_policy_attachment" "group_s3_access_policy_attachment" {
  group = aws_iam_group.group.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}

# IAM User
resource "aws_iam_user" "user" {
  name = "${var.domain}-${var.service_subdomain}"
  path = "/"
}

# Assign IAM User to group
resource "aws_iam_user_group_membership" "user_group_attach" {
  user = aws_iam_user.user.name

  groups = [
    aws_iam_group.group.name
  ]
}

# IAM Key Rotation Module
module "iam_key_rotation" {
  source = "git::https://github.com/ONS-Innovation/keh-aws-iam-key-rotation.git"

  iam_username          = aws_iam_user.user.name
  access_key_secret_arn = aws_secretsmanager_secret.access_key.arn
  secret_key_secret_arn = aws_secretsmanager_secret.secret_key.arn
  rotation_in_days      = 90
}