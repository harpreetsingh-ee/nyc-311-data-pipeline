"""
GCS Stage to Snowflake Data Load Pipeline

Orchestrates the loading of NYC 311 dataset from GCS stage into Snowflake.
Validates stage existence, executes COPY INTO operation, and validates load completion.

Schedule: Manual trigger only
Owner: Data Engineering Team
SLA: Must complete within 2 hours
"""

import logging
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.exceptions import AirflowException

logger = logging.getLogger(__name__)

# Define your connection ID established in Airflow
SNOWFLAKE_CONN_ID = "snowflake-connection"
SNOWFLAKE_DATABASE = "DE_CROSS_SKILLING_NYC_311"
SNOWFLAKE_SCHEMA = "HARPREET_SINGH_RAW"
RAW_TABLE = "NYC_311_DATASET"
STAGE_NAME = "HARPREET_SINGH_nyc_311_stage"
FILE_FORMAT = "HARPREET_SINGH_nyc_311_csv_format"


@dag(
    dag_id="snowflake_stage_reader_dag",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["snowflake", "prod"],
    owner="data-engineering",
    description="Load NYC 311 dataset from GCS stage to Snowflake",
    default_view="graph",
    sla=timedelta(hours=2),
    email=["data-alerts@company.com"],
    email_on_failure=True,
    email_on_retry=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    }
)
def snowflake_stage_reader_dag():

    @task(task_id="check_stage_exists")
    def check_stage_exists():
        """Verify that the required Snowflake stage exists."""
        try:
            logger.info(f"Checking if stage '{STAGE_NAME}' exists...")
            hook = SnowflakeHook(snowflake_conn_id=SNOWFLAKE_CONN_ID)

            check_sql = f"""
                SHOW STAGES LIKE '{STAGE_NAME}' IN {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA};
            """
            stages = hook.get_records(check_sql)

            if not stages:
                error_msg = (
                    f"Stage '{STAGE_NAME}' not found in "
                    f"{SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}"
                )
                logger.error(f"✗ {error_msg}")
                raise AirflowException(error_msg)

            logger.info(f"✓ Stage '{STAGE_NAME}' exists and is ready")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to check stage existence: {str(e)}", exc_info=True)
            raise AirflowException(f"Stage existence check failed: {str(e)}")

    @task(task_id="copy_data_from_stage")
    def copy_data_from_stage():
        """Copy data from Snowflake stage to raw table."""
        try:
            logger.info(f"Starting COPY INTO operation...")
            logger.info(f"Source: @{SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.{STAGE_NAME}/")
            logger.info(f"Target: {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.{RAW_TABLE}")

            hook = SnowflakeHook(snowflake_conn_id=SNOWFLAKE_CONN_ID)
            copy_sql = f"""
                COPY INTO {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.{RAW_TABLE}
                FROM @"{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."{STAGE_NAME}"/
                FILE_FORMAT = (
                    FORMAT_NAME = "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."{FILE_FORMAT}"
                    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
                )
                ON_ERROR = 'CONTINUE'
                PURGE = FALSE;
            """
            result = hook.run(copy_sql)
            logger.info(f"✓ COPY INTO operation completed")
            logger.info(f"Result: {result}")
            return result
        except Exception as e:
            logger.error(f"✗ COPY INTO operation failed: {str(e)}", exc_info=True)
            raise AirflowException(f"COPY INTO failed: {str(e)}")

    @task(task_id="validate_snowflake_load")
    def validate_snowflake_load():
        """Validate that data was loaded successfully into Snowflake."""
        try:
            logger.info("Validating Snowflake data load...")
            hook = SnowflakeHook(snowflake_conn_id=SNOWFLAKE_CONN_ID)

            # Check row count in target table
            row_count_sql = f"""
                SELECT COUNT(*) as row_count
                FROM {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.{RAW_TABLE}
            """
            result = hook.get_first(row_count_sql)
            row_count = result[0] if result else 0

            if row_count == 0:
                logger.error(f"No rows loaded into {RAW_TABLE}")
                raise AirflowException(f"Validation failed: {RAW_TABLE} is empty")

            logger.info(f"✓ Validation passed: {row_count} rows in {RAW_TABLE}")
            return row_count
        except Exception as e:
            logger.error(f"✗ Load validation failed: {str(e)}", exc_info=True)
            raise

    # Task dependencies
    stage_check = check_stage_exists()
    copy_result = copy_data_from_stage()
    validate = validate_snowflake_load()

    stage_check >> copy_result >> validate


snowflake_stage_reader_dag()