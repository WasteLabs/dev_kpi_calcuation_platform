provider "aws" {
  region = var.region
}

locals {
  tags = {
    region = var.region
    name   = var.project_name
    env    = terraform.workspace
  }
}


module "ecr" {
  source  = "terraform-aws-modules/ecr/aws"
  version = ">= 1.4.0, < 2.0.0"

  repository_name = var.project_name
  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep last 100 images",
        selection = {
          tagStatus     = "tagged",
          tagPrefixList = ["v"],
          countType     = "imageCountMoreThan",
          countNumber   = 100
        },
        action = {
          type = "expire"
        }
      }
    ]
  })

  tags = local.tags
}
