WITH source AS (
    SELECT *
    FROM {{ ref('curated_311_service_requests') }}
)

SELECT
    DISTINCT {{ dbt_utils.generate_surrogate_key(['complaint_type', 'descriptor']) }} as complaint_key,

    -- DISTINCT CONCAT(complaint_type, '_', COALESCE(descriptor, 'UNKNOWN')) AS complaint_key,
    complaint_type,
    descriptor
FROM source

