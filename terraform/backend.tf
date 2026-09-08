terraform {
  backend "gcs" {
    bucket = "ee-india-se-data-tf-state"
    prefix = "harpreet_singh_nyc-311-data-pipeline"
  }
}