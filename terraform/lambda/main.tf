provider "aws" {
  region = var.region
}

locals {
  image_uri = "${data.terraform_remote_state.ecr.outputs.repository_url}:latest"
  tags = {
    region    = var.region
    name      = var.project_name
    env       = terraform.workspace
    image_uri = local.image_uri
  }
  s3_bucket_arn      = data.terraform_remote_state.s3.outputs.s3_bucket_arn
  ecr_repository_arn = data.terraform_remote_state.ecr.outputs.repository_arn

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
      "Resource": [
        "*"
      ]
    }
  ]
}
EOT
}


module "lambda_function_container_image" {
  # TODO: configure triggers
  source  = "terraform-aws-modules/lambda/aws"
  version = ">= 1.2.0, < 2.0.0"

  function_name = var.project_name
  description   = "Lambda function performing main computation"

  create_package = false

  image_uri              = local.image_uri
  package_type           = "Image"
  memory_size            = 2048
  maximum_retry_attempts = 2
  timeout                = 20

  attach_policy_json = true
  policy_json        = local.iam_lambda

  tags = local.tags
}
