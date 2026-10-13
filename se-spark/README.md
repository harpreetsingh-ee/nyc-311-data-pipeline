# Dataset
https://www.kaggle.com/datasets/new-york-city/ny-311-service-requests?resource=download

# Apache Spark Architecture

```mermaid
flowchart LR
    APP["Application"] --> SC
    subgraph D["Driver"]
        SC["SparkContext"]
    end
    SC <--> CM["Cluster Manager"]
    CM --> W1["Worker<br/>(Executor)"]
    CM --> W2["Worker<br/>(Executor)"]
    CM --> W3["Worker<br/>(Executor)"]
    W1 & W2 & W3 <--> S[("Storage")]
```

- **Driver**: plans the job and schedules tasks.
- **SparkContext**: the Driver's connection to the cluster; creates jobs and talks to the Cluster Manager.
- **Cluster Manager**: allocates resources (Standalone, YARN, Kubernetes).
- **Workers / Executors**: run tasks in parallel and cache data.
- **Storage**: HDFS, S3, Parquet, databases, etc.
