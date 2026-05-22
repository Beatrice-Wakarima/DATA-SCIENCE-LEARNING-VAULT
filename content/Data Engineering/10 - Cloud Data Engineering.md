---
title: Cloud Data Engineering
tags: [data-engineering, cloud, aws, gcp, snowflake]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# ☁️ Cloud Data Engineering

> Cloud platforms remove the overhead of managing infrastructure, enable elastic scaling, and power the modern data stack. This note covers the essentials of AWS, GCP, and cloud-native data tools every data engineer needs.

---

## Why Cloud for Data Engineering?

```
On-Premise:                    Cloud:
  ❌ Buy expensive hardware      ✅ Pay per use
  ❌ Manage servers yourself     ✅ Managed services
  ❌ Scale takes weeks           ✅ Scale in minutes
  ❌ Single region               ✅ Global, multi-region
  ❌ You manage backups          ✅ Auto-backups built in
  ❌ High upfront cost           ✅ No upfront cost
```

---

## Major Cloud Providers

| | AWS | GCP | Azure |
|---|---|---|---|
| **Storage** | S3 | GCS | Blob Storage |
| **Warehouse** | Redshift | BigQuery | Synapse |
| **Orchestration** | MWAA (Airflow) | Cloud Composer | Data Factory |
| **Streaming** | Kinesis | Pub/Sub | Event Hubs |
| **Serverless** | Lambda | Cloud Functions | Azure Functions |
| **Container** | ECS/EKS | GKE | AKS |
| **Market share** | 33% | 11% | 22% |

---

## AWS for Data Engineers

### S3 — Object Storage

```python
# pip install boto3
import boto3
import pandas as pd
from io import StringIO, BytesIO
import os

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

BUCKET = "beatrice-data-lake"

# Upload DataFrame as Parquet to S3
def upload_parquet(df: pd.DataFrame, s3_key: str):
    """Upload DataFrame to S3 as Parquet"""
    buffer = BytesIO()
    df.to_parquet(buffer, index=False, compression="snappy")
    buffer.seek(0)
    s3.put_object(Bucket=BUCKET, Key=s3_key, Body=buffer.getvalue())
    print(f"✅ Uploaded: s3://{BUCKET}/{s3_key}")

# Download Parquet from S3
def download_parquet(s3_key: str) -> pd.DataFrame:
    """Download Parquet from S3 into DataFrame"""
    obj = s3.get_object(Bucket=BUCKET, Key=s3_key)
    return pd.read_parquet(BytesIO(obj["Body"].read()))

# List files with prefix
def list_files(prefix: str) -> list:
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
    return [obj["Key"] for obj in response.get("Contents", [])]

# Medallion Architecture on S3
upload_parquet(raw_df,   "bronze/bank_marketing/2026/05/20/data.parquet")
upload_parquet(clean_df, "silver/bank_customers/2026/05/20/data.parquet")
upload_parquet(gold_df,  "gold/campaign_performance/2026/05/20/data.parquet")
```

### Redshift — AWS Data Warehouse

```python
# Connect Python to Redshift (same as PostgreSQL)
import os
from sqlalchemy import create_engine

engine = create_engine(
    f"redshift+psycopg2://"
    f"{os.getenv('REDSHIFT_USER')}:{os.getenv('REDSHIFT_PASSWORD')}@"
    f"{os.getenv('REDSHIFT_HOST')}:5439/"
    f"{os.getenv('REDSHIFT_DB')}"
)

# Load data from S3 to Redshift (COPY is much faster than INSERT)
with engine.connect() as conn:
    conn.execute("""
        COPY silver.bank_customers
        FROM 's3://beatrice-data-lake/silver/bank_customers/2026/05/20/'
        IAM_ROLE 'arn:aws:iam::123456:role/RedshiftS3Access'
        FORMAT AS PARQUET;
    """)
```

---

## GCP for Data Engineers

### BigQuery — Serverless Data Warehouse

```python
# pip install google-cloud-bigquery
from google.cloud import bigquery
import pandas as pd
import os

# Authenticate (set GOOGLE_APPLICATION_CREDENTIALS env var)
client = bigquery.Client(project=os.getenv("GCP_PROJECT"))

# Run SQL query → DataFrame
def query_bigquery(sql: str) -> pd.DataFrame:
    """Execute BigQuery SQL and return DataFrame"""
    return client.query(sql).to_dataframe()

# Load DataFrame to BigQuery
def load_to_bigquery(df: pd.DataFrame,
                     table_id: str,
                     if_exists: str = "append") -> None:
    """Load DataFrame to BigQuery table"""
    write_disposition = {
        "append": bigquery.WriteDisposition.WRITE_APPEND,
        "replace": bigquery.WriteDisposition.WRITE_TRUNCATE,
        "fail": bigquery.WriteDisposition.WRITE_EMPTY
    }[if_exists]

    job_config = bigquery.LoadJobConfig(
        write_disposition=write_disposition,
        autodetect=True         # Auto-detect schema
    )

    job = client.load_table_from_dataframe(df, table_id,
                                            job_config=job_config)
    job.result()    # Wait for completion
    print(f"✅ Loaded {len(df):,} rows to {table_id}")

# Example queries
df = query_bigquery("""
    SELECT
        job,
        education,
        COUNT(*) AS total,
        SUM(CASE WHEN subscribed THEN 1 ELSE 0 END) AS subscriptions,
        ROUND(100 * AVG(IF(subscribed, 1, 0)), 2) AS conversion_rate
    FROM `my-project.silver.bank_customers`
    GROUP BY 1, 2
    ORDER BY conversion_rate DESC
    LIMIT 20
""")

# BigQuery is very cheap for analytics
# $5 per TB scanned — partitioning reduces cost dramatically
```

### GCS — Google Cloud Storage

```python
from google.cloud import storage

gcs = storage.Client()
bucket = gcs.bucket("beatrice-data-lake")

# Upload file
def upload_to_gcs(local_path: str, gcs_path: str):
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)
    print(f"✅ Uploaded to gs://beatrice-data-lake/{gcs_path}")

# Upload DataFrame
def upload_df_to_gcs(df: pd.DataFrame, gcs_path: str):
    from io import BytesIO
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    blob = bucket.blob(gcs_path)
    blob.upload_from_string(buffer.getvalue(),
                             content_type="application/octet-stream")
```

---

## Snowflake — Cloud Data Warehouse

```python
# pip install snowflake-connector-python snowflake-sqlalchemy
import snowflake.connector
from sqlalchemy import create_engine
import pandas as pd
import os

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),      # e.g. xy12345.eu-west-1
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
    database=os.getenv("SNOWFLAKE_DATABASE", "DATA_VAULT"),
    schema=os.getenv("SNOWFLAKE_SCHEMA", "SILVER")
)

# SQLAlchemy connection (works with pandas)
engine = create_engine(
    f"snowflake://{os.getenv('SNOWFLAKE_USER')}:"
    f"{os.getenv('SNOWFLAKE_PASSWORD')}@"
    f"{os.getenv('SNOWFLAKE_ACCOUNT')}/"
    f"{os.getenv('SNOWFLAKE_DATABASE')}/"
    f"{os.getenv('SNOWFLAKE_SCHEMA')}?"
    f"warehouse={os.getenv('SNOWFLAKE_WAREHOUSE')}"
)

# Write DataFrame to Snowflake
from snowflake.connector.pandas_tools import write_pandas

df = pd.read_csv("data/bank_marketing.csv", sep=";")
success, nchunks, nrows, _ = write_pandas(
    conn=conn,
    df=df,
    table_name="BANK_MARKETING_RAW",
    schema="BRONZE",
    auto_create_table=True,
    overwrite=True
)
print(f"✅ Loaded {nrows:,} rows to Snowflake")

# Snowflake-specific features
cursor = conn.cursor()

# Time travel — query data from 1 hour ago
cursor.execute("""
    SELECT * FROM silver.bank_customers
    AT (OFFSET => -3600)    -- 1 hour ago in seconds
""")

# Zero-copy clone — instant copy for testing
cursor.execute("""
    CREATE OR REPLACE TABLE silver.bank_customers_dev
    CLONE silver.bank_customers
""")
conn.close()
```

---

## dbt Profiles for Cloud

```yaml
# profiles.yml — multi-cloud configuration
bank_marketing:
  target: dev
  outputs:

    # Local PostgreSQL
    dev:
      type: postgres
      host: localhost
      user: beatrice
      password: "{{ env_var('DB_PASSWORD') }}"
      port: 5432
      dbname: data_vault
      schema: dbt_dev

    # Snowflake Production
    snowflake_prod:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: TRANSFORMER
      warehouse: COMPUTE_WH
      database: DATA_VAULT
      schema: SILVER
      threads: 8

    # BigQuery
    bigquery:
      type: bigquery
      method: service-account
      project: "{{ env_var('GCP_PROJECT') }}"
      dataset: silver
      keyfile: /secrets/gcp-keyfile.json
      threads: 8
      timeout_seconds: 300

    # Redshift
    redshift:
      type: redshift
      host: "{{ env_var('REDSHIFT_HOST') }}"
      user: "{{ env_var('REDSHIFT_USER') }}"
      password: "{{ env_var('REDSHIFT_PASSWORD') }}"
      port: 5439
      dbname: data_vault
      schema: silver
      threads: 4
```

---

## Infrastructure as Code — Terraform

```hcl
# main.tf — provision cloud infrastructure

# GCS bucket for data lake
resource "google_storage_bucket" "data_lake" {
  name          = "beatrice-data-lake"
  location      = "us-central1"
  force_destroy = false

  lifecycle_rule {
    condition { age = 90 }
    action { type = "SetStorageClass"; storage_class = "NEARLINE" }
  }

  lifecycle_rule {
    condition { age = 365 }
    action { type = "SetStorageClass"; storage_class = "ARCHIVE" }
  }
}

# BigQuery dataset
resource "google_bigquery_dataset" "silver" {
  dataset_id = "silver"
  location   = "US"
  description = "Cleaned data layer"
}

# S3 bucket
resource "aws_s3_bucket" "data_lake" {
  bucket = "beatrice-data-lake"
  tags = {
    Environment = "production"
    Owner       = "beatrice"
  }
}

# Redshift cluster
resource "aws_redshift_cluster" "warehouse" {
  cluster_identifier  = "beatrice-warehouse"
  database_name       = "data_vault"
  master_username     = var.redshift_user
  master_password     = var.redshift_password
  node_type           = "dc2.large"
  number_of_nodes     = 2
}
```

---

## Cost Optimisation Tips

```
BigQuery:
  ✅ Partition tables by date — only scan needed partitions
  ✅ Cluster on frequent WHERE/JOIN columns
  ✅ Use materialised views for repeated queries
  ✅ Set maximum bytes billed to avoid surprises

Snowflake:
  ✅ Auto-suspend warehouses after 60 seconds idle
  ✅ Use multi-cluster only for high concurrency
  ✅ Cluster keys on large tables for pruning
  ✅ Monitor credits with Resource Monitors

S3/GCS:
  ✅ Use Parquet/ORC over CSV (10x smaller)
  ✅ Lifecycle rules: move old data to cheaper tiers
  ✅ Intelligent tiering for unpredictable access

General:
  ✅ Schedule compute-heavy jobs in off-peak hours
  ✅ Use spot/preemptible instances for batch jobs
  ✅ Tag all resources for cost allocation
  ✅ Set billing alerts at 50%, 80%, 100% of budget
```

---

## Quick Reference

```python
# S3 (AWS)
import boto3
s3 = boto3.client("s3")
s3.put_object(Bucket="bucket", Key="path/file.parquet", Body=data)
s3.get_object(Bucket="bucket", Key="path/file.parquet")

# GCS (GCP)
from google.cloud import storage
gcs = storage.Client()
bucket = gcs.bucket("bucket")
bucket.blob("path/file.parquet").upload_from_filename("local.parquet")

# BigQuery
from google.cloud import bigquery
client = bigquery.Client()
df = client.query("SELECT ...").to_dataframe()
client.load_table_from_dataframe(df, "project.dataset.table")

# Snowflake
from snowflake.connector.pandas_tools import write_pandas
write_pandas(conn, df, "TABLE_NAME", schema="SCHEMA")
```

---

## Previous | Next
← [[09 - Monitoring and Alerting]] | → [[Data Engineering MOC]]
