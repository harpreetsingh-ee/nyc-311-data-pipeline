Here is the exact order of precedence Terraform uses (from lowest priority to highest)
1. *.tfvars (or *.tfvars.json) ← Lowest priority
2. *.auto.tfvars (or *.auto.tfvars.json)
3. TF_VAR_ environment variables
4. CLI flags (-var or -var-file) ← Highest priority