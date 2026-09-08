gcs_bucket_name                  = "harpreet_singh_nyc311"
gcs_bucket_location              = "asia-south1"
gcs_bucket_object_retention_days = 30
google_project_id                = "ee-india-se-data"
google_region                    = "us-central1"

snowflake_warehouse_name = "SNOWFLAKE_LEARNING_WH"
snowflake_database_name  = "DE_CROSS_SKILLING_NYC_311"
snowflake_schema_names   = ["raw", "currated", "consume"]
snowflake_schema_prefix  = "HARPREET_SINGH"

snowflake_table_columns = [
  { name = "UNIQUE_KEY", type = "NUMBER(38,0)" },
  { name = "CREATED_DATE", type = "VARCHAR(16777216)" },
  { name = "CLOSED_DATE", type = "VARCHAR(16777216)" },
  { name = "AGENCY", type = "VARCHAR(16777216)" },
  { name = "AGENCY_NAME", type = "VARCHAR(16777216)" },
  { name = "COMPLAINT_TYPE", type = "VARCHAR(16777216)" },
  { name = "DESCRIPTOR", type = "VARCHAR(16777216)" },
  { name = "LOCATION_TYPE", type = "VARCHAR(16777216)" },
  { name = "INCIDENT_ZIP", type = "VARCHAR(16777216)" },
  { name = "INCIDENT_ADDRESS", type = "VARCHAR(16777216)" },
  { name = "STREET_NAME", type = "VARCHAR(16777216)" },
  { name = "CROSS_STREET_1", type = "VARCHAR(16777216)" },
  { name = "CROSS_STREET_2", type = "VARCHAR(16777216)" },
  { name = "INTERSECTION_STREET_1", type = "VARCHAR(16777216)" },
  { name = "INTERSECTION_STREET_2", type = "VARCHAR(16777216)" },
  { name = "ADDRESS_TYPE", type = "VARCHAR(16777216)" },
  { name = "CITY", type = "VARCHAR(16777216)" },
  { name = "LANDMARK", type = "VARCHAR(16777216)" },
  { name = "FACILITY_TYPE", type = "VARCHAR(16777216)" },
  { name = "STATUS", type = "VARCHAR(16777216)" },
  { name = "DUE_DATE", type = "VARCHAR(16777216)" },
  { name = "RESOLUTION_DESCRIPTION", type = "VARCHAR(16777216)" },
  { name = "RESOLUTION_ACTION_UPDATED_DATE", type = "VARCHAR(16777216)" },
  { name = "COMMUNITY_BOARD", type = "VARCHAR(16777216)" },
  { name = "BOROUGH", type = "VARCHAR(16777216)" },
  { name = "X_COORDINATE", type = "NUMBER(38,0)" },
  { name = "Y_COORDINATE", type = "NUMBER(38,0)" },
  { name = "PARK_FACILITY_NAME", type = "VARCHAR(16777216)" },
  { name = "PARK_BOROUGH", type = "VARCHAR(16777216)" },
  { name = "BBL", type = "NUMBER(38,0)" },
  { name = "OPEN_DATA_CHANNEL_TYPE", type = "VARCHAR(16777216)" },
  { name = "VEHICLE_TYPE", type = "VARCHAR(16777216)" },
  { name = "TAXI_COMPANY_BOROUGH", type = "VARCHAR(16777216)" },
  { name = "TAXI_PICKUP_LOCATION", type = "VARCHAR(16777216)" },
  { name = "BRIDGE_HIGHWAY_NAME", type = "VARCHAR(16777216)" },
  { name = "BRIDGE_HIGHWAY_DIRECTION", type = "VARCHAR(16777216)" },
  { name = "ROAD_RAMP", type = "VARCHAR(16777216)" },
  { name = "BRIDGE_HIGHWAY_SEGMENT", type = "VARCHAR(16777216)" },
  { name = "LATITUDE", type = "FLOAT" },
  { name = "LONGITUDE", type = "FLOAT" },
  { name = "LOCATION", type = "VARCHAR(16777216)" },
  { name = "LOADED_AT", type = "TIMESTAMP_NTZ", default = "CURRENT_TIMESTAMP()" },
]