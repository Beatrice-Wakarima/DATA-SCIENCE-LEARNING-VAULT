---
title: Docker for PostgreSQL
tags: [docker, postgresql, databases, data-engineering]
created: 2026-05-20
up:: [[Docker MOC]]
---

# 🐘 Docker for PostgreSQL

> Running PostgreSQL in Docker eliminates installation headaches, enables multiple versions simultaneously, and makes database environments perfectly reproducible. Every data engineer needs this.

---

## Quick Start

```bash
# Run PostgreSQL in seconds — no installation needed!
docker run -d \
  --name my-postgres \
  -e POSTGRES_USER=beatrice \
  -e POSTGRES_PASSWORD=secret123 \
  -e POSTGRES_DB=data_vault \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15

# Connect immediately
docker exec -it my-postgres psql -U beatrice -d data_vault

# Or from host using psql (if installed)
psql -h localhost -U beatrice -d data_vault
```

---

## PostgreSQL Environment Variables

```yaml
environment:
  POSTGRES_USER: beatrice           # Superuser username
  POSTGRES_PASSWORD: secret123      # Superuser password
  POSTGRES_DB: data_vault           # Default database
  POSTGRES_HOST_AUTH_METHOD: trust  # No password (dev only!)
  PGDATA: /var/lib/postgresql/data  # Data directory
```

---

## Docker Compose — Production PostgreSQL

```yaml
# docker-compose.yml
version: "3.8"

services:
  postgres:
    image: postgres:15
    container_name: bb-postgres
    
    environment:
      POSTGRES_USER: ${DB_USER:-beatrice}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-secret123}
      POSTGRES_DB: ${DB_NAME:-data_vault}
    
    ports:
      - "${DB_PORT:-5432}:5432"
    
    volumes:
      # Persistent data storage
      - postgres_data:/var/lib/postgresql/data
      # Init scripts (run on first start only)
      - ./sql/01_schemas.sql:/docker-entrypoint-initdb.d/01_schemas.sql
      - ./sql/02_tables.sql:/docker-entrypoint-initdb.d/02_tables.sql
      - ./sql/03_seed.sql:/docker-entrypoint-initdb.d/03_seed.sql
      # PostgreSQL config
      - ./config/postgresql.conf:/etc/postgresql/postgresql.conf
    
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-beatrice} -d ${DB_NAME:-data_vault}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    
    restart: unless-stopped
    
    # Resource limits
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M

volumes:
  postgres_data:
    driver: local
```

---

## Init Scripts — Auto-Setup on First Run

```sql
-- sql/01_schemas.sql
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS staging;

-- sql/02_tables.sql
CREATE TABLE IF NOT EXISTS bronze.raw_bank_marketing (
    id          BIGSERIAL PRIMARY KEY,
    age         TEXT,
    job         TEXT,
    marital     TEXT,
    education   TEXT,
    balance     TEXT,
    campaign    TEXT,
    y           TEXT,
    source_file TEXT,
    loaded_at   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS silver.bank_customers (
    id              BIGSERIAL PRIMARY KEY,
    age             SMALLINT,
    job             VARCHAR(50),
    marital         VARCHAR(20),
    education       VARCHAR(50),
    balance         DECIMAL(12,2),
    balance_segment VARCHAR(20),
    subscribed      BOOLEAN,
    processed_at    TIMESTAMP DEFAULT NOW()
);

-- sql/03_seed.sql
INSERT INTO silver.bank_customers (age, job, marital, balance, subscribed)
VALUES
    (28, 'management', 'single', 95000, true),
    (35, 'technician', 'married', 45000, false),
    (42, 'admin', 'divorced', 12000, true)
ON CONFLICT DO NOTHING;
```

---

## PostgreSQL Configuration Tuning

```conf
# config/postgresql.conf — optimised for data engineering

# Memory
shared_buffers = 256MB              # 25% of RAM
effective_cache_size = 768MB        # 75% of RAM
work_mem = 16MB                     # Per sort/hash operation
maintenance_work_mem = 128MB        # For VACUUM, CREATE INDEX

# Connections
max_connections = 100

# Write Ahead Log
wal_level = replica
max_wal_size = 1GB

# Query Planning
random_page_cost = 1.1              # SSD (use 4.0 for HDD)
effective_io_concurrency = 200      # SSD

# Logging
log_min_duration_statement = 1000   # Log queries > 1 second
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d '
```

---

## Working with PostgreSQL in Docker

```bash
# ── PSQL COMMANDS ─────────────────────────────────────

# Connect
docker exec -it bb-postgres psql -U beatrice -d data_vault

# Inside psql:
\l                          # List databases
\c data_vault               # Connect to database
\dt                         # List tables
\dt silver.*                # Tables in silver schema
\d silver.bank_customers    # Describe table
\di                         # List indexes
\dn                         # List schemas
\du                         # List users
\q                          # Quit

# ── RUN SQL FROM HOST ─────────────────────────────────

# Run single command
docker exec -it bb-postgres \
  psql -U beatrice -d data_vault \
  -c "SELECT COUNT(*) FROM silver.bank_customers;"

# Run SQL file
docker exec -i bb-postgres \
  psql -U beatrice -d data_vault \
  < ./sql/queries/analysis.sql

# ── IMPORT/EXPORT DATA ────────────────────────────────

# Import CSV
docker exec -i bb-postgres \
  psql -U beatrice -d data_vault \
  -c "\COPY bronze.raw_bank_marketing FROM STDIN WITH CSV HEADER" \
  < ./data/bank_marketing.csv

# Export to CSV
docker exec -i bb-postgres \
  psql -U beatrice -d data_vault \
  -c "\COPY (SELECT * FROM silver.bank_customers) TO STDOUT WITH CSV HEADER" \
  > ./outputs/bank_customers_export.csv

# ── BACKUP & RESTORE ──────────────────────────────────

# Backup entire database
docker exec bb-postgres \
  pg_dump -U beatrice data_vault \
  > backups/data_vault_$(date +%Y%m%d).sql

# Backup specific schema
docker exec bb-postgres \
  pg_dump -U beatrice -n silver data_vault \
  > backups/silver_$(date +%Y%m%d).sql

# Restore database
docker exec -i bb-postgres \
  psql -U beatrice data_vault \
  < backups/data_vault_20260520.sql

# Binary backup (faster, smaller)
docker exec bb-postgres \
  pg_dump -U beatrice -Fc data_vault \
  > backups/data_vault_$(date +%Y%m%d).dump

# Restore binary backup
docker exec -i bb-postgres \
  pg_restore -U beatrice -d data_vault \
  < backups/data_vault_20260520.dump
```

---

## Multiple PostgreSQL Versions

```bash
# Run Postgres 15 on port 5432
docker run -d \
  --name pg15 \
  -e POSTGRES_PASSWORD=secret \
  -p 5432:5432 \
  postgres:15

# Run Postgres 14 on port 5433 simultaneously!
docker run -d \
  --name pg14 \
  -e POSTGRES_PASSWORD=secret \
  -p 5433:5432 \
  postgres:14

# Run Postgres 13 on port 5434
docker run -d \
  --name pg13 \
  -e POSTGRES_PASSWORD=secret \
  -p 5434:5432 \
  postgres:13
```

---

## Python + Dockerised PostgreSQL

```python
# Connect Python to PostgreSQL running in Docker
import os
from sqlalchemy import create_engine
import pandas as pd

# Connection string
DB_URL = (
    f"postgresql://"
    f"{os.getenv('DB_USER', 'beatrice')}:"
    f"{os.getenv('DB_PASSWORD', 'secret123')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'data_vault')}"
)

engine = create_engine(DB_URL)

# Test connection
with engine.connect() as conn:
    result = conn.execute("SELECT version();")
    print(result.fetchone())

# Load data
df = pd.read_sql("SELECT * FROM silver.bank_customers", engine)
print(f"Loaded {len(df):,} rows")

# Write data
df_clean.to_sql(
    "bank_customers_v2",
    engine,
    schema="silver",
    if_exists="replace",
    index=False
)
```

---

## Automated Backup Script

```bash
#!/bin/bash
# backup-postgres.sh — Run daily via cron

CONTAINER="bb-postgres"
DB_USER="beatrice"
DB_NAME="data_vault"
BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Create backup directory
mkdir -p $BACKUP_DIR

# Create backup
echo "🔄 Backing up $DB_NAME..."
docker exec $CONTAINER \
    pg_dump -U $DB_USER -Fc $DB_NAME \
    > $BACKUP_DIR/backup_${DATE}.dump

if [ $? -eq 0 ]; then
    echo "✅ Backup saved: backup_${DATE}.dump"
    SIZE=$(du -sh $BACKUP_DIR/backup_${DATE}.dump | cut -f1)
    echo "   Size: $SIZE"
else
    echo "❌ Backup FAILED!"
    exit 1
fi

# Remove backups older than retention period
find $BACKUP_DIR -name "*.dump" -mtime +$RETENTION_DAYS -delete
echo "🗑️  Removed backups older than $RETENTION_DAYS days"

# List current backups
echo "📂 Current backups:"
ls -lh $BACKUP_DIR
```

---

## Security Best Practices

```yaml
# ✅ Use environment variables for credentials
environment:
  POSTGRES_PASSWORD: ${DB_PASSWORD}   # From .env file

# ✅ Never expose port 5432 externally in production
# ports:
#   - "5432:5432"     # Comment out in production
# Use internal network only:
networks:
  - internal-net

# ✅ Create application user (not superuser)
# In init.sql:
CREATE USER app_user WITH PASSWORD 'app_password';
GRANT CONNECT ON DATABASE data_vault TO app_user;
GRANT USAGE ON SCHEMA silver TO app_user;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA silver TO app_user;

# ✅ Use read-only user for BI tools
CREATE USER bi_reader WITH PASSWORD 'bi_password';
GRANT CONNECT ON DATABASE data_vault TO bi_reader;
GRANT USAGE ON SCHEMA gold TO bi_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA gold TO bi_reader;
```

---

## Quick Reference

```bash
# Run PostgreSQL
docker run -d \
  --name postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=pass \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15

# Connect
docker exec -it postgres psql -U user -d mydb

# Import CSV
docker exec -i postgres psql -U user -d mydb \
  -c "\COPY table FROM STDIN WITH CSV HEADER" < file.csv

# Backup
docker exec postgres pg_dump -U user mydb > backup.sql

# Restore
docker exec -i postgres psql -U user mydb < backup.sql

# Health check
docker exec postgres pg_isready -U user
```

---

## Previous | Next
← [[05 - Docker for Data Engineering]] | → [[07 - Docker Security and Best Practices]]
