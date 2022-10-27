output "image_uri" {
  value       = local.image_uri
  description = "ECR image used for lambda function"
}

output "lambda_function_arn" {
  value       = module.kpi_calculation_lambda.lambda_function_arn
  description = "The ARN of the Lambda Function"
}

output "lambda_cloudwatch_log_group_name" {
  value       = module.kpi_calculation_lambda.lambda_cloudwatch_log_group_name
  description = "The name of the Cloudwatch Log Group"
}

output "lambda_function_name" {
  value       = module.kpi_calculation_lambda.lambda_function_name
  description = "The name of the Lambda Function"
}

output "tags" {
  value       = local.tags
  description = "Tags attached"
}


output "aws_glue_resource_arns" {
  value       = local.aws_glue_resource_arns
  description = "AWS Glue resource arns allower permissions"
}
