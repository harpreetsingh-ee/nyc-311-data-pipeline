"""Writing results to disk."""
from pathlib import Path

from pyspark.sql import DataFrame


def save(df: DataFrame, path: Path, partition_by: str | list[str] | None = None) -> None:
    # partitionBy makes one folder per value (e.g. borough=BROOKLYN/), so a query
    # for one value only reads that folder. Without it the output is not partitioned.
    writer = df.write.mode("overwrite")
    if partition_by:
        writer = writer.partitionBy(*([partition_by] if isinstance(partition_by, str) else partition_by))
    writer.parquet(str(path))
