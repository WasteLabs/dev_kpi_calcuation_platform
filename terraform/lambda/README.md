<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0.8, < 2.0.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 4.26.0, <5.0.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_terraform"></a> [terraform](#provider\_terraform) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_lambda_function_container_image"></a> [lambda\_function\_container\_image](#module\_lambda\_function\_container\_image) | terraform-aws-modules/lambda/aws | >= 1.2.0, < 2.0.0 |

## Resources

| Name | Type |
|------|------|
| [terraform_remote_state.ecr](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |
| [terraform_remote_state.s3](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_project_name"></a> [project\_name](#input\_project\_name) | Project name | `string` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | Project deployment region | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_image_uri"></a> [image\_uri](#output\_image\_uri) | ECR image used for lambda function |
<!-- END_TF_DOCS -->
