from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = SRC_DIR.parent / "data"

CSV_FILE = DATA_DIR / "311-service-requests-from-2010-to-present.csv"
JSON_FILE = DATA_DIR / "311-service-requests-sample-1000.jsonl"
PARQUET_FILE = DATA_DIR / "311-service-requests-from-2010-to-present.parquet"
OUTPUT_DIR = DATA_DIR / "etl_output"

SLA_HOURS = 72
REQUESTS_PARTITION_COLUMNS = ["borough", "complaint_type"]
