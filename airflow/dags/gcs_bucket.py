from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.google.cloud.operators.gcs import GCSSynchronizeBucketsOperator

# Define your GCS constants
GCS_CONN_ID = "gcloud-connection"  # The connection ID you configured
SOURCE_BUCKET_NAME = "nyc-311-dataset"
DESTINATION_BUCKET_NAME = "harpreet_singh_nyc311"
PREFIX = ""  # Optional: only list files inside this folder path

@dag(
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["gcs", "metadata"],
)
def gcs_bucket_reader_dag():

    @task
    def list_bucket_contents():
        # Initialize the GCS Hook
        gcs_hook = GCSHook(gcp_conn_id=GCS_CONN_ID)        
        files = gcs_hook.list(bucket_name=SOURCE_BUCKET_NAME, prefix=PREFIX)
        
        print(f"--- Total files found in bucket '{SOURCE_BUCKET_NAME}' --- Count: '{len(files)}'")        
        return files

    @task
    def copy_file_to_bucket():
        gcs_hook = GCSHook(gcp_conn_id=GCS_CONN_ID)
        
        list_bucket_contents();
        
        gcs_hook.sync(
            source_bucket=SOURCE_BUCKET_NAME,
            destination_bucket=DESTINATION_BUCKET_NAME,
            source_object=None,   
            destination_object=None,
            recursive=True,      
            allow_overwrite=True,   
            delete_extra_files=False
        )
    copy_file_to_bucket();

gcs_bucket_reader_dag()
