{% snapshot snapshot_nyc_311_service_requests %}
{{
    config(
        target_schema='HARPREET_SINGH_RAW',
        unique_key='unique_key',
        strategy='check',
        check_cols=['status', 'closed_date', 'resolution_action_updated_date']
    )
}}

select
    unique_key,
    status,
    closed_date,
    resolution_action_updated_date
from {{ source('cross_skilling_nyc_311', 'NYC_311_DATASET') }}  

{% endsnapshot %}