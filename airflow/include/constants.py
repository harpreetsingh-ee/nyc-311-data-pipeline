"""
Simple Constants Module

All application constants in one place.
Import with: from include.constants import GCS_SOURCE_BUCKET, SNOWFLAKE_DATABASE, etc.
"""

from datetime import timedelta

# ============================================================================
# GCS Configuration
# ============================================================================
GCS_CONN_ID = "gcloud-connection2"
GCS_SOURCE_BUCKET = "nyc-311-dataset"
GCS_DESTINATION_BUCKET = "harpreet_singh_nyc311"
GCS_PREFIX = ""
GCP_PROJECT_ID = "ee-india-se-data"

# ============================================================================
# Snowflake Configuration
# ============================================================================
SNOWFLAKE_CONN_ID = "snowflake-connection2"
SNOWFLAKE_ACCOUNT = "GUSDATD-DAB70621"  # Override with env var or Astro variable
SNOWFLAKE_USER = "HARPREET.SINGH"  # Override with env var or Astro variable
SNOWFLAKE_DATABASE = "DE_CROSS_SKILLING_NYC_311"
SNOWFLAKE_SCHEMA = "HARPREET_SINGH_RAW"
SNOWFLAKE_RAW_TABLE = "NYC_311_DATASET"
SNOWFLAKE_STAGE_NAME = "HARPREET_SINGH_nyc_311_stage"
SNOWFLAKE_FILE_FORMAT = "HARPREET_SINGH_nyc_311_csv_format"
SNOWFLAKE_WAREHOUSE = "SNOWFLAKE_LEARNING_WH"
SNOWFLAKE_ROLE = "SE_DE_PARTICIPANT"

# ============================================================================
# DAG Configuration
# ============================================================================
DAG_OWNER = "data-engineering"
DAG_EMAIL_ALERTS = ["data-alerts@company.com"]
DAG_RETRIES = 2
DAG_RETRY_DELAY = timedelta(minutes=5)
DAG_SLA_HOURS = 4
DAG_MAX_ACTIVE_RUNS = 1