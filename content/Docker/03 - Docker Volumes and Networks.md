---
title: Docker Volumes and Networks
tags: [docker, volumes, networking, devops]
created: 2026-05-20
up:: [[Docker MOC]]
---

# 💾🌐 Docker Volumes & Networks

> Volumes persist data beyond container lifecycles. Networks let containers talk to each other. Both are essential for multi-container data pipelines.

---

## The Data Problem Without Volumes

```bash
# Start a container and create a file
docker run -it ubuntu bash
echo "important data" > /data/file.txt
exit

# Container stopped — data is GONE when you remove it!
docker rm container_id

# Solution: Volumes persist data outside the container
```

---

## Types of Storage

```
┌─────────────────────────────────────────────────────┐
│                  Docker Host                        │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐ │
│  │ Named    │  │  Bind    │  │   tmpfs Mount     │ │
│  │ Volume   │  │  Mount   │  │   (in memory)     │ │
│  │/var/lib/ │  │./data →  │  │   Fast, temporary │ │
│  │docker/   │  │/app/data │  │                   │ │
│  │volumes/  │  │          │  │                   │ │
│  └──────────┘  └──────────┘  └───────────────────┘ │
└─────────────────────────────────────────────────────┘
  Managed by Docker  Host filesystem  RAM only
  Best for prod      Best for dev     Best for secrets
```

---

## Named Volumes

```bash
# Create a named volume
docker volume create my-data

# List volumes
docker volume ls

# Inspect volume
docker volume inspect my-data

# Use volume in container
docker run -d \
  -v my-data:/app/data \
  --name my-pipeline \
  my-pipeline-image

# Use with PostgreSQL (data persists!)
docker run -d \
  --name postgres \
  -v postgres-data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# Stop and remove container — DATA IS SAFE
docker stop postgres
docker rm postgres

# Start new container — data is still there!
docker run -d \
  --name postgres-new \
  -v postgres-data:/var/lib/postgresql/data \  # Same volume!
  postgres:15

# Remove volume (permanent delete!)
docker volume rm my-data
docker volume prune    # Remove all unused volumes
```

---

## Bind Mounts — Share Host Folder

```bash
# Mount current directory into container
docker run -d \
  -v $(pwd)/data:/app/data \        # host:container
  -v $(pwd)/outputs:/app/outputs \
  my-pipeline

# Windows Git Bash syntax
docker run -d \
  -v //c/Users/iescpcadmin/Desktop/Data_Science_Learning_Vault:/vault \
  my-pipeline

# Read-only mount (container can't write)
docker run -d \
  -v $(pwd)/config:/app/config:ro \
  my-pipeline

# Great for development — code changes reflect immediately!
docker run -d \
  -v $(pwd):/app \                  # Mount entire project
  -p 8000:8000 \
  fastapi-dev
```

---

## Docker Networks

```bash
# List networks
docker network ls

# Default networks:
# bridge  — default, containers on same host can communicate
# host    — container uses host's network directly
# none    — no networking

# Create custom network
docker network create my-network
docker network create \
  --driver bridge \
  --subnet 172.20.0.0/16 \
  data-pipeline-network

# Connect container to network
docker run -d \
  --name postgres \
  --network my-network \
  postgres:15

docker run -d \
  --name api \
  --network my-network \     # Same network = can talk to postgres!
  -p 8000:8000 \
  my-api

# Connect running container to network
docker network connect my-network existing-container

# Inspect network
docker network inspect my-network

# Remove network
docker network rm my-network
docker network prune
```

---

## Container Communication

```bash
# Containers on the same network can use container NAME as hostname

# Start postgres
docker run -d \
  --name my-postgres \           # Name becomes hostname!
  --network app-network \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# Python app can connect using container name
docker run -d \
  --name my-app \
  --network app-network \
  -e DB_HOST=my-postgres \       # Use container name as host!
  -e DB_PORT=5432 \
  my-python-app

# Python code inside container:
# engine = create_engine("postgresql://user:pass@my-postgres:5432/db")
#                                              ↑ container name works!
```

---

## Real World Example — Data Pipeline Network

```bash
# Create isolated network for pipeline
docker network create pipeline-net

# 1. Start PostgreSQL
docker run -d \
  --name postgres \
  --network pipeline-net \
  -v pgdata:/var/lib/postgresql/data \
  -e POSTGRES_USER=beatrice \
  -e POSTGRES_PASSWORD=secret123 \
  -e POSTGRES_DB=data_vault \
  postgres:15

# 2. Start Redis (for caching)
docker run -d \
  --name redis \
  --network pipeline-net \
  -v redis-data:/data \
  redis:7-alpine

# 3. Run ETL pipeline
docker run --rm \
  --name etl \
  --network pipeline-net \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  -e DB_HOST=postgres \          # Uses container name!
  -e DB_PASSWORD=secret123 \
  -e REDIS_HOST=redis \
  bank-etl-pipeline

# 4. Start API
docker run -d \
  --name api \
  --network pipeline-net \
  -p 8000:8000 \
  -e DB_HOST=postgres \
  -e REDIS_HOST=redis \
  bank-api

echo "Stack running!"
echo "API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
```

---

## Volume Backup & Restore

```bash
# Backup a named volume
docker run --rm \
  -v postgres-data:/source:ro \
  -v $(pwd)/backups:/backup \
  ubuntu \
  tar czf /backup/postgres-backup-$(date +%Y%m%d).tar.gz -C /source .

# Restore from backup
docker run --rm \
  -v postgres-data:/target \
  -v $(pwd)/backups:/backup \
  ubuntu \
  tar xzf /backup/postgres-backup-20260520.tar.gz -C /target

# Copy file from container to host
docker cp container_name:/app/output.csv ./output.csv

# Copy file from host to container
docker cp ./data.csv container_name:/app/data/data.csv
```

---

## Storage Quick Reference

```bash
# Named volumes (managed by Docker)
docker volume create vol-name
docker run -v vol-name:/container/path image

# Bind mounts (host directory)
docker run -v /host/path:/container/path image
docker run -v $(pwd):/app image          # Current dir

# Read-only
docker run -v /host/path:/container/path:ro image

# Inspect
docker volume ls
docker volume inspect vol-name

# Cleanup
docker volume rm vol-name
docker volume prune
```

```bash
# Networks
docker network create net-name
docker run --network net-name image
docker network connect net-name container
docker network ls
docker network inspect net-name
docker network rm net-name
docker network prune
```

---

## Previous | Next
← [[02 - Dockerfile]] | → [[04 - Docker Compose]]
