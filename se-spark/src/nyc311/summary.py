"""The final table: one row per borough + complaint type."""
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.functions import col


def summarise(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("borough", "complaint_type")
          .agg(
              F.count("*").alias("request_count"),
              F.sum(col("is_open").cast("int")).alias("open_count"),
              F.round(F.avg("resolution_hours"), 2).alias("avg_resolution_hours"),
              F.round(F.avg(col("closed_within_sla").cast("int")), 3).alias("sla_rate"),
              F.sum((col("resolution_outcome") == "ACTION_TAKEN").cast("int")).alias("action_taken_count"),
          )
          .orderBy("borough", F.desc("request_count"))
    )
