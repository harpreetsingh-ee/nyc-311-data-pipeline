# GCS RESOURCES: create bucket and set retention policy
resource "google_storage_bucket" "my_bucket" {
  name     = var.gcs_bucket_name
  location = var.gcs_bucket_location

  versioning {
    enabled = true
  }

  # Delete objects after retention period
  lifecycle_rule {
    condition {
      age = var.gcs_bucket_object_retention_days
    }
    action {
      type = "Delete"
    }
  }

  # Clean up old versions of objects (keep only 5 most recent non-live versions)
  lifecycle_rule {
    condition {
      num_newer_versions = 5
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_storage_bucket_iam_member" "snowflake_reader" {
  bucket = google_storage_bucket.my_bucket.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${var.snowflake_service_account}"
}

# SNOWFLAKE RESOURCES: Schemas
resource "snowflake_schema" "schema" {
  for_each = toset(var.snowflake_schema_names)

  database                    = var.snowflake_database_name
  name                        = "${var.snowflake_schema_prefix}_${upper(each.value)}"
  with_managed_access         = true
  data_retention_time_in_days = 30
}

resource "snowflake_table" "table" {
  database                    = var.snowflake_database_name
  schema                      = snowflake_schema.schema[var.snowflake_schema_names[0]].name
  name                        = "NYC_311_DATASET"
  comment                     = "NYC_311_DATASET"
  data_retention_time_in_days = 30
  change_tracking             = false

  dynamic "column" {
    for_each = var.snowflake_table_columns

    content {
      name = column.value.name
      type = column.value.type

      dynamic "default" {
        for_each = column.value.default == null ? [] : [column.value.default]

        content {
          expression = default.value
        }
      }
    }
  }
}

resource "snowflake_file_format_csv" "complete" {
  name     = "${var.snowflake_schema_prefix}_nyc_311_csv_format"
  database = var.snowflake_database_name
  schema   = snowflake_schema.schema[var.snowflake_schema_names[0]].name

  skip_header                  = 1
  field_optionally_enclosed_by = "\""
  null_if                      = ["NULL", "", "N/A"]
  field_delimiter              = ","
  date_format                  = "YYYY-MM-DD"
  timestamp_format             = "YYYY-MM-DD HH24:MI:SS"
  escape_unenclosed_field      = "NONE"
  trim_space                   = true
  empty_field_as_null          = true
}

resource "snowflake_stage_external_gcs" "stage" {
  name                = "${var.snowflake_schema_prefix}_nyc_311_stage"
  url                 = "gcs://${google_storage_bucket.my_bucket.name}/"
  database            = var.snowflake_database_name
  schema              = snowflake_schema.schema[var.snowflake_schema_names[0]].name
  storage_integration = var.snowflake_storage_integration_name
  file_format {
    format_name = snowflake_file_format_csv.complete.fully_qualified_name
  }
}

resource "snowflake_pipe" "pipe_with_stage" {
  name     = "${var.snowflake_schema_prefix}_nyc_311_pipe"
  database = var.snowflake_database_name
  schema   = snowflake_schema.schema[var.snowflake_schema_names[0]].name

  # integration = snowflake_stage_external_gcs.stage.storage_integration

  copy_statement = <<-SQL
    COPY INTO ${snowflake_table.table.fully_qualified_name}
    FROM @${snowflake_stage_external_gcs.stage.fully_qualified_name}/
    FILE_FORMAT = (
      FORMAT_NAME = ${snowflake_file_format_csv.complete.fully_qualified_name},
      ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
    )
    ON_ERROR = 'CONTINUE'
  SQL

  # lifecycle {
  #   replace_triggered_by = [
  #     snowflake_stage_external_gcs.stage.url,
  #     snowflake_stage_external_gcs.stage.storage_integration,
  #   ]
  # }
}