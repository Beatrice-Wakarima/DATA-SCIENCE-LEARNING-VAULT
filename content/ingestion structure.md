ingestion_project/
│── ingest.py              # Main pipeline (ETL flow)
│── config.py              # Configs & environment variables
│── validate.py            # Data validation rules
│── db_utils.py            # DB connection & insert helpers
│── audit.py               # Audit logs & summary reports
│── logger.py              # Logging configuration
│── tests/                 # Unit/integration tests
│── dags/                  # Airflow DAGs (if using Airflow)
│── scripts/cronjob.sh     # Cronjob for scheduling
│── logs/                  # Centralized logs

### 🔧 What You Can Include in `config.py`

|Setting|What It Means (Layman’s Terms)|
|---|---|
|`DB_NAME`|The name of the database we’re sending data to|
|`DB_USER`|The username used to log into the database|
|`DB_PASSWORD`|The password for that user (kept secret using `.env`)|
|`DB_HOST`|Where the database lives — usually `localhost` or a cloud address|
|`DB_PORT`|The door we use to connect to the database — usually `5432` for PostgreSQL|
|`CHUNK_SIZE`|How many rows we process at a time — useful for big files like `train.csv`|
|`CSV_PATH`|Where the data file is stored — like a map to find `train.csv`|
|`LOG_PATH`|Where we save logs — so we can track what happened during ingestion|
|`TABLE_NAME`|The name of the table we’re inserting data into — like `sales` or `transactions`|
|`VALID_REGIONS`|A list of allowed regions — used to check if the data is clean|
|`DASHBOARD_URL`|Where the dashboard lives — useful for linking to visual reports|