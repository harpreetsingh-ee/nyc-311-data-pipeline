output "bucket_name" {
  value       = google_storage_bucket.my_bucket.name
  description = "The globally unique name of the created GCS bucket."
}

output "bucket_url" {
  value       = google_storage_bucket.my_bucket.self_link
  description = "The URL of the created GCS bucket."
}