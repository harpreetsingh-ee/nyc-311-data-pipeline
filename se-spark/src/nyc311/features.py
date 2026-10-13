"""New columns calculated from existing ones."""
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.functions import col

from nyc311.config import SLA_HOURS


def add_features(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("resolution_hours",
                      (col("closed_date").cast("long") - col("created_date").cast("long")) / 3600)
          .withColumn("closed_within_sla", col("resolution_hours") <= SLA_HOURS)
          .withColumn("is_open", ~((col("status") == "Closed") & col("closed_date").isNotNull()))
          .withColumn("created_hour", F.hour("created_date"))
          .withColumn("created_day_name", F.date_format("created_date", "EEEE"))
    )
