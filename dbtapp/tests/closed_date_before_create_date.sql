SELECT 
    unique_key
FROM {{ ref('curated_311_service_requests') }}
WHERE closed_date < created_date