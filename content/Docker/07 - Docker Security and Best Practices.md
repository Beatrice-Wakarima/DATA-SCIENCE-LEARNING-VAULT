---
title: Docker Security and Best Practices
tags: [docker, security, devops, best-practices]
created: 2026-05-20
up:: [[Docker MOC]]
---

# 🔒 Docker Security & Best Practices

> Security is not optional in production. These practices protect your containers, data, and infrastructure from vulnerabilities and attacks.

---

## The Top Security Risks

```
1. Running as root (default — dangerous!)
2. Hardcoded secrets in images
3. Using unverified base images
4. Exposing unnecessary ports
5. Overly permissive network access
6. Outdated base images with CVEs
7. Secrets in environment variables
8. Writable filesystems
```

---

## Rule 1 — Never Run as Root

```dockerfile
# ❌ Bad — runs as root by default
FROM python:3.11-slim
COPY . .
CMD ["python", "main.py"]

# ✅ Good — create and use non-root user
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

CMD ["python", "main.py"]
```

```bash
# Verify container runs as non-root
docker run --rm my-app whoami
# Expected: appuser (not root)

# Run as specific user
docker run --user 1000:1000 my-app
```

---

## Rule 2 — Never Put Secrets in Images

```dockerfile
# ❌ NEVER do this — secrets baked into image!
ENV DB_PASSWORD=secret123
ENV API_KEY=abc123xyz

# ❌ NEVER do this — visible in docker history!
RUN export DB_PASSWORD=secret && python setup.py

# ✅ Pass secrets at runtime
# docker run -e DB_PASSWORD=secret my-app

# ✅ Use .env file (never commit it!)
# docker run --env-file .env my-app

# ✅ Use Docker secrets (production)
# docker secret create db_password ./password.txt
```

```bash
# Check if secrets are in image history
docker history --no-trunc my-image | grep -i password
docker history --no-trunc my-image | grep -i secret
docker history --no-trunc my-image | grep -i key

# Inspect image for env vars
docker inspect my-image | grep -i env
```

---

## Rule 3 — Use Minimal Base Images

```dockerfile
# Size comparison:
# python:3.11          = ~900MB (full OS, dev tools)
# python:3.11-slim     = ~150MB (minimal OS)
# python:3.11-alpine   = ~50MB  (very minimal, musl libc)
# distroless           = ~30MB  (no shell, most secure)

# ✅ Use slim for most cases
FROM python:3.11-slim

# ✅ Alpine for smallest images (may need extra packages)
FROM python:3.11-alpine
RUN apk add --no-cache gcc musl-dev libpq-dev

# ✅ Distroless for maximum security (no shell to exploit)
FROM gcr.io/distroless/python3-debian12
```

---

## Rule 4 — Read-Only Filesystem

```bash
# Run container with read-only filesystem
docker run --read-only my-app

# Allow writes only to specific directories
docker run \
  --read-only \
  --tmpfs /tmp \                        # Temp files in memory
  -v $(pwd)/outputs:/app/outputs \      # Explicit write location
  -v $(pwd)/logs:/app/logs \            # Explicit log location
  my-app
```

```yaml
# In docker-compose.yml
services:
  api:
    image: my-api
    read_only: true
    tmpfs:
      - /tmp
    volumes:
      - ./logs:/app/logs
```

---

## Rule 5 — Limit Resources

```yaml
# docker-compose.yml
services:
  pipeline:
    image: my-pipeline
    deploy:
      resources:
        limits:
          cpus: "1.0"           # Max 1 CPU core
          memory: 512M          # Max 512MB RAM
        reservations:
          cpus: "0.5"           # Guaranteed 0.5 CPU
          memory: 256M          # Guaranteed 256MB RAM
```

```bash
# Limit resources at run time
docker run \
  --memory 512m \           # Max 512MB RAM
  --memory-swap 512m \      # No swap
  --cpus 1.0 \              # Max 1 CPU
  --pids-limit 100 \        # Max 100 processes
  my-pipeline
```

---

## Rule 6 — Network Isolation

```yaml
# Isolate services — only expose what's needed
version: "3.8"

services:
  postgres:
    image: postgres:15
    networks:
      - internal              # NOT exposed externally
    # NO ports section = not accessible from host

  api:
    build: .
    networks:
      - internal              # Can reach postgres
      - external              # Exposed to internet
    ports:
      - "8000:8000"           # Only API is public

  pipeline:
    build: ./pipeline
    networks:
      - internal              # Can reach postgres
    # NO ports = not accessible from outside

networks:
  internal:
    internal: true            # Completely isolated
  external:
    driver: bridge
```

---

## Rule 7 — Scan Images for Vulnerabilities

```bash
# Docker Scout (built into Docker Desktop)
docker scout cves my-image
docker scout recommendations my-image

# Trivy (open source, most popular)
# Install: https://github.com/aquasecurity/trivy
trivy image my-image
trivy image --severity HIGH,CRITICAL my-image
trivy image python:3.11-slim

# Fix: Update base image regularly
FROM python:3.11-slim       # Pin to specific version
RUN apt-get update && apt-get upgrade -y  # Update packages
```

---

## Rule 8 — Use Multi-Stage Builds

```dockerfile
# Multi-stage removes dev tools from final image
# Attackers can't exploit tools that aren't there!

# Stage 1: Builder (has compilers, dev tools)
FROM python:3.11 AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime (clean, minimal)
FROM python:3.11-slim AS runtime
WORKDIR /app

# Copy only what's needed from builder
COPY --from=builder /root/.local /root/.local

COPY src/ ./src/
COPY main.py .

RUN useradd -m appuser && chown -R appuser /app
USER appuser

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "main.py"]
# Final image: no gcc, no pip, no compilers — smaller attack surface
```

---

## Secure docker-compose.yml Template

```yaml
version: "3.8"

services:
  app:
    build: .
    
    # Security settings
    read_only: true                 # Read-only filesystem
    user: "1000:1000"              # Non-root user
    
    # No new privileges
    security_opt:
      - no-new-privileges:true
    
    # Drop all capabilities, add only needed
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE            # Only if binding to port < 1024
    
    # Resource limits
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"
    
    # Tmpfs for writable directories
    tmpfs:
      - /tmp
    
    # Volumes (explicit, no broad mounts)
    volumes:
      - ./outputs:/app/outputs     # Specific, not ./:/app
    
    # Secrets from env file (not hardcoded)
    env_file:
      - .env
    
    # Network isolation
    networks:
      - app-network

  postgres:
    image: postgres:15
    
    # Security
    user: "999:999"                 # postgres user
    read_only: false                # Postgres needs writes
    security_opt:
      - no-new-privileges:true
    
    # No external port exposure!
    # ports: - "5432:5432"         # COMMENTED OUT in production
    
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password  # Docker secret
    
    networks:
      - app-network

networks:
  app-network:
    internal: false

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

---

## .dockerignore for Security

```dockerignore
# Security critical — ALWAYS ignore these
.env
.env.*
*.key
*.pem
*.p12
*.pfx
secrets/
credentials/

# Source control
.git/
.gitignore

# Dev tools
venv/
.venv/
__pycache__/

# Sensitive data
data/
*.csv
*.xlsx
backups/

# IDE config (may contain secrets)
.vscode/settings.json
.idea/
```

---

## Security Checklist

```
Dockerfile:
  ✅ Uses slim/alpine base image
  ✅ Pinned version tag (not latest)
  ✅ Runs as non-root user
  ✅ Multi-stage build (dev tools excluded)
  ✅ .dockerignore present
  ✅ No secrets or passwords

Runtime:
  ✅ --read-only filesystem
  ✅ Resource limits set
  ✅ Secrets via env file or Docker secrets
  ✅ No unnecessary ports exposed

Networking:
  ✅ Internal network for databases
  ✅ Only API/web ports exposed externally
  ✅ No --network host in production

Maintenance:
  ✅ Base images updated regularly
  ✅ Images scanned for CVEs
  ✅ Unused images removed
```

---

## Quick Security Commands

```bash
# Check running user
docker run --rm my-image whoami

# Check exposed ports
docker inspect my-container | grep -i port

# Check environment variables (may expose secrets!)
docker inspect my-container | grep -i env

# Scan for vulnerabilities
docker scout cves my-image

# Check image layers for secrets
docker history --no-trunc my-image

# Run with security options
docker run \
  --read-only \
  --user 1000:1000 \
  --security-opt no-new-privileges \
  --cap-drop ALL \
  --memory 512m \
  my-image
```

---

## Previous | Next
← [[06 - Docker for PostgreSQL]] | → [[08 - Docker Interview Checklist]]
