## Best Practices for PostgreSQL in Docker

### 🛡️ 1. Regular Backups

#### 🔁 SQL Dump (Single DB)

bash

```
docker exec -t postgres-db pg_dump -U myuser mydatabase > backup.sql
```

#### 📦 Full Backup (All DBs + Roles)

bash

```
docker exec -t postgres-db pg_dumpall -U myuser > full_backup.sql
```

#### 🧪 Automated Backup Script

bash

```
#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d")
BACKUP_DIR="/path/to/pg-backups"
mkdir -p $BACKUP_DIR
docker exec postgres-db pg_dumpall -U myuser | gzip > $BACKUP_DIR/postgres_$TIMESTAMP.sql.gz
find $BACKUP_DIR -name "postgres_*.sql.gz" -mtime +30 -delete
```

#### ⏰ Cron Job (Daily at 3 AM)

cron

```
0 3 * * * /path/to/backup.sh
```

> 🔗 Backlink: [[backup strategy]] | [[Maintenance]] | [[Disaster Recovery]]

### 📦 2. Use Named Volumes

#### ✅ Create & Mount Volume

bash

```
docker volume create postgres-data

docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres
```

#### 📤 Volume Backup

bash

```
docker run --rm \
  -v postgres-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres-data-backup.tar.gz /data
```

#### 📥 Volume Restore

bash

```
docker run --rm \
  -v postgres-data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/postgres-data-backup.tar.gz --strip 1"
```

> 🔗 Backlink: [[Volumes]] | [[Upgrade Workflow]]

### 🔐 3. Secure Your PostgreSQL Container

#### 🔑 Strong Passwords

bash

```
export POSTGRES_PASSWORD=$(openssl rand -base64 32)
echo "$POSTGRES_PASSWORD" > postgres-password.txt
```

> 🔗 Backlink: [[Security]] | [[Environment Variables]]

#### 🌐 Restrict Network Access

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 127.0.0.1:5432:5432 \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres
```

> 🔗 Backlink: [[Networking]] | [[pg_hba.conf]]

#### 🧾 Custom PostgreSQL Config

conf

```
ssl = on
ssl_cert_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem'
ssl_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key'
max_connections = 100
authentication_timeout = 1min
listen_addresses = 'localhost'
```

#### 📦 Mount Config Files

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v ./pg_hba.conf:/var/lib/postgresql/data/pg_hba.conf \
  -v ./postgresql.conf:/var/lib/postgresql/data/postgresql.conf \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres
```

> 🔗 Backlink: [[postgresql.conf]] | [[Security Hardening]]

### ⬆️ 4. Keep PostgreSQL Updated

bash

```
docker pull postgres:latest
docker stop postgres-db
docker rm postgres-db
# Recreate with latest image
```

> 🔗 Backlink: [[Upgrade Workflow]] | [[Maintenance]]