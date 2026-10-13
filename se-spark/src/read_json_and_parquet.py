from nyc311.config import JSON_FILE, PARQUET_FILE
from nyc311.ingest import read_json_file, read_parquet_file
from nyc311.spark_session import create_spark


def main() -> None:
    spark = create_spark()
    try:
        json_df = read_json_file(spark, JSON_FILE)
        print(f"JSON: {JSON_FILE.name} -> {json_df.count()} rows, {len(json_df.columns)} columns")
        json_df.printSchema()
        json_df.show(5, truncate=40)

        parquet_df = read_parquet_file(spark, PARQUET_FILE)
        print(f"Parquet: {PARQUET_FILE.name} -> {parquet_df.count()} rows, {len(parquet_df.columns)} columns")
        parquet_df.printSchema()
        parquet_df.show(5, truncate=40)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
