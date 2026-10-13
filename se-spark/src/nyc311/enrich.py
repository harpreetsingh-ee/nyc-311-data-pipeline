import re

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType

# Rules are checked in order and the first match wins.
OUTCOME_RULES = [
    ("DUPLICATE", r"\bduplicate\b"),
    ("NO_ACTION_NEEDED", r"no evid|no action|no violations? (?:were )?(?:issued|found|observed)"),
    ("ACTION_TAKEN", r"summons|violations? (?:were )?issued|repaired|removed|fixed|cleaned|resolved"),
    ("INFO_PROVIDED", r"see notes|additional infor|status for this request"),
]

# Known agency names; the free text varies too much for a generic "Department of ..." match.
AGENCY_PATTERN = re.compile(
    r"\b(Police Department|Fire Department|Taxi and Limousine Commission"
    r"|Department of (?:Housing Preservation and Development|Environmental? Protection|Transportation"
    r"|Sanitation|Buildings|Parks and Recreation|Health and Mental Hygiene|Consumer Affairs"
    r"|Education|Finance|Homeless Services|Information Technology and Telecommunications))",
    re.IGNORECASE,
)


def classify(text):
    """Turn a resolution sentence into a short label."""
    if text is None:
        return None
    lowered = text.lower()
    for label, pattern in OUTCOME_RULES:
        if re.search(pattern, lowered):
            return label
    return "OTHER"


def add_outcome(df: DataFrame) -> DataFrame:
    classify_udf = udf(classify, StringType())
    labels = (
        df.select("resolution_description").distinct()
          .withColumn("resolution_outcome", classify_udf(col("resolution_description")))
    )
    return df.join(labels, on="resolution_description", how="left")


def extract_agency(text):
    """Find the agency named in a resolution sentence, or None."""
    if text is None:
        return None
    match = AGENCY_PATTERN.search(text)
    if match is None:
        return None
    agency = match.group(1).replace("Environment Protection", "Environmental Protection")
    return re.sub(r"\s+", " ", agency)


def add_agency(df: DataFrame) -> DataFrame:
    extract_agency_udf = udf(extract_agency, StringType())
    agencies = (
        df.select("resolution_description").distinct()
          .withColumn("resolution_agency", extract_agency_udf(col("resolution_description")))
    )
    return df.join(agencies, on="resolution_description", how="left")
