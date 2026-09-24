WITH source AS (
    SELECT *
    FROM {{ source('cross_skilling_nyc_311', 'NYC_311_DATASET') }}
),

incremental_records AS (
    SELECT * FROM {{ ref('incremental_311_requests') }}
),

combined AS (
    SELECT * FROM source
    UNION ALL
    SELECT * FROM incremental_records
)

SELECT 
    *
FROM combined