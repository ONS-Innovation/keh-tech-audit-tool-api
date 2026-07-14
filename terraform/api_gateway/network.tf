resource "aws_security_group" "apigw_vpce" {
  name        = "${var.domain}-${var.service_subdomain}-apigw-vpce-sg"
  description = "Security group for API Gateway VPC endpoint"
  vpc_id      = data.terraform_remote_state.sdp_infrastructure.outputs.vpc_id

  ingress {
    description     = "HTTPS access from the permitted ECS service"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [data.terraform_remote_state.tat_ui.outputs.security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Project       = var.project_tag
    TeamOwner     = var.team_owner_tag
    BusinessOwner = var.business_owner_tag
  }
}

resource "aws_vpc_endpoint" "api_gateway" {
  vpc_id              = data.terraform_remote_state.sdp_infrastructure.outputs.vpc_id
  service_name        = "com.amazonaws.${var.region}.execute-api"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = data.terraform_remote_state.sdp_infrastructure.outputs.private_subnets
  private_dns_enabled = true
  security_group_ids  = [aws_security_group.apigw_vpce.id]

  tags = {
    Name          = "${var.domain}-${var.service_subdomain}-execute-api-vpce"
    Project       = var.project_tag
    TeamOwner     = var.team_owner_tag
    BusinessOwner = var.business_owner_tag
  }
}
