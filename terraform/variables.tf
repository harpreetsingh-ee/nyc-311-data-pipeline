# GCS VARIABLES
variable "gcs_bucket_name" {
  description = "Globally unique name of the Google Cloud Storage bucket."
  type        = string
}

variable "gcs_bucket_location" {
  description = "Location of the Google Cloud Storage bucket."
  type        = string
}

variable "gcs_bucket_object_retention_days" {
  description = "Delete bucket objects after this many days."
  type        = number
}

variable "google_project_id" {
  description = "Google Cloud project ID."
  type        = string
}

variable "google_credentials_path" {
  description = "Path to the Google Cloud service account credentials file."
  type        = string
}

variable "google_region" {
  description = "Default Google Cloud provider region."
  type        = string
}

# SNOWFLAKE VARIABLES
variable "snowflake_organization_name" {
  description = "Snowflake organization name."
  type        = string
}

variable "snowflake_account_name" {
  description = "Snowflake account name."
  type        = string
}

variable "snowflake_user" {
  description = "Snowflake user used by Terraform."
  type        = string
}

variable "snowflake_role" {
  description = "Snowflake role used by Terraform."
  type        = string
}

variable "snowflake_private_key_path" {
  description = "Path to the Snowflake private key file."
  type        = string
}

variable "snowflake_warehouse_name" {
  description = "Name of the Snowflake warehouse to use."
  type        = string
}

variable "snowflake_database_name" {
  description = "Name of the Snowflake database to create."
  type        = string
}

variable "snowflake_schema_names" {
  description = "Names of the Snowflake schemas to create."
  type        = list(string)
}

variable "snowflake_schema_prefix" {
  description = "Prefix applied to each Snowflake schema name."
  type        = string
}

variable "snowflake_table_columns" {
  description = "Column definitions for the NYC 311 Snowflake table."
  type = list(object({
    name    = string
    type    = string
    default = optional(string)
  }))
}

variable "snowflake_service_account" {
  description = "Snowflake GCS integration service account email."
  type        = string
  sensitive   = true
}

variable "snowflake_storage_integration_name" {
  description = "Name of the existing Snowflake GCS storage integration."
  type        = string
}

variable "state_encryption_key" {
  description = "Encryption key for Terraform state backend."
  type        = string
  sensitive   = true
  default     = ""
}
