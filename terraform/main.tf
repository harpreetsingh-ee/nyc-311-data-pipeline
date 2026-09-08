resource "snowflake_database" "tf_db" {
  name         = "TF_DEMO_DB"
  is_transient = false
}

resource "google_storage_bucket" "my_bucket" {
  name     = "harpreet_singh_nyc311"
  location = "asia-south1"
  versioning {
    enabled = true
  }
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}