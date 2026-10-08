from pathlib import Path
import time
from pyspark.sql import SparkSession

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "nyc311_dev.csv"


def main():
    spark = (
        SparkSession.builder.master("local[*]")
        .appName("nyc311-smoke-test")
        .getOrCreate()
    )
    print(f"Spark version: {spark.version}")
    print(f"Spark URL: {spark.sparkContext._jsc.sc().uiWebUrl()}")

    df = spark.read.csv(str(DATA_PATH), header=True, inferSchema=True)
    df.show(5)
    df.printSchema()
    # time.sleep(600) 

    spark.stop()


if __name__ == "__main__":
    main()
