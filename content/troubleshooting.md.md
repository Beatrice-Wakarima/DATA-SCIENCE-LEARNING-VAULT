## Troubleshooting PostgreSQL in Docker

### 🧠 Common Connection Issues

#### 🔍 Check Container Status

bash

```
docker ps
```

- Confirms container is running
    
- Use `docker ps -a` to see stopped containers
    

> 🔗 Backlink: [[Container Lifecycle]] | [[PostgreSQL Setup]]

#### 🌐 Verify Port Mapping

bash

```
docker port postgres-db
```

- Ensures correct host-to-container port exposure
    
- Default: `5432:5432`, or custom like `5433:5432`
    

> 🔗 Backlink: [[Networking]] | [[pgAdmin Integration]]

#### 🔐 Authentication Errors

- Confirm correct `POSTGRES_USER` and `POSTGRES_PASSWORD`
    
- Check `pg_hba.conf` for allowed auth methods
    
- Use `scram-sha-256` for secure connections
    

> 🔗 Backlink: [[Security Hardening]] | [[pg_hba.conf]]

### 📜 Log Inspection

#### 🧾 View Logs

bash

```
docker logs postgres-db
```

#### 🔍 Tail Last 50 Logs

bash

```
docker logs --tail 50 postgres-db
```

#### 📡 Follow Logs Live

bash

```
docker logs -f postgres-db
```

- Useful for debugging startup or connection issues
    

> 🔗 Backlink: [[Monitoring Stack]] | [[Upgrade Workflow]]

### 🧱 Volume & Data Issues

#### 📦 Inspect Volume

bash

```
docker volume inspect postgres-data
```

#### 🧪 Restore from Backup

bash

```
docker run --rm \
  -v postgres-data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/postgres-data-backup.tar.gz --strip 1"
```

> 🔗 Backlink: [[backup strategy]] | [[Volumes]]

### 🧬 Version Conflicts

#### 🧾 Check PostgreSQL Version

bash

```
docker exec postgres-db postgres --version
```

#### ⬆️ Upgrade Safely

- Backup first
    
- Pull new image
    
- Recreate container with same volume
    

> 🔗 Backlink: [[Upgrade Workflow]] | [[Maintenance]]
### 🚨 Common Container Startup Issues

#### 🔍 Container Exits Immediately

bash

```
docker logs postgres-db
```

- Check logs for permission errors or missing environment variables
    

> 🔗 Backlink: [[Container Lifecycle]] | [[PostgreSQL Setup]]

#### 🛑 Volume Permission Error

text

```
initdb: could not change permissions of directory "/var/lib/postgresql/data": Operation not permitted
```

##### ✅ Fix Ownership & Permissions

bash

```
docker run --rm -v postgres-data:/data alpine ls -la /data
docker run --rm -v postgres-data:/data alpine chmod 700 /data
```

> 🔗 Backlink: [[Volumes]] | [[Security Hardening]]

#### 🔐 Missing Environment Variables

text

```
Database is uninitialized and superuser password is not specified
```

##### ✅ Solution

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres
```

> 🔗 Backlink: [[Environment Variables]] | [[PostgreSQL Setup]]

#### 🧱 Invalid Volume Contents

text

```
PostgreSQL Database directory appears to contain a database; Skipping initialization
```

##### ✅ Reinitialize with New Volume

bash

```
docker volume create postgres-data-new
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v postgres-data-new:/var/lib/postgresql/data \
  -d postgres
```

> 🔗 Backlink: [[Volumes]] | [[backup strategy]]

### 🌐 Connectivity Issues

#### ✅ Confirm Container Is Running

bash

```
docker ps | grep postgres-db
```

#### 🔍 Verify Port Mapping

bash

```
docker port postgres-db
```

> 🔗 Backlink: [[Networking]] | [[pgAdmin Integration]]

#### 🔧 Check Connection Parameters

- Hostname: `localhost` or `127.0.0.1`
    
- Port: `5432` (or mapped host port)
    
- Username: `POSTGRES_USER`
    
- Password: `POSTGRES_PASSWORD`
    
- Database: `POSTGRES_DB`
    

> 🔗 Backlink: [[PostgreSQL Setup]] | [[Security Hardening]]

#### 🧪 Test from Inside Container

bash

```
docker exec -it postgres-db psql -U postgres
```

> 🔗 Backlink: [[Container Lifecycle]] | [[Troubleshooting]]

#### 🔥 Check Firewall Rules

##### Linux

bash

```
sudo iptables -L | grep 5432
```

##### macOS

bash

```
sudo pfctl -sr | grep 5432
```

> 🔗 Backlink: [[Security Hardening]] | [[Networking]]