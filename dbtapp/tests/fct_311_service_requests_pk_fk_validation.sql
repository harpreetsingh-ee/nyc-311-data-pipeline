WITH duplicate_keys AS (
    SELECT
        unique_key,
        'duplicate_primary_key' AS failure_reason
    FROM {{ ref('fct_311_service_requests') }}
    GROUP BY unique_key
    HAVING COUNT(*) > 1
),

orphaned_keys AS (
    SELECT
        fct.unique_key,
        'orphaned_foreign_key' AS failure_reason
    FROM {{ ref('fct_311_service_requests') }} AS fct
    LEFT JOIN {{ ref('dim_311_complaint') }} AS dim
        ON fct.complaint_key = dim.complaint_key
    WHERE dim.complaint_key IS NULL
)

SELECT * FROM duplicate_keys
UNION ALL
SELECT * FROM orphaned_keys
