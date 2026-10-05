from datetime import datetime, timedelta
from airflow import DAG;
from airflow.operators.bash import BashOperator
import base64
import os;

DBT_PROJECT_DIR = "/Users/hs086u/Documents/learning/terraform-projects/nyc-311-data-pipeline/dbtapp"
DBT_PROFILES_DIR = "/Users/hs086u/.dbt"
VENV_DIR = "/tmp/dbt_run_env"
DBT_EXECUTABLE = f"{VENV_DIR}/bin/dbt"

# 1. Get the encoded Base64 string from your .env file
encoded_key = os.getenv("DBT_ENV_SECRET_SNOWFLAKE_KEY", "")

# 2. Decode it back to the clean, original PEM text layout
if encoded_key:
    # Decodes bytes, then converts those bytes into a standard UTF-8 Python string
    decoded_key = base64.b64decode(encoded_key).decode("utf-8")
else:
    decoded_key = ""

# Passing directories into the environment so dbt knows where to look
DBT_ENV = {
    "DBT_PROJECT_DIR": "/usr/local/airflow/dbtapp",
    "DBT_PROFILES_DIR": "/home/astro/.dbt",
    "DBT_ENV_SECRET_SNOWFLAKE_KEY": decoded_key,
}

# 2. Define default arguments for your tasks
default_args = {
    "owner": "data_engineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# 3. Instantiate the DAG
with DAG(
    dag_id="dbt_build_pipeline",
    default_args=default_args,
    description="An Airflow DAG to run a monolithic dbt build",
    catchup=False,
    tags=["nyc_311"],
) as dag:

    setup_env = BashOperator(
        task_id="setup_env",
        bash_command=(
            f"python3 -m venv {VENV_DIR} && "
            f"{VENV_DIR}/bin/pip install --upgrade pip && "
            f"{VENV_DIR}/bin/pip install 'cryptography>=42.0.0,<43.0.0' && "
            f"{VENV_DIR}/bin/pip install dbt-core dbt-bigquery dbt-snowflake"
        ),
    )

    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=f"cd $DBT_PROJECT_DIR && {DBT_EXECUTABLE} deps",
        env=DBT_ENV,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=f"cd $DBT_PROJECT_DIR && {DBT_EXECUTABLE} build",
        env=DBT_ENV,
    )

    # Set dependency: Run deps first, then run build
    setup_env >> dbt_deps >> dbt_build