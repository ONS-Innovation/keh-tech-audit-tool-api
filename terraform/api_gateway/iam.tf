data "aws_iam_policy_document" "api_private_access" {
  statement {
    sid    = "AllowFromConfiguredVpcEndpoints"
    effect = "Allow"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = [
      "execute-api:Invoke"
    ]

    resources = [
      "${aws_api_gateway_rest_api.main.execution_arn}/*"
    ]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceVpce"
      values   = [aws_vpc_endpoint.api_gateway.id]
    }
  }
}

resource "aws_api_gateway_rest_api_policy" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  policy      = data.aws_iam_policy_document.api_private_access.json
}

data "aws_iam_policy_document" "domain_private_access" {
  statement {
    sid    = "AllowFromConfiguredVpcEndpoints"
    effect = "Allow"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = [
      "execute-api:Invoke"
    ]

    resources = [
      "arn:aws:execute-api:${var.region}:${var.aws_account_id}:/domainnames/${var.service_subdomain}.${var.domain}.${var.domain_extension}*"
    ]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceVpce"
      values   = [aws_vpc_endpoint.api_gateway.id]
    }
  }
}
