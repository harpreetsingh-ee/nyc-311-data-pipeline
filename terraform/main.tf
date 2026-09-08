resource "snowflake_database" "tf_db" {
  name         = var.snowflake_database_name
  is_transient = false
}

resource "google_storage_bucket" "my_bucket" {
  name     = var.gcs_bucket_name
  location = var.gcs_bucket_location
  versioning {
    enabled = true
  }
  lifecycle_rule {
    condition {
      age = var.gcs_bucket_object_retention_days
    }
    action {
      type = "Delete"
    }
  }
}