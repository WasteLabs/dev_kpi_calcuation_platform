output "s3_bucket_region" {
  value       = module.s3.s3_bucket_region
  description = "The AWS region this bucket resides in."
}

output "s3_bucket_id" {
  value       = module.s3.s3_bucket_id
  description = "The name of the bucket."
}

output "s3_bucket_arn" {
  value       = module.s3.s3_bucket_arn
  description = "The ARN of the bucket. Will be of format arn:aws:s3:::bucketname."
}
