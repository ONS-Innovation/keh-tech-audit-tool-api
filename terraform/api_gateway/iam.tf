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
      "execute-api:/*"
    ]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceVpce"
      values   = [aws_vpc_endpoint.api_gateway.id]
    }
  }
}
