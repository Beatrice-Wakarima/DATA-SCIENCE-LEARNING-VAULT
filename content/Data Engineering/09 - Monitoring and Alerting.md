---
title: Monitoring and Alerting
tags: [data-engineering, monitoring, alerting, observability]
created: 2026-05-20
up:: [[Data Engineering MOC]]
---

# 📡 Monitoring & Alerting

> A pipeline that fails silently is worse than no pipeline. Monitoring gives you visibility into what's running, what's broken, and how your data is behaving. Alerting ensures you find out before your stakeholders do.

---

## What to Monitor

```
Pipeline Health:
  ✅ Did the pipeline run on schedule?
  ✅ Did all tasks succeed?
  ✅ How long did it take?
  ✅ How many rows were processed?

Data Quality:
  ✅ Is the data fresh (updated on time)?
  ✅ Are row counts within expected range?
  ✅ Are there unexpected nulls or duplicates?
  ✅ Has the schema changed?

Infrastructure:
  ✅ Database connections available?
  ✅ Disk space sufficient?
  ✅ Container health?
```

---

## Pipeline Metrics Table

```sql
-- Store metrics from every pipeline run
CREATE TABLE pipeline_metrics (
    id              BIGSERIAL PRIMARY KEY,
    run_id          VARCHAR(100) UNIQUE,
    pipeline_name   VARCHAR(100) NOT NULL,
    run_date        DATE NOT NULL,
    started_at      TIMESTAMP NOT NULL,
    completed_at    TIMESTAMP,
    duration_secs   INTEGER,
    status          VARCHAR(20),            -- success | failed | warning

    -- Volume metrics
    rows_extracted  INTEGER DEFAULT 0,
    rows_loaded     INTEGER DEFAULT 0,
    rows_rejected   INTEGER DEFAULT 0,
    rows_updated    INTEGER DEFAULT 0,

    -- Quality metrics
    null_rate_pct   DECIMAL(5,2),
    duplicate_count INTEGER DEFAULT 0,

    -- Error info
    error_stage     VARCHAR(50),
    error_message   TEXT,

    -- Metadata
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Index for fast lookups
CREATE INDEX idx_metrics_pipeline_date
    ON pipeline_metrics(pipeline_name, run_date);
CREATE INDEX idx_metrics_status
    ON pipeline_metrics(status, run_date);
```

---

## Python Monitoring Class

```python
# src/monitoring/pipeline_monitor.py
import logging
import time
import os
from datetime import datetime, date
from typing import Optional
from sqlalchemy import create_engine, text
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class PipelineRun:
    """Track a single pipeline execution"""
    pipeline_name: str
    run_date: str = field(default_factory=lambda: str(date.today()))
    run_id: str = field(default_factory=lambda:
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    status: str = "running"
    rows_extracted: int = 0
    rows_loaded: int = 0
    rows_rejected: int = 0
    rows_updated: int = 0
    null_rate_pct: float = 0.0
    duplicate_count: int = 0
    error_stage: Optional[str] = None
    error_message: Optional[str] = None

    @property
    def duration_secs(self) -> Optional[int]:
        if self.completed_at:
            return int((self.completed_at - self.started_at).total_seconds())
        return None


class PipelineMonitor:
    """Monitor and log pipeline execution metrics"""

    def __init__(self, db_url: str = None):
        url = db_url or os.getenv("DB_URL")
        self.engine = create_engine(url)

    def start_run(self, pipeline_name: str,
                  run_date: str = None) -> PipelineRun:
        """Start tracking a pipeline run"""
        run = PipelineRun(
            pipeline_name=pipeline_name,
            run_date=run_date or str(date.today())
        )

        with self.engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO pipeline_metrics
                    (run_id, pipeline_name, run_date,
                     started_at, status)
                VALUES (:run_id, :name, :date, :started, 'running')
                ON CONFLICT (run_id) DO NOTHING
            """), {
                "run_id": run.run_id,
                "name": run.pipeline_name,
                "date": run.run_date,
                "started": run.started_at
            })
            conn.commit()

        logger.info(f"▶ Pipeline started: {pipeline_name} [{run.run_id}]")
        return run

    def update_run(self, run: PipelineRun) -> None:
        """Update metrics during run"""
        with self.engine.connect() as conn:
            conn.execute(text("""
                UPDATE pipeline_metrics SET
                    rows_extracted = :extracted,
                    rows_loaded    = :loaded,
                    rows_rejected  = :rejected,
                    rows_updated   = :updated,
                    null_rate_pct  = :null_rate,
                    duplicate_count= :dupes
                WHERE run_id = :run_id
            """), {
                "run_id": run.run_id,
                "extracted": run.rows_extracted,
                "loaded": run.rows_loaded,
                "rejected": run.rows_rejected,
                "updated": run.rows_updated,
                "null_rate": run.null_rate_pct,
                "dupes": run.duplicate_count
            })
            conn.commit()

    def complete_run(self, run: PipelineRun,
                     status: str = "success") -> None:
        """Mark pipeline as complete"""
        run.completed_at = datetime.now()
        run.status = status

        with self.engine.connect() as conn:
            conn.execute(text("""
                UPDATE pipeline_metrics SET
                    completed_at  = :completed,
                    duration_secs = :duration,
                    status        = :status,
                    rows_extracted= :extracted,
                    rows_loaded   = :loaded,
                    rows_rejected = :rejected,
                    error_stage   = :err_stage,
                    error_message = :err_msg
                WHERE run_id = :run_id
            """), {
                "run_id": run.run_id,
                "completed": run.completed_at,
                "duration": run.duration_secs,
                "status": status,
                "extracted": run.rows_extracted,
                "loaded": run.rows_loaded,
                "rejected": run.rows_rejected,
                "err_stage": run.error_stage,
                "err_msg": run.error_message
            })
            conn.commit()

        emoji = "✅" if status == "success" else "❌"
        logger.info(
            f"{emoji} Pipeline {status}: {run.pipeline_name} "
            f"[{run.duration_secs}s] "
            f"{run.rows_loaded:,} rows loaded"
        )


# Usage in pipeline
def run_monitored_pipeline():
    monitor = PipelineMonitor()
    run = monitor.start_run("bank_marketing_etl")

    try:
        # Extract
        df = extract_data()
        run.rows_extracted = len(df)
        monitor.update_run(run)

        # Transform & Load
        df_clean = transform(df)
        rows = load(df_clean)
        run.rows_loaded = rows
        run.rows_rejected = len(df) - rows
        monitor.update_run(run)

        monitor.complete_run(run, "success")

    except Exception as e:
        run.error_stage = "pipeline"
        run.error_message = str(e)
        monitor.complete_run(run, "failed")
        raise
```

---

## Email Alerting

```python
# src/monitoring/alerting.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class AlertManager:
    """Send email and Slack alerts for pipeline events"""

    def __init__(self):
        self.email_from = os.getenv("ALERT_EMAIL_FROM")
        self.email_password = os.getenv("ALERT_EMAIL_PASSWORD")
        self.alert_recipients = os.getenv(
            "ALERT_RECIPIENTS",
            "beatiewakarima1@gmail.com"
        ).split(",")
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

    def send_email(self, subject: str, body_html: str,
                   recipients: list = None) -> bool:
        """Send HTML email alert"""
        recipients = recipients or self.alert_recipients

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.email_from
            msg["To"] = ", ".join(recipients)
            msg.attach(MIMEText(body_html, "html"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.email_from, self.email_password)
                server.sendmail(self.email_from, recipients,
                               msg.as_string())

            logger.info(f"📧 Alert sent to {recipients}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False

    def send_slack(self, message: str, color: str = "good") -> bool:
        """Send Slack notification"""
        if not self.slack_webhook:
            return False
        try:
            import requests
            payload = {
                "attachments": [{
                    "color": color,
                    "text": message,
                    "footer": "Beatrice Builds Data Platform",
                    "ts": datetime.now().timestamp()
                }]
            }
            resp = requests.post(self.slack_webhook, json=payload)
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"Slack alert failed: {e}")
            return False

    def pipeline_success(self, pipeline: str, run_date: str,
                         rows_loaded: int, duration_secs: int):
        """Alert on pipeline success"""
        subject = f"✅ Pipeline Complete — {pipeline} ({run_date})"
        body = f"""
        <div style="font-family: Arial; color: #333;">
            <h2 style="color: #27ae60;">✅ Pipeline Complete</h2>
            <table style="border-collapse: collapse; width: 400px;">
                <tr><td><b>Pipeline:</b></td><td>{pipeline}</td></tr>
                <tr><td><b>Run Date:</b></td><td>{run_date}</td></tr>
                <tr><td><b>Rows Loaded:</b></td>
                    <td>{rows_loaded:,}</td></tr>
                <tr><td><b>Duration:</b></td>
                    <td>{duration_secs}s</td></tr>
            </table>
            <p>
                <a href="https://data-science-learning-vault.vercel.app">
                View Dashboard</a>
            </p>
        </div>
        """
        self.send_email(subject, body)
        self.send_slack(
            f"✅ *{pipeline}* complete — "
            f"{rows_loaded:,} rows in {duration_secs}s",
            color="good"
        )

    def pipeline_failure(self, pipeline: str, run_date: str,
                         error_stage: str, error_message: str):
        """Alert on pipeline failure"""
        subject = f"🚨 PIPELINE FAILED — {pipeline} ({run_date})"
        body = f"""
        <div style="font-family: Arial; color: #333;">
            <h2 style="color: #e74c3c;">🚨 Pipeline Failed</h2>
            <table style="border-collapse: collapse; width: 400px;">
                <tr><td><b>Pipeline:</b></td><td>{pipeline}</td></tr>
                <tr><td><b>Run Date:</b></td><td>{run_date}</td></tr>
                <tr><td><b>Failed Stage:</b></td>
                    <td style="color:red;">{error_stage}</td></tr>
                <tr><td><b>Error:</b></td>
                    <td>{error_message}</td></tr>
            </table>
            <p><b>Action required:</b> Check Airflow logs immediately.</p>
        </div>
        """
        self.send_email(subject, body)
        self.send_slack(
            f"🚨 *{pipeline}* FAILED at `{error_stage}`: "
            f"{error_message}",
            color="danger"
        )

    def data_quality_warning(self, pipeline: str,
                              failed_checks: list):
        """Alert on data quality issues"""
        subject = f"⚠️ Data Quality Warning — {pipeline}"
        checks_html = "".join(
            f"<li style='color:orange;'>{c}</li>"
            for c in failed_checks
        )
        body = f"""
        <div style="font-family: Arial;">
            <h2 style="color: #f39c12;">⚠️ Data Quality Warning</h2>
            <p>Pipeline: <b>{pipeline}</b></p>
            <p>Failed checks:</p>
            <ul>{checks_html}</ul>
            <p>Data may still be loaded but requires review.</p>
        </div>
        """
        self.send_email(subject, body)
```

---

## Monitoring Dashboard Queries

```sql
-- Pipeline health summary (last 30 days)
SELECT
    pipeline_name,
    COUNT(*)                                        AS total_runs,
    COUNT(*) FILTER (WHERE status = 'success')      AS successful,
    COUNT(*) FILTER (WHERE status = 'failed')       AS failed,
    ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'success')
          / COUNT(*), 1)                            AS success_rate_pct,
    ROUND(AVG(duration_secs), 0)                    AS avg_duration_secs,
    ROUND(AVG(rows_loaded), 0)                      AS avg_rows_loaded,
    MAX(run_date)                                   AS last_run_date
FROM pipeline_metrics
WHERE run_date >= CURRENT_DATE - 30
GROUP BY pipeline_name
ORDER BY pipeline_name;

-- Recent failures with error details
SELECT
    run_date,
    pipeline_name,
    error_stage,
    LEFT(error_message, 200)                        AS error_summary,
    started_at,
    duration_secs
FROM pipeline_metrics
WHERE status = 'failed'
  AND run_date >= CURRENT_DATE - 7
ORDER BY started_at DESC;

-- Data volume trends
SELECT
    run_date,
    pipeline_name,
    rows_extracted,
    rows_loaded,
    rows_rejected,
    ROUND(100.0 * rows_rejected / NULLIF(rows_extracted, 0), 1)
                                                    AS rejection_rate_pct
FROM pipeline_metrics
WHERE status = 'success'
  AND run_date >= CURRENT_DATE - 30
ORDER BY run_date DESC, pipeline_name;

-- SLA monitoring — pipelines taking too long
SELECT
    run_date,
    pipeline_name,
    duration_secs,
    ROUND(duration_secs / 60.0, 1)                 AS duration_mins,
    CASE
        WHEN duration_secs > 3600 THEN '🔴 Critical'
        WHEN duration_secs > 1800 THEN '🟡 Warning'
        ELSE '🟢 OK'
    END                                             AS sla_status
FROM pipeline_metrics
WHERE run_date >= CURRENT_DATE - 7
ORDER BY duration_secs DESC;
```

---

## Airflow Monitoring Integration

```python
# dags/monitoring_dag.py
from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

with DAG(
    dag_id="pipeline_monitoring",
    schedule_interval="0 7 * * *",      # Run daily at 7 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["monitoring"]
) as dag:

    @task
    def check_yesterday_pipelines(**context):
        """Verify all pipelines ran successfully yesterday"""
        yesterday = context["yesterday_ds"]
        hook = PostgresHook(postgres_conn_id="postgres_data_vault")

        # Check for failed pipelines
        failed = hook.get_records(f"""
            SELECT pipeline_name, error_stage, error_message
            FROM pipeline_metrics
            WHERE run_date = '{yesterday}'
              AND status = 'failed'
        """)

        # Check for missing pipeline runs
        missing = hook.get_records(f"""
            SELECT unnest(ARRAY[
                'bank_marketing_etl',
                'customer_sync'
            ]) AS expected_pipeline
            EXCEPT
            SELECT pipeline_name FROM pipeline_metrics
            WHERE run_date = '{yesterday}'
              AND status = 'success'
        """)

        if failed or missing:
            alert = AlertManager()
            if failed:
                for pipeline, stage, error in failed:
                    alert.pipeline_failure(
                        pipeline, yesterday, stage, error
                    )
            if missing:
                missing_names = [r[0] for r in missing]
                alert.send_slack(
                    f"⚠️ Pipelines DID NOT RUN yesterday "
                    f"({yesterday}): {missing_names}",
                    color="warning"
                )
            raise ValueError(
                f"Pipeline issues detected: "
                f"{len(failed)} failed, {len(missing)} missing"
            )

        return f"All pipelines healthy for {yesterday}"

    @task
    def check_data_freshness(**context):
        """Verify data is fresh in key tables"""
        hook = PostgresHook(postgres_conn_id="postgres_data_vault")

        stale_tables = hook.get_records("""
            SELECT table_name, last_loaded, hours_since_load
            FROM (VALUES
                ('silver.bank_customers',
                 (SELECT MAX(processed_at) FROM silver.bank_customers)),
                ('gold.campaign_performance',
                 (SELECT MAX(refreshed_at)
                  FROM gold.campaign_performance))
            ) AS t(table_name, last_loaded)
            CROSS JOIN LATERAL (
                SELECT EXTRACT(EPOCH FROM (NOW() - last_loaded))
                       / 3600 AS hours_since_load
            ) AS h
            WHERE hours_since_load > 30
               OR last_loaded IS NULL
        """)

        if stale_tables:
            for table, last_loaded, hours in stale_tables:
                logger.warning(
                    f"⚠️ Stale data: {table} "
                    f"(last loaded {hours:.1f}h ago)"
                )

    check_yesterday_pipelines() >> check_data_freshness()
```

---

## Quick Reference

```python
# Monitor a pipeline run
monitor = PipelineMonitor()
run = monitor.start_run("my_pipeline")
run.rows_extracted = 1000
monitor.update_run(run)
monitor.complete_run(run, "success")

# Send alerts
alerts = AlertManager()
alerts.pipeline_success("bank_etl", "2026-05-20", 45000, 120)
alerts.pipeline_failure("bank_etl", "2026-05-20", "load", "Connection refused")
alerts.data_quality_warning("bank_etl", ["null_check_age", "range_balance"])

# Key metrics to track
rows_extracted      # Source volume
rows_loaded         # Successfully stored
rows_rejected       # Failed validation
duration_secs       # Performance
null_rate_pct       # Data quality
duplicate_count     # Uniqueness
```

---

## Previous | Next
← [[08 - End-to-End Pipeline Project]] | → [[10 - Cloud Data Engineering]]
