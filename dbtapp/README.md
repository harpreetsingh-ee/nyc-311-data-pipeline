# DBT learning

Incremental strategies

1. append: Inserts new records without checking for updates, deletes, or duplicates, making it ideal for append-only logs.
2. merge: Updates matching records and inserts new ones using a unique_key (similar to SCD1), though it can be costly on large tables.
3. delete+insert: Deletes rows matching a unique_key before inserting new records, serving as an alternative when merge is unsupported or keys aren't strictly unique.
4. insert_overwrite: Replaces entire partitions rather than individual rows, making it optimal for partitioned datasets in warehouses like BigQuery.
5. microbatch: Processes data in time-based chunks via an event_time column to enhance resilience for massive time-series pipelines.