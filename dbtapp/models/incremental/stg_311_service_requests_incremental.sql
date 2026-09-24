WITH source AS (
    SELECT *
    FROM {{ ref('raw_311_service_requests_incremental') }}
)

{% set source_rel = source('cross_skilling_nyc_311', 'NYC_311_DATASET') %}
{% set column_rename_map = convert_to_snake_case(source_rel) %}

SELECT 
    {{ dbt_utils.star(
        from=source_rel,
        rename=column_rename_map,
        except=["resolution_action_updated_date", "created_date", "closed_date", "due_date", "borough"]
    ) }},

    INITCAP(TRIM(borough)) AS borough,
    
    TRY_TO_TIMESTAMP_NTZ(resolution_action_updated_date, 'YYYY-MM-DD HH24:MI:SS "UTC"') AS resolution_action_updated_date,
    TRY_TO_TIMESTAMP_NTZ(created_date, 'YYYY-MM-DD HH24:MI:SS "UTC"') AS created_date,
    TRY_TO_TIMESTAMP_NTZ(closed_date, 'YYYY-MM-DD HH24:MI:SS "UTC"') AS closed_date,
    TRY_TO_TIMESTAMP_NTZ(due_date, 'YYYY-MM-DD HH24:MI:SS "UTC"') AS due_date,
    CURRENT_TIMESTAMP()::TIMESTAMP_NTZ AS ingested_at
FROM source
{% if is_incremental() %}
    WHERE loaded_at >= (
        SELECT MAX(loaded_at)
        FROM {{ this }}
    )
{% endif %}