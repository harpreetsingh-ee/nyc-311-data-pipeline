provider "google" {
  project     = var.google_project_id
  credentials = file(var.google_credentials_path)
  region      = var.google_region
}

provider "snowflake" {
  organization_name = var.snowflake_organization_name
  account_name      = var.snowflake_account_name
  user              = var.snowflake_user
  role              = var.snowflake_role
  authenticator     = "SNOWFLAKE_JWT"
  private_key       = file(var.snowflake_private_key_path)
  warehouse         = var.snowflake_warehouse_name

  preview_features_enabled = ["snowflake_table_resource"]
}