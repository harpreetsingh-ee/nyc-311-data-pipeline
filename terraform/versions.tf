terraform {
  required_version = ">= 1.0.0"
  required_providers {
    snowflake = {
      source = "snowflakedb/snowflake"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 8.0"
    }
  }
}