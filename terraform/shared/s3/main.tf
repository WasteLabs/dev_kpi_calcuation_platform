provider "aws" {
  region = var.region
}

locals {
  tags = {
    name = replace(var.project_name, "_", "-")
    env  = terraform.workspace
  }
}


module "s3" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = ">= 3.4.0, < 4.0.0"

  bucket = local.tags.name
  acl    = "private"

  versioning = {
    enabled = false
  }

  tags = local.tags
}
