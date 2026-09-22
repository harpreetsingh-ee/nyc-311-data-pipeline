WITH stage AS (
    SELECT
        unique_key,
        created_date,
        closed_date,
        borough,
        complaint_type,
        status
    FROM {{ ref('stg_311_service_requests') }}
),

bad_records AS (
    SELECT
        unique_key,
        created_date,
        closed_date,
        borough,
        complaint_type,
        status
    FROM {{ ref('bad_311_requests') }}
),

combined AS (
    SELECT * FROM stage
    UNION ALL
    SELECT * FROM bad_records
)

SELECT
    unique_key,
    created_date,
    closed_date,
    borough,
    complaint_type,
    status
FROM combined
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY unique_key
    ORDER BY closed_date DESC
) = 1
