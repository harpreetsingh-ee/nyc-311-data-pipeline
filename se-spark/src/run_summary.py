from pathlib import Path

from pyspark.sql import DataFrame

from nyc311.config import OUTPUT_DIR
from nyc311.ingest import read_requests
from nyc311.save import save
from nyc311.spark_session import create_spark
from nyc311.summary import summarise


def run(output_dir: Path = OUTPUT_DIR) -> DataFrame:
    spark = create_spark()
    try:
        requests = read_requests(spark, output_dir);
        print(requests.count());
        summary = summarise(requests)
        summary.show(10, truncate=False)
        summary.where("borough == 'MANHATTAN'").show(10, truncate=False)
        save(summary, output_dir / "summary")
        print("Saved to", output_dir / "summary")
        return summary
    finally:
        spark.stop()


if __name__ == "__main__":
    run()
