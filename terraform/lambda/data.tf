# Get the ecs infrastructure outputs from the remote state data source
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "${var.domain}-tf-state"
    key    = "${var.domain}-ecs-infra/terraform.tfstate"
    region = "eu-west-2"
  }
}
