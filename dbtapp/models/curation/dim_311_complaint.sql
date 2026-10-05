WITH source AS (
    SELECT *
    FROM {{ ref('curated_311_service_requests') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['complaint_type', 'descriptor']) }} as complaint_key,
    complaint_type,
    descriptor
FROM source
GROUP BY complaint_type, descriptor

