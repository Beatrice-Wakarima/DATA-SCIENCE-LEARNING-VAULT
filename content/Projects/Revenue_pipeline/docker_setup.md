# 🐳 docker_setup

**Files:** `docker-compose.yml`, `Dockerfile`  
**Role:** Containerises the full ELT pipeline + PostgreSQL warehouse  
**Parent:** [[SPAERO_REVENUE_ANALYSIS]]  
**Tags:** #docker #infrastructure #devops

---

## Architecture

```
┌─────────────────────────── spaero_network (bridge) ───────────────────────┐
│                                                                             │
│  ┌─────────────────────┐          ┌──────────────────────────────────┐    │
│  │  postgres_warehouse  │◄─────────│         elt_pipeline             │    │
│  │  postgres:15-alpine  │  :5432   │  python:3.11-slim                │    │
│  │                      │          │                                  │    │
│  │  Persists data via   │          │  1. extract_load.py              │    │
│  │  named volume        │          │  2. transform.py                 │    │
│  │                      │          │  3. inspect_views.py             │    │
│  └─────────────────────┘          │  exits with code 0               │    │
│           │                        └──────────────────────────────────┘    │
└───────────┼─────────────────────────────────────────────────────────────────┘
            │ ports: 5439:5432
            ▼
     localhost:5439
     (Power BI connects here)
```

---

## Services

### `postgres_warehouse`

| Setting | Value |
|---|---|
| Image | `postgres:15-alpine` |
| Container name | `spaero_warehouse` |
| Internal port | `5432` |
| Host port | `${DB_HOST_PORT:-5439}` |
| Volume | `spaero_postgres_data` (named, persists across restarts) |
| Restart policy | `unless-stopped` |
| Healthcheck | `pg_isready -U ${DB_USER} -d ${DB_NAME}` every 5s |

> [!NOTE]
> Local Postgres 18 occupies `5432` on the host. Docker Postgres 15 is mapped to `5439` to avoid collision. Inside Docker, containers always talk on `5432`.

### `elt_pipeline`

| Setting | Value |
|---|---|
| Build | `Dockerfile` in project root |
| Container name | `spaero_elt` |
| Restart | `no` — runs once and exits |
| Depends on | `postgres_warehouse: service_healthy` |
| Volume mount | `./data:/app/data:ro` — Excel files, read-only |
| `DB_HOST` | Hardcoded to `postgres_warehouse` (service name resolves via network) |

---

## Dockerfile

```dockerfile
FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/extract_load.py  .
COPY scripts/transform.py     .
COPY scripts/inspect_views.py .

CMD ["sh", "-c", "python extract_load.py && python transform.py && python inspect_views.py"]
```

**Layer caching order:**
1. Base image (cached after first pull)
2. System packages (cached until apt changes)
3. `requirements.txt` copy (cached until file changes)
4. `pip install` (cached until requirements change)
5. Script files (rebuilds only when scripts change)

> [!TIP]
> Scripts are copied last so changing Python code doesn't invalidate the expensive `pip install` layer.

---

## Run Commands

```bash
# ── First time ─────────────────────────────────────────────────────
cp .env.example .env          # fill in credentials
docker compose up --build     # build image, start both services

# ── After code changes ─────────────────────────────────────────────
docker compose down
docker compose up --build     # force rebuild of elt_pipeline image

# ── After new data only (no code changes) ──────────────────────────
docker compose run --rm elt_pipeline

# ── Check pipeline logs ────────────────────────────────────────────
docker logs spaero_elt
docker logs spaero_warehouse

# ── Connect to database directly ───────────────────────────────────
docker exec -it spaero_warehouse psql -U ${DB_USER} -d ${DB_NAME}

# ── Inspect a specific view ────────────────────────────────────────
docker compose run --rm elt_pipeline python inspect_views.py --view presentation.vw_exec_kpi_scorecard
```

---

## Environment Variables

All read from `.env` in project root.

| Variable | Used by | Description |
|---|---|---|
| `DB_USER` | both services | Postgres username |
| `DB_PASSWORD` | both services | Postgres password |
| `DB_HOST` | `elt_pipeline` | Set to `postgres_warehouse` in compose |
| `DB_PORT` | `elt_pipeline` | Internal port — always `5432` |
| `DB_NAME` | both services | Database name |
| `DB_HOST_PORT` | `docker-compose.yml` | Host-side port mapping (e.g. `5439`) |

> [!WARNING]
> Never set `DB_PORT=5439` — that breaks the internal container connection. `DB_PORT` is the port inside Docker (`5432`). `DB_HOST_PORT` is what your host machine exposes (`5439`).

---

## Volumes & Networks

```yaml
networks:
  spaero_net:
    name: spaero_network
    driver: bridge        # both containers on same bridge = hostname resolution

volumes:
  postgres_data:
    name: spaero_postgres_data   # persists DB across docker compose down
```

> [!NOTE]
> `docker compose down` keeps the volume. `docker compose down -v` deletes it — database is wiped. Pipeline recreates everything from Excel on next run.

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `Network spaero_network Error` | Network already exists from previous run | Normal — ignore, compose recreates it |
| `parent snapshot does not exist` | Corrupted Docker build cache | `docker system prune -af` then `docker compose up --build` |
| `Connection refused on port 5439` | `elt_pipeline` using host port internally | Check `.env` — `DB_PORT` must be `5432`, not `5439` |
| `spaero_elt exited with code 1` | Pipeline script failed | `docker logs spaero_elt` to see which block failed |
| `postgres_warehouse not healthy` | DB slow to start | Healthcheck retries 10× — wait or increase `start_period` |
| `port 5439 already in use` | Another process on that port | Change `DB_HOST_PORT` in `.env` to e.g. `5440` |

---

## pgAdmin (Optional)

Not included by default. Your local pgAdmin or DBeaver can connect directly:

| Setting | Value |
|---|---|
| Host | `localhost` |
| Port | `5439` |
| Database | `DB_NAME` from `.env` |
| Username | `DB_USER` from `.env` |
| Password | `DB_PASSWORD` from `.env` |

Add as a new server connection — no extra container needed.

---

## Related

- [[SPAERO_REVENUE_ANALYSIS]] — Parent project note
- [[extract_load]] — Script running inside `elt_pipeline`
- [[transform]] — Script running inside `elt_pipeline`
- [[inspect_views]] — Script running inside `elt_pipeline`
