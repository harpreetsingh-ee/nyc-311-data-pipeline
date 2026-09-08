provider "snowflake" {
  organization_name = "GUSDATD"
  account_name      = "DAB70621"
  user              = "HARPREET.SINGH"
  role              = "SE_DE_PARTICIPANT"
  authenticator     = "SNOWFLAKE_JWT"
  private_key       = file("./keys/snowflake_rsa_key.p8")
}

provider "google" {
  project     = "ee-india-se-data"
  credentials = file("./keys/ee-india-se-data-01d41119c96e.json")
  region      = "us-central1"
}