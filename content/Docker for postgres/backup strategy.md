### Volume-Based Backup (SQL Dump)

#### 🧬 Create SQL Backup

bash

```
docker run --rm \
  -v postgres-data:/data \
  -v $(pwd):/backup \
  postgres:17.4 \
  bash -c "pg_dumpall -U myuser > /backup/postgres_backup.sql"
```

- `--rm`: Removes container after execution
    
- `-v postgres-data:/data`: Mounts data volume
    
- `-v $(pwd):/backup`: Mounts local folder for output
    
- `pg_dumpall`: Dumps all databases, roles, and configs
    

> 🔗 Backlink: [[Upgrade Workflow]] | [[Disaster Recovery]]

### 🧾 Backup Best Practices

- **Schedule regular backups** (daily or weekly)
    
- **Use timestamped filenames** for versioning
    
- **Store backups off-host** (e.g., cloud, external disk)
    
- **Verify backup integrity** before upgrades
    
- **Automate with cron or CI/CD hooks**
    

> 🔗 Backlink: [[Maintenance]] | [[Security]]

### 🔁 Restore from SQL Dump

bash

```
psql -U myuser -f postgres_backup.sql
```

- Run inside a fresh container or existing DB
    
- Restores roles, databases, and data
    

> 🔗 Backlink: [[Disaster Recovery]] | [[PostgreSQL Setup]]
## ⬆️ Upgrade Workflow for PostgreSQL in Docker

### 🎯 Why Upgrade?

- Access new features and performance improvements
    
- Apply security patches and bug fixes
    
- Maintain compatibility with client applications
    

> 🔗 Backlink: [[backup strategy]] | [[Maintenance]] | [[Images]]

### 🧠 Pre-Upgrade Checklist

- ✅ Confirm current version: `docker exec postgres-db postgres --version`
    
- ✅ Review PostgreSQL release notes
    
- ✅ Backup your data volume
    
- ✅ Test upgrade in a non-production environment
    

### 📦 Backup Before Upgrade

bash

```
docker run --rm \
  -v postgres-data:/data \
  -v $(pwd):/backup \
  postgres:17.4 \
  bash -c "pg_dumpall -U myuser > /backup/postgres_backup.sql"
```

- Creates SQL dump in current directory
    
- Ensures rollback safety
    

> 🔗 Backlink: [[Volumes]] | [[Disaster Recovery]]

### 🔄 Upgrade Steps

#### 1. Pull New Image

bash

```
docker pull postgres:17.5
```

#### 2. Stop & Remove Old Container

bash

```
docker stop postgres-db
docker rm postgres-db
```

#### 3. Start New Container (Same Volume)

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_DB=mydatabase \
  -v postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres:17.5
```

> 🔗 Backlink: [[PostgreSQL Setup]] | [[Container Lifecycle]]

### ⚠️ Major Version Considerations

- PostgreSQL may auto-run internal migrations
    
- Always test upgrades in staging first
    
- Backup volume before applying changes
    
- Monitor logs post-upgrade:
    
    bash
    
    ```
    docker logs -f postgres-db
    ```