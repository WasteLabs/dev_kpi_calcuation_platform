provider "aws" {
  region = var.region
}

locals {
  name           = var.project_name
  s3_bucket_name = data.terraform_remote_state.s3.outputs.s3_bucket_id
  tags = {
    region = var.region
    name   = var.project_name
    env    = terraform.workspace
  }
  env = terraform.workspace
}



resource "aws_glue_catalog_database" "database" {

  name        = local.name
  description = <<EOT
  KPI calculation platform database
EOT

}


# == ATHENA ==
resource "aws_athena_workgroup" "athena_workgroup" {
  #checkov:skip=CKV_AWS_159:Ensure that Athena Workgroup is encrypted
  name  = var.project_name
  state = "ENABLED"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${local.s3_bucket_name}/shared/02_primary/athena_workgroup_outputs/"
    }

  }

  tags = local.tags
}
