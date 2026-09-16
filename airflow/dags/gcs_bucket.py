"""
GCS to GCS Data Pipeline

Orchestrates the transfer of NYC 311 dataset from the public GCS bucket
to the team's dedicated GCS bucket. Includes file listing and copy validation.

Schedule: Manual trigger only
Owner: Data Engineering Team
SLA: Must complete within 4 hours

Configuration: include/constants.py
Environment: Set AIRFLOW_ENV=dev|staging|prod (default: dev)
Overrides: Use environment variables (GCS_SOURCE_BUCKET=value, etc.)
"""

import logging
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.exceptions import AirflowException

from include.constants import (
    GCS_CONN_ID,
    GCS_SOURCE_BUCKET,
    GCS_DESTINATION_BUCKET,
    GCS_PREFIX,
    DAG_OWNER,
    DAG_EMAIL_ALERTS,
    DAG_RETRIES,
    DAG_RETRY_DELAY,
    DAG_SLA_HOURS,
)

logger = logging.getLogger(__name__)


@dag(
    dag_id="gcs_bucket_reader_dag",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["gcs", "metadata", "prod"],
    description="Copy NYC 311 dataset from public GCS bucket to team bucket",
    default_args={
        "owner": DAG_OWNER,
        "retries": DAG_RETRIES,
        "retry_delay": DAG_RETRY_DELAY,
        "email": DAG_EMAIL_ALERTS,
        "email_on_failure": True,
        "email_on_retry": False,
    }
)
def gcs_bucket_reader_dag():

    @task(task_id="list_bucket_contents")
    def list_bucket_contents():
        """List all files in source GCS bucket."""
        try:
            logger.info(f"Listing files in bucket '{GCS_SOURCE_BUCKET}'")
            gcs_hook = GCSHook(gcp_conn_id=GCS_CONN_ID)
            files = gcs_hook.list(bucket_name=GCS_SOURCE_BUCKET, prefix=GCS_PREFIX)

            if not files:
                raise AirflowException(f"No files found in bucket '{GCS_SOURCE_BUCKET}'")

            logger.info(f"✓ Listed {len(files)} files in bucket '{GCS_SOURCE_BUCKET}'")
            return files
        except Exception as e:
            logger.error(f"✗ Failed to list bucket contents: {str(e)}", exc_info=True)
            raise

    @task(task_id="copy_file_to_bucket")
    def copy_file_to_bucket():
        """Sync all files from source to destination bucket."""
        try:
            logger.info(f"Starting sync: '{GCS_SOURCE_BUCKET}' → '{GCS_DESTINATION_BUCKET}'")
            logger.info("Sync parameters: recursive=True, allow_overwrite=True, delete_extra_files=False")

            gcs_hook = GCSHook(gcp_conn_id=GCS_CONN_ID)
            gcs_hook.sync(
                source_bucket=GCS_SOURCE_BUCKET,
                destination_bucket=GCS_DESTINATION_BUCKET,
                source_object=None,
                destination_object=None,
                recursive=True,
                allow_overwrite=True,
                delete_extra_files=False
            )
            logger.info(f"✓ Successfully synced files to '{GCS_DESTINATION_BUCKET}'")
        except Exception as e:
            logger.error(f"✗ GCS sync failed: {str(e)}", exc_info=True)
            raise AirflowException(f"GCS sync failed: {str(e)}")

    @task(task_id="validate_gcs_copy")
    def validate_gcs_copy(source_files):
        """Validate that all files were copied successfully."""
        try:
            logger.info("Validating GCS copy operation...")
            gcs_hook = GCSHook(gcp_conn_id=GCS_CONN_ID)
            dest_files = gcs_hook.list(bucket_name=GCS_DESTINATION_BUCKET, prefix=GCS_PREFIX)

            if not dest_files:
                raise AirflowException(f"No files found in destination bucket '{GCS_DESTINATION_BUCKET}'")

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
