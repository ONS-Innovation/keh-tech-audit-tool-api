output "lambda_function_arn" {
  value = module.tech_audit_lambda.lambda_function_arn
}

output "lambda_function_name" {
  value = module.tech_audit_lambda.lambda_function_name
}

output "lambda_execution_role_arn" {
  value = module.lambda_role_and_sg.role_arn
} 

output "lambda_image_uri" {
  description = "ECR image URI (including digest) used by the Lambda function"
  value       = local.lambda_image_uri
}