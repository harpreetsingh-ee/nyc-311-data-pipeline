WITH source AS (
    SELECT *
    FROM {{ ref('fct_311_service_requests') }}
)

SELECT
    borough,
    complaint_type,
    COUNT(unique_key) as total_requests,
    COUNT_IF(is_closed = TRUE) as closed_requests,
    COUNT_IF(is_closed = FALSE) as open_requests,
    AVG(resolution_hours) AS avg_resolution_hours,
FROM source
GROUP BY borough, complaint_type

