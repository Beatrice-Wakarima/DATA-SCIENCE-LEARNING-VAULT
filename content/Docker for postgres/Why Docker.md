## Why Use PostgreSQL in Docker

### 🔍 What Is PostgreSQL?

A powerful, open-source relational database system used for transactional workloads, analytics, and data warehousing.

> 🔗 Backlink: [[PostgreSQL Overview]]

### ✅ Benefits of Dockerized PostgreSQL

- **🚀 Simplified Setup** Spin up PostgreSQL with one command—no manual installation or dependency wrangling.
    
- **🔁 Consistent Environments** Identical setups across OSes and teams—eliminates “works on my machine” issues.
    
- **🧼 Isolation & Flexibility** Run multiple PostgreSQL versions side-by-side without conflict.
    
- **📌 Version Control** Lock database versions for reproducibility and upgrade testing.
    
- **⚡ Resource Efficiency** Lightweight containers outperform VMs for dev/test workloads.
    

### 🧠 When to Use PostgreSQL in Docker

- **Local Development** Quick setup, exact version matching, safe experimentation
    
- **Microservices Architecture** Isolated DB per service, independent lifecycle
    
- **CI/CD & Testing** Fresh DB per test run improves reliability
    
- **Migration Script Development** Safely test schema changes before production
    
- **Kubernetes Deployments** Seamless dev-to-prod parity in container orchestration
### Setup Prerequisites

- Install Docker Engine or Docker Desktop
    
    - Ubuntu:
        
        bash
        
        ```
        sudo apt update  
        sudo apt install docker.io  
        sudo systemctl enable --now docker
        ```
        
- Understand basic Docker concepts:
    
    - Images, Containers, Volumes
        

### 📦 Pulling PostgreSQL Image

bash

```
docker pull postgres          # latest stable
docker pull postgres:17       # specific version
docker pull postgres:bookworm # Debian-based variant
```

> 🔗 Backlink: [[Images]] | [[PostgreSQL Setup]]
## Running PostgreSQL in Docker

### 🚀 Basic Command

bash

```
docker run --name postgres-db -e POSTGRES_PASSWORD=mypassword postgres
```

#### 🔍 Breakdown

- `docker run`: Creates and starts a container
    
- `--name postgres-db`: Assigns a name for easy reference
    
- `-e POSTGRES_PASSWORD=mypassword`: Sets password for default `postgres` user
    
- `postgres`: Uses official PostgreSQL image from Docker Hub
    

> 🔗 Backlink: [[Images]] | [[PostgreSQL Setup]]

### ⚙️ Recommended Full Command

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_DB=mydatabase \
  -p 5432:5432 \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres
```

#### 🧠 Explanation

- `POSTGRES_USER`: Creates a custom superuser
    
- `POSTGRES_DB`: Creates a named database
    
- `-p 5432:5432`: Maps container port to host for external access
    
- `-v postgres-data:/var/lib/postgresql/data`: Persists data via Docker volume
    
- `-d`: Runs container in detached (background) mode
    

> 🔗 Backlink: [[Volumes]] | [[Networking]] | [[docker-compose.yml]]

### 🧪 Verify Container Status

bash

```
docker ps
```

- Lists running containers with ID, image, status, ports, and name
    

> 🔗 Backlink: [[Container Lifecycle]] | [[Troubleshooting]]

### 🧱 Use Cases

- Local dev with isolated DB
    
- CI/CD test environments
    
- Microservices with independent DBs
    
- Safe migration script testing
    
- Kubernetes-ready setups
    

> 🔗 Backlink: [[Case Study]] | [[backup strategy]] | [[Monitoring Stack]]
## Configuring PostgreSQL in Docker

### 📦 Persistent Storage with Volumes

#### 🔍 Why It Matters

- Containers are ephemeral—data disappears when removed
    
- Volumes store data outside the container filesystem
    
- Essential for database durability, backups, and upgrades
    

> 🔗 Backlink: [[Volumes]] | [[PostgreSQL Setup]]

### 🧱 Create a Named Volume

bash

```
docker volume create postgres-data
```

- Creates a persistent volume named `postgres-data`
    
- Survives container restarts, removals, and upgrades
    

> 🔗 Backlink: [[docker-compose.yml]] | [[backup strategy]]

### 🔍 Inspect Volume Details

bash

```
docker volume inspect postgres-data
```

- Shows mount point, metadata, and configuration
    
- Useful for debugging or backup planning
    

> 🔗 Backlink: [[Troubleshooting]] | [[Volume Management]]

### 🚀 Run PostgreSQL with Volume Mounted

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres
```

#### 🧠 Breakdown

- `-v postgres-data:/var/lib/postgresql/data`: Mounts volume to PostgreSQL’s data directory
    
- Ensures data persists across container lifecycle
    
- `-d`: Detached mode (runs in background)
    

> 🔗 Backlink: [[Container Lifecycle]] | [[PostgreSQL Setup]]

### ✅ Advantages of Using Volumes

- Data survives container removal
    
- Easy container upgrades without data loss
    
- Backup-friendly: volume can be archived independently
    
- Better performance than bind mounts (especially on macOS/Windows)
    

> 🔗 Backlink: [[backup strategy]] | [[Maintenance]]
## 🌐 Exposing Ports to Connect to PostgreSQL

### 🔓 Default Port Mapping

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -d postgres
```

- Maps container’s port `5432` to host’s port `5432`
    
- Enables access via `localhost:5432`
    

> 🔗 Backlink: [[Networking]] | [[PostgreSQL Setup]]

### 🔁 Alternate Port Mapping

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5433:5432 \
  -d postgres
```

- Maps container’s port `5432` to host’s port `5433`
    
- Useful if port `5432` is already in use
    

> 🔗 Backlink: [[Troubleshooting]] | [[pgAdmin Integration]]

### 🔐 Restrict to Localhost

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 127.0.0.1:5432:5432 \
  -d postgres
```

- Limits access to local machine only
    
- Enhances security by blocking external connections
    

> 🔗 Backlink: [[Security]] | [[pg_hba.conf]]

## ⚙️ Configuring PostgreSQL Settings

### 🧬 Environment Variables

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_DB=mydatabase \
  -e POSTGRES_INITDB_ARGS="--data-checksums" \
  -e POSTGRES_HOST_AUTH_METHOD=scram-sha-256 \
  -d postgres
```

#### 🔍 Breakdown

- `POSTGRES_PASSWORD`: Sets superuser password
    
- `POSTGRES_USER`: Creates custom superuser
    
- `POSTGRES_DB`: Creates default database
    
- `POSTGRES_INITDB_ARGS`: Passes initdb flags (e.g., checksums)
    
- `POSTGRES_HOST_AUTH_METHOD`: Sets auth method (e.g., `scram-sha-256`)
    

> 🔗 Backlink: [[PostgreSQL Setup]] | [[Security]]

### 🧠 Custom Configuration File

Create `my-postgres.conf`:

conf

```
max_connections = 200
shared_buffers = 1GB
work_mem = 16MB
maintenance_work_mem = 256MB
```

Mount it:

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v ./my-postgres.conf:/etc/postgresql/postgresql.conf \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres \
  -c 'config_file=/etc/postgresql/postgresql.conf'
```

> 🔗 Backlink: [[postgresql.conf]] | [[Performance Tuning]] | [[Volumes]]
## 🔗 Connecting to PostgreSQL in Docker

### 🧱 Reference Setup

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_DB=mydatabase \
  -v postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres
```

> 🔗 Backlink: [[PostgreSQL Setup]] | [[Volumes]] | [[Networking]]

### 🖥️ Method 1: Command-Line (psql)

#### 🔍 Connect Using `psql`

bash

```
docker exec -it postgres-db psql -U myuser -d mydatabase
```

- `docker exec -it`: Runs interactive command inside container
    
- `psql -U myuser -d mydatabase`: Connects to DB as user `myuser`
    

> 🔗 Backlink: [[Container Lifecycle]] | [[Troubleshooting]]

#### 🧪 Common Issues

- Check container status: `docker ps`
    
- Verify port mapping: `docker port postgres-db`
    

### 🖼️ Method 2: GUI (pgAdmin or DBeaver)

#### 🔧 pgAdmin Setup

- Right-click **Servers** → Register → Server
    
- **General tab**: Name your connection
    
- **Connection tab**:
    
    - Host: `localhost`
        
    - Port: `5432` (or mapped port)
        
    - DB: `mydatabase`
        
    - User: `myuser`
        
    - Password: `mysecretpassword`
        

> 🔗 Backlink: [[pgAdmin Integration]] | [[Security]]

### 🧠 Why It Works

From your app’s perspective, Dockerized PostgreSQL behaves like any local or cloud-hosted instance. The container exposes the database at the mapped address (`localhost:5432`), and tools connect using standard credentials.

> 🔗 Backlink: [[Case Study]] | [[Access from Python]]
### 🔄 Container Lifecycle Commands

#### 🧱 Stop, Start, Restart

bash

```
docker stop postgres-db
docker start postgres-db
docker restart postgres-db
```

- Gracefully manage container state
    
- Useful after config changes or during maintenance
    

> 🔗 Backlink: [[Container Lifecycle]] | [[postgresql.conf]]

#### 🧹 Remove Container (Preserve Data)

bash

```
docker stop postgres-db
docker rm postgres-db
```

- Removes container but **not** the volume
    
- Data remains in `postgres-data`
    

> 🔗 Backlink: [[Volumes]] | [[backup strategy]]

#### 📋 List All Containers

bash

```
docker ps -a
```

- Shows running and stopped containers
    
- Confirms removal or status
    

> 🔗 Backlink: [[Troubleshooting]]

### 📜 Inspecting Logs

#### 🧾 View All Logs

bash

```
docker logs postgres-db
```

#### 🔍 Tail Last 50 Logs

bash

```
docker logs --tail 50 postgres-db
```

#### 📡 Follow Logs in Real-Time

bash

```
docker logs -f postgres-db
```

- Great for debugging or monitoring live activity
    
- Use `Ctrl+C` to exit
    

> 🔗 Backlink: [[Monitoring Stack]] | [[pg_stat_statements]]

### ⬆️ Updating PostgreSQL Version

#### 🧬 Pull New Image

bash

```
docker pull postgres:17.5
```

#### 🔄 Replace Container (Keep Volume)

bash

```
docker stop postgres-db
docker rm postgres-db

docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_DB=mydatabase \
  -v postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres:17.5
```

> 🔗 Backlink: [[Images]] | [[PostgreSQL Setup]]

### 🧯 Backup Before Upgrade

bash

```
docker run --rm \
  -v postgres-data:/data \
  -v $(pwd):/backup \
  postgres:17.4 \
  bash -c "pg_dumpall -U myuser > /backup/postgres_backup.sql"
```

- Creates SQL dump in current directory
    
- Essential before major upgrades
    

> 🔗 Backlink: [[backup strategy]] | [[Maintenance]]