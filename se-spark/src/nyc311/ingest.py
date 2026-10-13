import csv
from pathlib import Path
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from nyc311.schema import RAW_COLUMNS, to_snake_case

def check_header(path: Path) -> None:
    with open(path, newline="") as f:
        header = next(csv.reader(f))
    expected = [field.name for field in RAW_COLUMNS.fields]
    if header != expected:
        raise ValueError(f"CSV header does not match RAW_COLUMNS.\n  found:    {header}\n  expected: {expected}")

def read_csv_file(spark: SparkSession, path: Path) -> DataFrame:
    check_header(path)
    raw = spark.read.csv(str(path), schema=RAW_COLUMNS, header=True, escape='"')
    return raw.toDF(*[to_snake_case(field.name) for field in RAW_COLUMNS.fields])  # snake_case names


def conform(df: DataFrame) -> DataFrame:
    """Give any source the CSV's column types and snake_case names. Unparseable values become null."""
    return df.select(*[
        F.nullif(F.col(f"`{f.name}`").cast("string"), F.lit("")).try_cast(f.dataType).alias(to_snake_case(f.name))
        for f in RAW_COLUMNS.fields
    ])


def read_json_file(spark: SparkSession, path: Path) -> DataFrame:
    """Read a JSON Lines file (one object per line). Values are the CSV strings, so they are cast to RAW_COLUMNS types."""
    return conform(spark.read.json(str(path)))


def read_parquet_file(spark: SparkSession, path: Path) -> DataFrame:
    return conform(spark.read.parquet(str(path)))


def read_requests(spark: SparkSession, output_dir: Path) -> DataFrame:
    return spark.read.parquet(str(output_dir / "requests"))
