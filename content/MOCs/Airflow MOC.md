---
title: Airflow MOC
tags: [MOC, airflow, orchestration, data-engineering]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# 🌬️ Airflow MOC

> Complete Apache Airflow learning path — from first DAG to production deployment with Docker, Celery, and full monitoring.

---

## 🟢 Part 1 — Foundations

- [[01 - Introduction to Apache Airflow|01 · Introduction to Apache Airflow]]
- [[02 - Airflow Operators and Sensors|02 · Operators & Sensors]]

---

## 🔵 Part 2 — Core Skills

- [[03 - Airflow Taskflow API and Best Practices|03 · Taskflow API & Best Practices]]
- [[04 - Airflow Connections Variables and XCom|04 · Connections, Variables & XCom]]

---

## 🟣 Part 3 — Production

- [[05 - Airflow Production Deployment|05 · Production Deployment]]
- [[06 - Airflow Interview Cheat Sheet|06 · Interview Cheat Sheet]]

---

## 🔑 Key Concepts Summary

| Concept | Note | Description |
|---|---|---|
| DAG | 01 | Pipeline blueprint in Python |
| Executor | 01 | How tasks are run (Local/Celery/K8s) |
| schedule_interval | 01 | When the DAG runs |
| catchup | 01 | Backfill control |
| PythonOperator | 02 | Run Python functions |
| BashOperator | 02 | Run shell commands |
| BranchPythonOperator | 02 | Conditional branching |
| Sensors | 02 | Wait for conditions |
| Hooks | 02 | External system connections |
| Taskflow API | 03 | Modern decorator-based DAGs |
| Dynamic mapping | 03 | Parallel tasks from a list |
| Task groups | 03 | Visual organisation |
| Connections | 04 | Stored credentials |
| Variables | 04 | Configuration values |
| XCom | 04 | Data passing between tasks |
| CeleryExecutor | 05 | Production parallelism |
| Resource Monitors | 05 | Cost and concurrency control |
| Trigger rules | 06 | When tasks execute |
| Idempotency | 06 | Safe re-runs |

---

## 🗺️ Related MOCs

- [[Data Engineering MOC]]
- [[Docker MOC]]
- [[DBT MOC]]
- [[Python MOC]]
- [[Snowflake MOC]]

---

up:: [[Data Engineering MOC]]
