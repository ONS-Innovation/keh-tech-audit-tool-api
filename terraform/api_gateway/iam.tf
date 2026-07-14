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
      "${aws_api_gateway_rest_api.main.execution_arn}/*",
      "arn:aws:execute-api:${var.region}:${var.aws_account_id}:/domainnames/${aws_api_gateway_domain_name.api.domain_name}+${aws_api_gateway_domain_name.api.domain_name_id}"
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
