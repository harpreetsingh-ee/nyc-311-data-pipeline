import re

from pyspark.sql.types import (
    DoubleType, IntegerType, LongType, StringType, StructField, StructType, TimestampType,
)

# CSV header names
RAW_COLUMNS = StructType([
    StructField("Unique Key", IntegerType()),
    StructField("Created Date", TimestampType()),
    StructField("Closed Date", TimestampType()),
    StructField("Agency", StringType()),
    StructField("Agency Name", StringType()),
    StructField("Complaint Type", StringType()),
    StructField("Descriptor", StringType()),
    StructField("Location Type", StringType()),
    StructField("Incident Zip", StringType()),
    StructField("Incident Address", StringType()),
    StructField("Street Name", StringType()),
    StructField("Cross Street 1", StringType()),
    StructField("Cross Street 2", StringType()),
    StructField("Intersection Street 1", StringType()),
    StructField("Intersection Street 2", StringType()),
    StructField("Address Type", StringType()),
    StructField("City", StringType()),
    StructField("Landmark", StringType()),
    StructField("Facility Type", StringType()),
    StructField("Status", StringType()),
    StructField("Due Date", TimestampType()),
    StructField("Resolution Description", StringType()),
    StructField("Resolution Action Updated Date", TimestampType()),
    StructField("Community Board", StringType()),
    StructField("BBL", LongType()),
    StructField("Borough", StringType()),
    StructField("X Coordinate (State Plane)", IntegerType()),
    StructField("Y Coordinate (State Plane)", IntegerType()),
    StructField("Open Data Channel Type", StringType()),
    StructField("Park Facility Name", StringType()),
    StructField("Park Borough", StringType()),
    StructField("Vehicle Type", StringType()),
    StructField("Taxi Company Borough", StringType()),
    StructField("Taxi Pick Up Location", StringType()),
    StructField("Bridge Highway Name", StringType()),
    StructField("Bridge Highway Direction", StringType()),
    StructField("Road Ramp", StringType()),
    StructField("Bridge Highway Segment", StringType()),
    StructField("Latitude", DoubleType()),
    StructField("Longitude", DoubleType()),
    StructField("Location", StringType()),
    StructField("Zip Codes", StringType()),
    StructField("Community Districts", StringType()),
    StructField("Borough Boundaries", StringType()),
    StructField("City Council Districts", IntegerType()),
    StructField("Police Precincts", IntegerType()),
])


def to_snake_case(name: str) -> str:
    return re.sub(r"[^0-9a-z]+", "_", name.strip().lower()).strip("_")
