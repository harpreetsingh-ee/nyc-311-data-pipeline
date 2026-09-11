from airflow.decorators import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime

# Define your connection ID established in Airflow
SNOWFLAKE_CONN_ID = "snowflake-connection"
SNOWFLAKE_DATABASE = "DE_CROSS_SKILLING_NYC_311"
SNOWFLAKE_SCHEMA = "HARPREET_SINGH_RAW"
RAW_TABLE = "NYC_311_DATASET"
STAGE_NAME = "HARPREET_SINGH_nyc_311_stage"

@dag(
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["snowflake"],
)
def snowflake_stage_reader_dag():
    # 1. Execute the SHOW STAGES query and push results to XCom
    list_stages_task = SQLExecuteQueryOperator(
        task_id="list_snowflake_stages",
        conn_id=SNOWFLAKE_CONN_ID,
        sql="SHOW STAGES;",
        # do_xcom_push=True captures the multi-row metadata matrix returned by SHOW
        do_xcom_push=True,
    )

    # 2. Execute COPY INTO using the stage's file format
    @task
    def copy_data_from_stage():
        hook = SnowflakeHook(snowflake_conn_id=SNOWFLAKE_CONN_ID)
        copy_sql = f"""
            COPY INTO {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.{RAW_TABLE}
            FROM @"{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."{STAGE_NAME}"/
            FILE_FORMAT = (
                FORMAT_NAME = "{SNOWFLAKE_DATABASE}"."{SNOWFLAKE_SCHEMA}"."HARPREET_SINGH_nyc_311_csv_format"
                ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
            )
            ON_ERROR = 'CONTINUE'
            PURGE = FALSE;
        """
        result = hook.run(copy_sql)
        return result

    # 3. Process and log the stages using an Airflow TaskFlow API task
    @task
    def process_and_print_stages(stages_data):
        if not stages_data:
            print("No stages found or data format is empty.")
            return

        print(f"Total Stages Found: {len(stages_data)}")
        print("-" * 50)
        
        # In the returned matrix, column index 1 is usually 'name' and 4 is 'type'
        for stage in stages_data:
            stage_name_val = stage[1]
            stage_type = stage[4]
            print(f"Stage Name: {stage_name_val} | Type: {stage_type}")

    # 4. Print COPY result
    @task
    def print_copy_result(copy_result):
        print("\n" + "="*50)
        print("COPY INTO Result:")
        print("="*50)
        print(f"Result: {copy_result}")
        print("Data successfully copied to the raw table.")

    # Set up task dependencies and execute
    stages_output = process_and_print_stages(list_stages_task.output)
    copy_result = copy_data_from_stage()
    print_copy_result(copy_result)
snowflake_stage_reader_dag();