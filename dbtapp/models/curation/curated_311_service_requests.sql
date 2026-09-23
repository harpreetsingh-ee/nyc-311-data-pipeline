{{ config(
    materialized='incremental',
    unique_key='unique_key'
) }}

WITH source AS (
    SELECT *
    FROM {{ ref('stg_311_service_requests') }}
)

SELECT 
    unique_key,
    YEAR(created_date) AS created_year,
    MONTH(created_date) AS created_month,
    IFF(closed_date IS NULL OR TRIM(closed_date) = '', TRUE, FALSE) AS is_closed,
    {{ resolution_hours('created_date', 'closed_date') }} AS resolution_hours,
    IFF(resolution_hours > {{ var('resolution_hours_threshold') }}, TRUE, FALSE) AS is_long_resolution,
    agency,
    agency_name,
    borough,
    complaint_type,
    descriptor,
    status,
    created_date,
    closed_date,
    resolution_action_updated_date,
    open_data_channel_type,
    loaded_at
    ingested_at
FROM source
WHERE resolution_hours > 0
{% if is_incremental() %}
    AND loaded_at >= (
        SELECT MAX(loaded_at)
        FROM {{ this }}
    )
{% endif %}
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY unique_key
    ORDER BY ingested_at DESC
) = 1