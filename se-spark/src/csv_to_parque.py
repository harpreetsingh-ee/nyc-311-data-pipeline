from pyspark.sql import SparkSession
from pathlib import Path

DATA_PATH = Path.cwd() / "data"
# 1. Initialize SparkSession
spark = SparkSession.builder \
    .appName("CSV to Parquet") \
    .getOrCreate()

# 2. Read the CSV file
df = spark.read.csv(str(DATA_PATH / "311-service-requests-from-2010-to-present.csv"), header=True, inferSchema=True)

# 3. Write to Parquet format
df.write.parquet(str(DATA_PATH / "311-service-requests-from-2010-to-present.parquet"))

spark.stop()