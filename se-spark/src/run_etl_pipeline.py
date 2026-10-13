from pathlib import Path

from pyspark.sql import DataFrame

from nyc311.clean import clean
from nyc311.combine import COMBINED_PARTITION, combine_sources
from nyc311.config import CSV_FILE, JSON_FILE, OUTPUT_DIR, PARQUET_FILE, REQUESTS_PARTITION_COLUMNS
from nyc311.enrich import add_agency, add_outcome
from nyc311.features import add_features
from nyc311.ingest import read_csv_file, read_json_file, read_parquet_file, read_requests
from nyc311.save import save
from nyc311.spark_session import create_spark
from nyc311.summary import summarise


def run(
    csv_path: Path = CSV_FILE,
    json_path: Path = JSON_FILE,
    parquet_path: Path = PARQUET_FILE,
    output_dir: Path = OUTPUT_DIR,
) -> DataFrame:
    spark = create_spark()
    try:
        combined = combine_sources(
            ("csv", read_csv_file(spark, csv_path)),
            ("parquet", read_parquet_file(spark, parquet_path)),
            ("json", read_json_file(spark, json_path)),
        )
        save(combined, output_dir / "combined", partition_by=COMBINED_PARTITION)  # one folder per created_date year
        requests = (
            spark.read.parquet(str(output_dir / "combined"))
            .transform(clean)
            .transform(add_features)
            .transform(add_outcome)
            .transform(add_agency)
            .repartition(*REQUESTS_PARTITION_COLUMNS)  # one task per borough/complaint_type folder
        )
        save(requests, output_dir / "requests", partition_by=REQUESTS_PARTITION_COLUMNS)  # borough=/complaint_type=

        summary = summarise(read_requests(spark, output_dir))
        save(summary, output_dir / "summary", partition_by=REQUESTS_PARTITION_COLUMNS)
        summary.show(10, truncate=False)
        print("Saved to", output_dir)
        return summary
    finally:
        spark.stop()


if __name__ == "__main__":
    run()
