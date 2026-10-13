from functools import reduce

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

COMBINED_PARTITION = "created_year"


def combine_sources(*sources: tuple[str, DataFrame]) -> DataFrame:
    """UNION ALL the sources, tagging each row with its source and the year of created_date (the partition column)."""
    tagged = [df.withColumn("source", F.lit(name)) for name, df in sources]
    return reduce(DataFrame.unionByName, tagged).withColumn(COMBINED_PARTITION, F.year("created_date"))
