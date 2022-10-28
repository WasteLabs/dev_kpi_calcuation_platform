output "glue_table_arns" {
  value = [
    aws_glue_catalog_table.stops.arn,
    aws_glue_catalog_table.kpi.arn,
  ]
  description = "Glue table arns"
}
