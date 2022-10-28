output "database" {
  value       = local.name
  description = "Glue database name"
}


output "id" {
  value       = aws_glue_catalog_database.database.id
  description = "Glue database id"
}


output "database_arn" {
  value       = aws_glue_catalog_database.database.arn
  description = "Glue database arn"
}
