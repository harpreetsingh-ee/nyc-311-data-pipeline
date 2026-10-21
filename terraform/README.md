## install terraform
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

## install gcloud-cli
brew install --cask gcloud-cli
gcloud-init
gcloud auth application-default login
gcloud config set project ee-india-se-data
gcloud config set compute/region us-central1

## Commands
terraform init
terraform plan
terraform apply
terraform destroy
terraform destroy -target snowflake_database=tf_db
terraform fmt
terraform providers
terraform validate
terraform destroy -target snowflake_stage_external_gcs.stage


openssl rsa -in snowflake_rsa_key.p8 -pubout -outform DER | openssl dgst -sha256 -binary | openssl enc -base64

Here is the exact order of precedence Terraform uses (from lowest priority to highest)
1. *.tfvars (or *.tfvars.json) ← Lowest priority
2. *.auto.tfvars (or *.auto.tfvars.json)
3. TF_VAR_ environment variables
4. CLI flags (-var or -var-file) ← Highest priority