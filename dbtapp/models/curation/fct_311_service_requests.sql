WITH source AS (
    SELECT *
    FROM {{ ref('curated_311_service_requests') }}
)

SELECT
    unique_key,
    complaint.complaint_key AS complaint_key,
    source.complaint_type AS complaint_type,
    source.descriptor AS descriptor,
    agency,
    borough,
    status,
    open_data_channel_type,
    created_date,
    closed_date,
    resolution_action_updated_date,
    created_year,
    created_month,
    is_closed,
    resolution_hours,
    ingested_at
FROM source
JOIN {{ ref('dim_311_complaint') }} AS complaint
    ON source.complaint_type = complaint.complaint_type
    AND COALESCE(source.descriptor, 'UNKNOWN') = COALESCE(complaint.descriptor, 'UNKNOWN')

