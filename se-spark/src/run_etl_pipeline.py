from pathlib import Path

from pyspark.sql import DataFrame

from nyc311.clean import clean
from nyc311.combine import combine_sources
from nyc311.config import CSV_FILE, JSON_FILE, OUTPUT_DIR, PARQUET_FILE
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
        requests = (
            combine_sources(
                ("csv", read_csv_file(spark, csv_path)),
                ("parquet", read_parquet_file(spark, parquet_path)),
                ("json", read_json_file(spark, json_path)),
            )
            .transform(clean)
            .transform(add_features)
            .transform(add_outcome)
            .transform(add_agency)
        )
        save(requests, output_dir / "requests")

        summary = summarise(read_requests(spark, output_dir))
        summary.show(10, truncate=False)
        save(summary, output_dir / "summary")
        print("Saved to", output_dir)
        return summary
    finally:
        spark.stop()


if __name__ == "__main__":
    run()
