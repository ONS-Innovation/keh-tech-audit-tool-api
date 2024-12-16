output "lambda_function_arn" {
  value = aws_lambda_function.tech_audit_lambda.arn
}

output "lambda_function_name" {
  value = aws_lambda_function.tech_audit_lambda.function_name
}

output "lambda_execution_role_arn" {
  value = aws_iam_role.lambda_execution_role.arn
} 