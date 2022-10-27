provider "aws" {
  region = var.region
}

locals {
  name = var.project_name
}



resource "aws_glue_catalog_database" "database" {
  name = local.name
}
