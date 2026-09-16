output "bucket_name" {
  value       = google_storage_bucket.my_bucket.name
  description = "The globally unique name of the created GCS bucket."
}

output "bucket_url" {
  value       = google_storage_bucket.my_bucket.self_link
  description = "The URL of the created GCS bucket."
}

output "bucket_self_link" {
  value       = google_storage_bucket.my_bucket.self_link
  description = "The self link of the created GCS bucket."
}

output "snowflake_storage_integration_name" {
  value       = var.snowflake_storage_integration_name
  description = "The name of the Snowflake GCS storage integration."
}

output "snowflake_database_name" {
  value       = var.snowflake_database_name
  description = "The name of the Snowflake database."
}

output "snowflake_schema_names" {
  value       = [for s in snowflake_schema.schema : s.name]
  description = "The names of the created Snowflake schemas."
}

output "snowflake_table_name" {
  value       = snowflake_table.table.fully_qualified_name
  description = "The fully qualified name of the NYC 311 Snowflake table."
}

output "snowflake_file_format_name" {
  value       = snowflake_file_format_csv.complete.fully_qualified_name
  description = "The fully qualified name of the CSV file format."
}

output "snowflake_stage_name" {
  value       = snowflake_stage_external_gcs.stage.fully_qualified_name
  description = "The fully qualified name of the created Snowflake stage."
}

output "snowflake_pipe_name" {
  value       = snowflake_pipe.pipe_with_stage.fully_qualified_name
  description = "The fully qualified name of the Snowflake pipe for data ingestion."
}