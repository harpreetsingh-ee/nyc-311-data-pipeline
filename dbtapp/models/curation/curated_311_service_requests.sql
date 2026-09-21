WITH source AS (
    SELECT *
    FROM {{ ref('stg_311_service_requests') }}
)

SELECT 
    unique_key,
    YEAR(created_date) AS created_year,
    MONTH(created_date) AS created_month,
    IFF(closed_date IS NULL OR TRIM(closed_date) = '', TRUE, FALSE) AS is_closed,
    agency,
    agency_name,
    borough,
    complaint_type,
    descriptor,
    status,
    created_date,
    closed_date,
    resolution_action_updated_date,
    open_data_channel_type
FROM source
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY unique_key
    ORDER BY ingested_at DESC
) = 1