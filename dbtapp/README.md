# DBT learning

## Commands
dbt init --project-name dbt
dbt debug
dbt deps
dbt lint
dbt clean
dbt complie
dbt build
dbt snapshot
dbt seed
dbt run -s stg_311_service_requests
dbt test -s curated_311_service_requests
dbt run -s tag:incremental
dbt run -s tag:incremental --full-refresh
dbt docs generate
dbt docs serve

make sure to update ~/.dbt/profiles.yml for 
    private_key_path: '<SNOWFLAKE_RSA_KEY>.p8'
    private_key_passphrase: ""

### Incremental strategies

1. append: Inserts new records without checking for updates, deletes, or duplicates, making it ideal for append-only logs.
2. merge: Updates matching records and inserts new ones using a unique_key (similar to SCD1), though it can be costly on large tables.
3. delete+insert: Deletes rows matching a unique_key before inserting new records, serving as an alternative when merge is unsupported or keys aren't strictly unique.
4. insert_overwrite: Replaces entire partitions rather than individual rows, making it optimal for partitioned datasets in warehouses like BigQuery.
5. microbatch: Processes data in time-based chunks via an event_time column to enhance resilience for massive time-series pipelines.