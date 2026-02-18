data "terraform_remote_state" "secrets" {
  backend = "s3"
  config = {
    bucket = "${var.domain}-tf-state"
    key    = "${var.domain}-${var.service_subdomain}-secrets/terraform.tfstate"
    region = "eu-west-2"
  }
}

data "terraform_remote_state" "storage" {
  backend = "s3"
  config = {
    bucket = "${var.domain}-tf-state"
    key    = "${var.domain}-${var.service_subdomain}-storage/terraform.tfstate"
    region = "eu-west-2"
  }
}