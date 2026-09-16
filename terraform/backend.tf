terraform {
  backend "gcs" {
    bucket = "ee-india-se-data-tf-state"
    prefix = "harpreet_singh_nyc-311-data-pipeline"
    # Uncomment below and set TF_BACKEND_GCS_ENCRYPTION_KEY env var for encryption
    # encryption_key = var.state_encryption_key
  }
  # Note: GCS bucket backend encryption can also be configured at the GCS bucket level
  # Enable Customer-Managed Encryption Keys (CMEK) in GCS bucket settings for additional security
}

# GCS Backend Requirements:
# - Bucket: ee-india-se-data-tf-state must have versioning enabled
# - Enable object versioning on the bucket for state recovery
# - Consider enabling uniform bucket-level access for security
# - Enable audit logging for state file access
# - Use service account with minimal permissions (storage.buckets.get, storage.objects.*)
# - Optionally enable CMEK (Customer-Managed Encryption Keys) at bucket level