---
title: Introduction to Docker
tags: [docker, basics, devops]
created: 2026-05-20
up:: [[Docker MOC]]
---

# 🐳 Introduction to Docker

> Docker packages your application and everything it needs into a container that runs identically anywhere. No more "works on my machine." Essential for modern data engineering.

---

## The Problem Docker Solves

```
Without Docker:
  Developer laptop:  Python 3.11, pandas 2.0, Ubuntu 22  ✅
  Test server:       Python 3.8,  pandas 1.3, CentOS 7   ❌ Breaks!
  Production:        Python 3.10, pandas 1.5, Debian 11  ❌ Breaks!

With Docker:
  Everywhere:        Same container image               ✅ Always works!
```

---

## Virtual Machine vs Container

```
┌─────────────────────────┐    ┌─────────────────────────┐
│   Virtual Machine       │    │   Docker Container      │
├─────────────────────────┤    ├─────────────────────────┤
│  App A  │  App B        │    │  App A  │  App B        │
├─────────┼───────────────┤    ├─────────┼───────────────┤
│  OS A   │  OS B         │    │  Docker Engine          │
├─────────────────────────┤    ├─────────────────────────┤
│  Hypervisor             │    │  Host Operating System  │
├─────────────────────────┤    ├─────────────────────────┤
│  Hardware               │    │  Hardware               │
└─────────────────────────┘    └─────────────────────────┘
  GBs of overhead               MBs — starts in seconds!
```

| | VM | Container |
|---|---|---|
| Size | Gigabytes | Megabytes |
| Startup | Minutes | Seconds |
| OS | Full OS per VM | Shares host OS |
| Isolation | Complete | Process-level |
| Performance | Slower | Near-native |

---

## Core Docker Concepts

```
Image       = Blueprint / recipe (read-only)
Container   = Running instance of an image
Dockerfile  = Instructions to build an image
Registry    = Store for images (Docker Hub)
Volume      = Persistent storage for containers
Network     = Communication between containers
```

---

## Docker Architecture

```
┌──────────────────────────────────────────┐
│              Docker Client               │
│  (docker build, docker run, docker ps)   │
└──────────────────┬───────────────────────┘
                   │ REST API
┌──────────────────▼───────────────────────┐
│              Docker Daemon               │
│         (manages everything)             │
├─────────────────────────────────────────┤
│  Images  │  Containers  │  Networks     │
│          │              │  Volumes      │
└──────────┴──────────────┴───────────────┘
                   │
┌──────────────────▼───────────────────────┐
│           Docker Registry                │
│     (Docker Hub, ECR, GCR, etc.)        │
└──────────────────────────────────────────┘
```

---

## Installing Docker

```bash
# Windows — Download Docker Desktop
# https://docs.docker.com/desktop/install/windows/

# Verify installation
docker --version
docker compose version

# Test with hello-world
docker run hello-world

# Expected output:
# Hello from Docker!
# This message shows that your installation appears to be working correctly.
```

---

## Your First Container

```bash
# Run an nginx web server
docker run nginx

# Run in background (detached)
docker run -d nginx

# Run with port mapping (host:container)
docker run -d -p 8080:80 nginx
# Visit: http://localhost:8080

# Run with a name
docker run -d -p 8080:80 --name my-webserver nginx

# Run interactively (get a shell)
docker run -it ubuntu bash
# Now you're INSIDE the container!
# Type: ls, pwd, apt-get install python3
# Type: exit to leave

# Run and auto-remove when done
docker run --rm ubuntu echo "Hello from Ubuntu container!"
```

---

## Essential Docker Commands

```bash
# ── IMAGES ────────────────────────────────
docker images                       # List downloaded images
docker pull python:3.11-slim        # Download image from Docker Hub
docker rmi python:3.11-slim         # Remove image
docker image prune                  # Remove unused images
docker image prune -a               # Remove ALL unused images

# ── CONTAINERS ────────────────────────────
docker ps                           # List RUNNING containers
docker ps -a                        # List ALL containers (including stopped)
docker start container_name         # Start stopped container
docker stop container_name          # Gracefully stop container
docker kill container_name          # Force stop container
docker restart container_name       # Restart container
docker rm container_name            # Remove stopped container
docker rm -f container_name         # Force remove (even if running)

# ── INSPECT & DEBUG ───────────────────────
docker logs container_name          # View container output
docker logs -f container_name       # Follow live logs
docker logs --tail 50 container_name # Last 50 lines
docker exec -it container_name bash # Shell into running container
docker inspect container_name       # Detailed JSON info
docker stats                        # Live resource usage
docker top container_name           # Processes inside container

# ── CLEANUP ───────────────────────────────
docker system prune                 # Remove stopped containers + unused images
docker system prune -a              # Remove everything unused
docker volume prune                 # Remove unused volumes
docker network prune                # Remove unused networks
```

---

## Docker Run Flags Explained

```bash
docker run \
  -d \                          # Detached (background)
  -it \                         # Interactive + TTY (for shell access)
  --name my-container \         # Name the container
  -p 8080:80 \                  # Port: host:container
  -p 5432:5432 \                # Multiple port mappings
  -e DB_HOST=localhost \        # Environment variable
  -e DB_PASSWORD=secret \       # Another env var
  --env-file .env \             # Load env vars from file
  -v ./data:/app/data \         # Volume: host:container
  -v my-volume:/app/uploads \   # Named volume
  --network my-network \        # Connect to network
  --restart always \            # Auto-restart policy
  --memory 512m \               # Memory limit
  --cpus 1.0 \                  # CPU limit
  python:3.11-slim              # Image to use
```

---

## Working with PostgreSQL in Docker

```bash
# Run PostgreSQL (no installation needed!)
docker run -d \
  --name postgres-db \
  -e POSTGRES_USER=beatrice \
  -e POSTGRES_PASSWORD=secret123 \
  -e POSTGRES_DB=data_vault \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15

# Connect to it
docker exec -it postgres-db psql -U beatrice -d data_vault

# Run SQL commands
docker exec -it postgres-db psql -U beatrice -d data_vault -c "SELECT version();"
```

---

## Data Engineering Use Cases

```bash
# 1. Run a Python pipeline script
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  python:3.11-slim \
  python /app/pipeline.py

# 2. Run Apache Airflow
docker run -d \
  -p 8080:8080 \
  --name airflow \
  apache/airflow:2.7.0

# 3. Run Kafka
docker run -d \
  --name kafka \
  -p 9092:9092 \
  apache/kafka:3.7.0

# 4. Run a Jupyter notebook
docker run -d \
  -p 8888:8888 \
  -v $(pwd):/home/jovyan/work \
  jupyter/datascience-notebook

# 5. Run dbt
docker run --rm \
  -v $(pwd):/usr/app \
  -e DBT_PROFILES_DIR=/usr/app \
  ghcr.io/dbt-labs/dbt-postgres:1.7.0 \
  dbt run
```

---

## Docker Hub — Finding Images

```bash
# Search for images
docker search python
docker search postgres
docker search airflow

# Official images (most trusted)
python:3.11-slim        # Official Python
postgres:15             # Official PostgreSQL
redis:7                 # Official Redis
nginx:latest            # Official Nginx
ubuntu:22.04            # Official Ubuntu

# Image tags (versions)
python:3.11             # Full Python 3.11
python:3.11-slim        # Smaller (~50MB)
python:3.11-alpine      # Smallest (~20MB) - may have issues
python:latest           # Latest (avoid in production!)
```

---

## Quick Reference Card

```bash
# Lifecycle
docker pull image           # Download
docker run image            # Create + start
docker start container      # Start stopped
docker stop container       # Stop running
docker rm container         # Delete stopped
docker rmi image            # Delete image

# Inspect
docker ps                   # Running containers
docker ps -a                # All containers
docker images               # All images
docker logs container       # View logs
docker exec -it c bash      # Shell access

# Cleanup
docker system prune -a      # Nuclear option (removes everything unused)
```

---

## Previous | Next
← Start | → [[02 - Dockerfile]]
