from functools import reduce

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def combine_sources(*sources: tuple[str, DataFrame]) -> DataFrame:
    """UNION ALL the sources, tagging each row with the source it came from. Duplicates are kept."""
    tagged = [df.withColumn("source", F.lit(name)) for name, df in sources]
    return reduce(DataFrame.unionByName, tagged)
