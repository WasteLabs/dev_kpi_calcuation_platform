provider "aws" {
  region = var.region
}

locals {
  image_uri = "${data.terraform_remote_state.ecr.outputs.repository_url}:${var.build_tag}"
  env       = terraform.workspace
  tags = {
    region    = var.region
    name      = var.project_name
    env       = terraform.workspace
    image_uri = local.image_uri
  }
  s3_bucket_id          = data.terraform_remote_state.s3.outputs.s3_bucket_id
  s3_bucket_arn         = data.terraform_remote_state.s3.outputs.s3_bucket_arn
  ecr_repository_arn    = data.terraform_remote_state.ecr.outputs.repository_arn
  aws_glue_database_arn = data.terraform_remote_state.glue_database.outputs.database_arn
  aws_glue_catalog_arn  = replace(local.aws_glue_database_arn, "database/kpi_calculation_platform", "catalog")
  aws_glue_resource_arns = concat(
    [
      local.aws_glue_database_arn,
      local.aws_glue_catalog_arn,
    ],
    data.terraform_remote_state.glue_tables.outputs.glue_table_arns
  )

  iam_lambda = <<EOT
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "${local.s3_bucket_arn}",
        "${local.s3_bucket_arn}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:*"
      ],
      "Resource": [
        "${local.ecr_repository_arn}"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
          "glue:*"
      ],
      "Resource": ${jsonencode(local.aws_glue_resource_arns)}
    }
  ]
}
EOT
}


module "kpi_calculation_lambda" {
  # TODO: adjust logs
  # TODO: Configure CI/CD
  source  = "terraform-aws-modules/lambda/aws"
  version = ">= 4.2.0, < 5.0.0"

  function_name = "${var.project_name}-${local.env}"
  description   = "Lambda function performing main computation"

  create_package = false

  image_uri              = local.image_uri
  package_type           = "Image"
  memory_size            = 1024
  maximum_retry_attempts = 2
  timeout                = 40

  attach_policy_json = true
  policy_json        = local.iam_lambda

  environment_variables = {
    APP_ENV = local.env
  }

  tags = local.tags
}


resource "aws_lambda_permission" "allow_bucket_access" {
  statement_id  = "AllowExecutionFromS3Bucket${terraform.workspace}"
  action        = "lambda:InvokeFunction"
  function_name = module.kpi_calculation_lambda.lambda_function_arn
  principal     = "s3.amazonaws.com"
  source_arn    = local.s3_bucket_arn
}


resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = local.s3_bucket_id

  lambda_function {
    id                  = "${local.env}-user-stops-trigger"
    lambda_function_arn = module.kpi_calculation_lambda.lambda_function_arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "${local.env}/01_raw/user_stops/"
    filter_suffix       = ".xlsx"
  }

  depends_on = [
    aws_lambda_permission.allow_bucket_access
  ]
}
