"""Starting Spark."""
import os

from pyspark.sql import SparkSession

from nyc311.config import SRC_DIR


def create_spark() -> SparkSession:
    os.environ["PYTHONPATH"] = os.pathsep.join(filter(None, [str(SRC_DIR), os.environ.get("PYTHONPATH")]))
    spark = (
        SparkSession.builder.master("local[*]")
        .appName("nyc311-etl")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.session.timeZone", "America/New_York")  # the CSV times are New York times
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark
