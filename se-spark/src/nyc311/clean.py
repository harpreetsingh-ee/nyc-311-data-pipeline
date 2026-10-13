from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.functions import col


def clean(df: DataFrame) -> DataFrame:
    df = df.filter(col("unique_key").isNotNull() & col("created_date").isNotNull())
    df = df.withColumn("borough", F.upper(F.trim(col("borough"))))
    df = df.fillna({"borough": "UNSPECIFIED"})
    return df.dropDuplicates(["unique_key"]) 
