---
title: Dockerfile
tags: [docker, dockerfile, devops]
created: 2026-05-20
up:: [[Docker MOC]]
---

# 📄 Dockerfile

> A Dockerfile is a script of instructions that builds a Docker image. Every production Python application needs one. Master this and you can containerise anything.

---

## What is a Dockerfile?

```
Dockerfile → docker build → Image → docker run → Container
(recipe)                    (cake)               (eaten cake)
```

---

## Basic Structure

```dockerfile
# Every Dockerfile starts with a base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy files from host to container
COPY requirements.txt .

# Run commands during build
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of app
COPY . .

# What port the app listens on
EXPOSE 8000

# Command to run when container starts
CMD ["python", "main.py"]
```

---

## All Dockerfile Instructions

```dockerfile
# FROM — base image (required, must be first)
FROM python:3.11-slim
FROM ubuntu:22.04
FROM scratch                    # Empty base (for static binaries)

# WORKDIR — set working directory (creates if doesn't exist)
WORKDIR /app
WORKDIR /usr/src/app

# COPY — copy files from host to image
COPY file.txt /app/
COPY src/ /app/src/
COPY . .                        # Copy everything
COPY requirements.txt .         # Copy to current WORKDIR

# ADD — like COPY but also handles URLs and tar files
ADD app.tar.gz /app/            # Auto-extracts tar files
ADD https://example.com/file /app/  # Downloads from URL

# RUN — execute command during BUILD (creates a layer)
RUN pip install pandas
RUN apt-get update && apt-get install -y gcc
RUN mkdir -p /app/data /app/logs

# ENV — set environment variables
ENV APP_ENV=production
ENV DB_PORT=5432
ENV PYTHONPATH=/app

# ARG — build-time variable (not in final image)
ARG PYTHON_VERSION=3.11
ARG BUILD_DATE

# EXPOSE — document which port app uses (doesn't actually open it)
EXPOSE 8000
EXPOSE 5432

# VOLUME — declare mount point for persistent data
VOLUME ["/app/data"]
VOLUME ["/app/logs"]

# USER — run as non-root user (security!)
USER appuser
USER 1000                       # By UID

# CMD — default command when container starts (can be overridden)
CMD ["python", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

# ENTRYPOINT — always runs (CMD becomes arguments)
ENTRYPOINT ["python"]
CMD ["main.py"]                 # python main.py
# docker run image other.py → python other.py

# HEALTHCHECK — how Docker monitors container health
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# LABEL — metadata
LABEL maintainer="beatrice@gmail.com"
LABEL version="1.0"
LABEL description="Bank Marketing Pipeline"
```

---

## Python App Dockerfile

```dockerfile
# Dockerfile for a Python data pipeline

# 1. Base image
FROM python:3.11-slim

# 2. Build arguments
ARG BUILD_DATE
ARG VERSION=1.0.0
LABEL build_date=$BUILD_DATE version=$VERSION

# 3. System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*   # Clean up to reduce image size

# 4. Working directory
WORKDIR /app

# 5. Install Python dependencies (copy requirements FIRST for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY main.py .

# 7. Create directories
RUN mkdir -p data/raw data/processed outputs logs

# 8. Security: create and use non-root user
RUN useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

# 9. Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_ENV=production

# 10. Health check
HEALTHCHECK --interval=60s --timeout=10s \
    CMD python -c "import sys; sys.exit(0)"

# 11. Run the pipeline
CMD ["python", "main.py"]
```

---

## FastAPI Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Multi-Stage Build — Smaller Images

```dockerfile
# Stage 1: Builder (has all build tools)
FROM python:3.11 AS builder

WORKDIR /app
COPY requirements.txt .

# Install packages to local user directory
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime (lean, no build tools)
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy ONLY the installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application
COPY src/ ./src/
COPY main.py .

# Make packages available
ENV PATH=/root/.local/bin:$PATH

CMD ["python", "main.py"]

# Result: ~200MB instead of ~900MB!
```

---

## Layer Caching — Speed Up Builds

```dockerfile
# ❌ SLOW — copies everything first, reinstalls on any file change
COPY . .
RUN pip install -r requirements.txt

# ✅ FAST — requirements cached separately
COPY requirements.txt .          # Only changes when requirements change
RUN pip install -r requirements.txt   # Cached if requirements unchanged
COPY . .                         # Other files can change without reinstalling
```

**Docker caches each layer. If a layer hasn't changed, it reuses the cache — making builds much faster.**

---

## Build & Run

```bash
# Build image from Dockerfile in current directory
docker build -t my-pipeline .

# Build with tag (version)
docker build -t my-pipeline:v1.0 .
docker build -t beatrice/bank-pipeline:latest .

# Build with build args
docker build \
  --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  --build-arg VERSION=2.0 \
  -t my-pipeline:v2.0 .

# Build without cache (fresh build)
docker build --no-cache -t my-pipeline .

# Run the built image
docker run my-pipeline
docker run -d -p 8000:8000 my-pipeline

# View image layers (understand size)
docker history my-pipeline
```

---

## .dockerignore — Exclude Files

```dockerignore
# .dockerignore — like .gitignore for Docker

# Virtual environment (huge, not needed in container)
venv/
env/
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Secrets (NEVER include these!)
.env
*.key
*.pem
secrets/

# Git
.git/
.gitignore

# Data files (often large, use volumes instead)
data/
*.csv
*.xlsx
*.parquet

# Notebooks (not needed in production)
notebooks/
*.ipynb
.ipynb_checkpoints/

# Tests (not needed in production image)
tests/
pytest.ini
.pytest_cache/

# Documentation
*.md
docs/

# IDE
.vscode/
.idea/
*.swp

# OS files
.DS_Store
Thumbs.db

# Logs
logs/
*.log
```

---

## Debugging Dockerfile Issues

```bash
# Build with verbose output
docker build --progress=plain -t my-app .

# Check image contents
docker run --rm -it my-app bash
# Inside: ls, cat requirements.txt, python --version

# Check image layers
docker history my-app

# Inspect image metadata
docker inspect my-app

# Run specific stage of multi-stage build
docker build --target builder -t my-app-debug .
docker run --rm -it my-app-debug bash

# Override CMD for debugging
docker run --rm -it my-app bash          # Get shell instead of running app
docker run --rm -it my-app python        # Get Python REPL
```

---

## Dockerfile Best Practices

```dockerfile
# ✅ Use specific version tags (not latest)
FROM python:3.11-slim          # Good
FROM python:latest             # Bad — could break on update

# ✅ Combine RUN commands to reduce layers
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ✅ Clean up in same RUN command
RUN pip install -r requirements.txt \
    && pip cache purge

# ✅ Use slim or alpine base images
FROM python:3.11-slim           # ~50MB
FROM python:3.11                # ~900MB

# ✅ Never run as root
RUN useradd -m appuser
USER appuser

# ✅ Use COPY not ADD (unless you need tar extraction)
COPY . .                       # Explicit and safe
ADD . .                        # Avoid unless needed

# ✅ Set PYTHONUNBUFFERED for logging
ENV PYTHONUNBUFFERED=1

# ✅ Use .dockerignore
# (create .dockerignore file)
```

---

## Quick Reference

```dockerfile
FROM image:tag          # Base image
WORKDIR /path           # Set working dir
COPY src dest           # Copy files
RUN command             # Execute during build
ENV KEY=value           # Environment variable
EXPOSE port             # Document port
USER username           # Switch user
VOLUME ["/path"]        # Declare volume
HEALTHCHECK CMD ...     # Health monitoring
CMD ["cmd", "arg"]      # Default run command
ENTRYPOINT ["cmd"]      # Always-run command
```

---

## Previous | Next
← [[01 - Introduction to Docker]] | → [[03 - Docker Volumes and Networks]]
