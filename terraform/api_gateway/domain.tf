data "aws_route53_zone" "domain" {
  name = "${var.domain}.${var.domain_extension}"
}

resource "aws_acm_certificate" "cert" {
  domain_name       = "${var.service_subdomain}.${var.domain}.${var.domain_extension}"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.domain.zone_id
}

resource "aws_acm_certificate_validation" "cert_validation" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}

resource "aws_api_gateway_domain_name" "api" {
  domain_name     = "${var.service_subdomain}.${var.domain}.${var.domain_extension}"
  certificate_arn = aws_acm_certificate_validation.cert_validation.certificate_arn
  policy          = data.aws_iam_policy_document.domain_private_access.json

  endpoint_configuration {
    types           = ["PRIVATE"]
    ip_address_type = "dualstack"
  }

  lifecycle {
    ignore_changes = [policy]
  }
}

resource "aws_api_gateway_domain_name_access_association" "api" {
  access_association_source      = aws_vpc_endpoint.api_gateway.id
  access_association_source_type = "VPCE"
  domain_name_arn                = aws_api_gateway_domain_name.api.arn
}

resource "aws_api_gateway_base_path_mapping" "api" {
  api_id         = aws_api_gateway_rest_api.main.id
  stage_name     = aws_api_gateway_stage.main.stage_name
  domain_name    = aws_api_gateway_domain_name.api.domain_name
  domain_name_id = aws_api_gateway_domain_name.api.domain_name_id
}

resource "aws_route53_record" "api" {
  name    = aws_api_gateway_domain_name.api.domain_name
  type    = "CNAME"
  zone_id = data.aws_route53_zone.domain.zone_id
  ttl     = 60
  records = [aws_vpc_endpoint.api_gateway.dns_entry[0].dns_name]
}
