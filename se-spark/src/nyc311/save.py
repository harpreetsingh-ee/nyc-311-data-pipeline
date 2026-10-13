"""Writing results to disk."""
from pathlib import Path

from pyspark.sql import DataFrame

from nyc311.config import PARTITION_COLUMN


def save(df: DataFrame, path: Path) -> None:
    # partitionBy makes one folder per borough (borough=BROOKLYN/, ...), so a query
    # for one borough only reads that folder.
    df.write.mode("overwrite").partitionBy(PARTITION_COLUMN).parquet(str(path))
