"""
GCS to GCS Data Pipeline

Orchestrates the transfer of NYC 311 dataset from the public GCS bucket
to the team's dedicated GCS bucket. Includes file listing and copy validation.

Schedule: Manual trigger only
Owner: Data Engineering Team
SLA: Must complete within 4 hours
"""

import logging
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.exceptions import AirflowException

logger = logging.getLogger(__name__)

# Define your GCS constants
GCS_CONN_ID = "gcloud-connection"
SOURCE_BUCKET_NAME = "nyc-311-dataset"
DESTINATION_BUCKET_NAME = "harpreet_singh_nyc311"
PREFIX = ""


@dag(
    dag_id="gcs_bucket_reader_dag",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["gcs", "metadata", "prod"],
    owner="data-engineering",
    description="Copy NYC 311 dataset from public GCS bucket to team bucket",
    default_view="graph",
    sla=timedelta(hours=4),
    email=["data-alerts@company.com"],
    email_on_failure=True,
    email_on_retry=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    }
)
def gcs_bucket_reader_dag():

    @task(task_id="list_bucket_contents")
    def list_bucket_contents():
        """List all files in source GCS bucket."""
        try:
            logger.info(f"Listing files in bucket '{SOURCE_BUCKET_NAME}'")
            gcs_hook = GCSHook(gcp_conn_id=GCS_CONN_ID)
            files = gcs_hook.list(bucket_name=SOURCE_BUCKET_NAME, prefix=PREFIX)

            if not files:
                raise AirflowException(f"No files found in bucket '{SOURCE_BUCKET_NAME}'")

            logger.info(f"✓ Listed {len(files)} files in bucket '{SOURCE_BUCKET_NAME}'")
            return files
        except Exception as e:
            logger.error(f"✗ Failed to list bucket contents: {str(e)}", exc_info=True)
            raise

    @task(task_id="copy_file_to_bucket")
    def copy_file_to_bucket():
        """Sync all files from source to destination bucket."""
        try:
            logger.info(f"Starting sync: '{SOURCE_BUCKET_NAME}' → '{DESTINATION_BUCKET_NAME}'")
            logger.info("Sync parameters: recursive=True, allow_overwrite=True, delete_extra_files=False")

            gcs_hook = GCSHook(gcp_conn_id=GCS_CONN_ID)
            gcs_hook.sync(
                source_bucket=SOURCE_BUCKET_NAME,
                destination_bucket=DESTINATION_BUCKET_NAME,
                source_object=None,
                destination_object=None,
                recursive=True,
                allow_overwrite=True,
                delete_extra_files=False
            )
            logger.info(f"✓ Successfully synced files to '{DESTINATION_BUCKET_NAME}'")
        except Exception as e:
            logger.error(f"✗ GCS sync failed: {str(e)}", exc_info=True)
            raise AirflowException(f"GCS sync failed: {str(e)}")

    @task(task_id="validate_gcs_copy")
    def validate_gcs_copy(source_files):
        """Validate that all files were copied successfully."""
        try:
            logger.info("Validating GCS copy operation...")
            gcs_hook = GCSHook(gcp_conn_id=GCS_CONN_ID)
            dest_files = gcs_hook.list(bucket_name=DESTINATION_BUCKET_NAME, prefix=PREFIX)

            if not dest_files:
                raise AirflowException(f"No files found in destination bucket '{DESTINATION_BUCKET_NAME}'")

            if len(dest_files) < len(source_files):
                logger.warning(
                    f"File count mismatch. Source: {len(source_files)}, "
                    f"Destination: {len(dest_files)}"
                )
                raise AirflowException("Not all files were copied successfully")

            logger.info(f"✓ Validation passed: {len(dest_files)} files in destination bucket")
            return True
        except Exception as e:
            logger.error(f"✗ GCS copy validation failed: {str(e)}", exc_info=True)
            raise

    # Task dependencies
    source_files = list_bucket_contents()
    copy_result = copy_file_to_bucket()
    validate_result = validate_gcs_copy(source_files)

    source_files >> copy_result >> validate_result


gcs_bucket_reader_dag()
