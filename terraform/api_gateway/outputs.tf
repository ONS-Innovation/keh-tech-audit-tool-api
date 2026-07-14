output "api_gateway_id" {
  description = "ID of the API Gateway REST API"
  value       = aws_api_gateway_rest_api.main.id
}

output "api_gateway_stage_name" {
  description = "Name of the API Gateway stage"
  value       = aws_api_gateway_stage.main.stage_name
}

output "api_gateway_invoke_url" {
  description = "Invoke URL for the API Gateway stage"
  value       = aws_api_gateway_stage.main.invoke_url
}

output "api_gateway_vpc_endpoint_id" {
  description = "VPC endpoint ID used to access the private API"
  value       = aws_vpc_endpoint.api_gateway.id
}

output "api_gateway_private_dns_invoke_url" {
  description = "Private DNS invoke URL for the private API"
  value       = "https://${aws_api_gateway_rest_api.main.id}.execute-api.${var.region}.amazonaws.com/${aws_api_gateway_stage.main.stage_name}"
}

output "api_gateway_vpce_invoke_url" {
  description = "VPC endpoint-specific invoke URL for the private API"
  value       = "https://${aws_api_gateway_rest_api.main.id}-${aws_vpc_endpoint.api_gateway.id}.execute-api.${var.region}.amazonaws.com/${aws_api_gateway_stage.main.stage_name}"
}

output "api_custom_domain_url" {
  description = "Stable private custom domain URL for the API"
  value       = "https://${aws_api_gateway_domain_name.api.domain_name}"
}

output "api_gateway_execution_arn" {
  description = "Execution ARN of the API Gateway"
  value       = aws_api_gateway_rest_api.main.execution_arn
}

output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch Log Group for API Gateway errors"
  value       = aws_cloudwatch_log_group.api_gateway.name
}