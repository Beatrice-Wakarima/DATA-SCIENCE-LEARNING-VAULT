---
title: Python for Automation
tags: [python, automation, data-engineering, airflow]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🤖 Python for Automation

> Automation is where Python shines brightest — scheduled pipelines, email reports, file processing, and workflow orchestration with Airflow.

---

## Scheduling with `schedule`

```python
pip install schedule

import schedule
import time

def run_daily_pipeline():
    print("🚀 Running daily ETL pipeline...")
    # Your pipeline code here

def send_morning_report():
    print("📧 Sending morning report...")

def cleanup_temp_files():
    print("🧹 Cleaning temp files...")

# Schedule tasks
schedule.every().day.at("06:00").do(run_daily_pipeline)
schedule.every().day.at("08:30").do(send_morning_report)
schedule.every().monday.at("09:00").do(cleanup_temp_files)
schedule.every(30).minutes.do(run_daily_pipeline)     # Every 30 mins
schedule.every().hour.do(cleanup_temp_files)

# Keep running
print("⏰ Scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)          # Check every minute
```

---

## Automating Emails

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_report_email(recipient, subject, body, attachment_path=None):
    """Send automated email report"""
    
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")   # Use App Password for Gmail
    
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    
    # Email body (HTML supported)
    html_body = f"""
    <html>
    <body style="font-family: Arial; color: #333;">
        <h2 style="color: #c9a84c;">📊 Automated Data Report</h2>
        <p>{body}</p>
        <hr>
        <p style="color: #888; font-size: 12px;">
            Sent automatically by Beatrice Builds Pipeline
        </p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, "html"))
    
    # Attach file
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",
                          f"attachment; filename={os.path.basename(attachment_path)}")
            msg.attach(part)
    
    # Send
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
    
    print(f"✅ Email sent to {recipient}")

# Use it
send_report_email(
    recipient="manager@company.com",
    subject="Daily Sales Report — May 2026",
    body="Please find today's sales report attached.",
    attachment_path="outputs/daily_report.xlsx"
)
```

---

## File Automation

```python
import os
import shutil
from pathlib import Path
from datetime import datetime

def organize_downloads(download_folder):
    """Auto-organize files by type"""
    
    folder = Path(download_folder)
    
    categories = {
        "Data": [".csv", ".xlsx", ".json", ".parquet", ".sql"],
        "Documents": [".pdf", ".docx", ".txt", ".pptx"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
        "Scripts": [".py", ".sql", ".sh", ".r"],
        "Archives": [".zip", ".tar", ".gz"]
    }
    
    moved = 0
    for file in folder.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            
            for category, extensions in categories.items():
                if ext in extensions:
                    dest = folder / category
                    dest.mkdir(exist_ok=True)
                    shutil.move(str(file), str(dest / file.name))
                    print(f"Moved: {file.name} → {category}/")
                    moved += 1
                    break
    
    print(f"✅ Organized {moved} files")

# Run it
organize_downloads("/c/Users/iescpcadmin/Desktop/Data_Science_Learning_Vault")
```

---

## Automating Excel Reports

```python
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference
from pathlib import Path
from datetime import datetime

def create_sales_report(data, output_path):
    """Generate a formatted Excel sales report"""
    
    df = pd.DataFrame(data)
    
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Sales Data", index=False)
        
        ws = writer.sheets["Sales Data"]
        
        # Style header row
        header_fill = PatternFill(fill_type="solid", fgColor="1a1a2e")
        header_font = Font(color="c9a84c", bold=True, size=12)
        
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")
        
        # Auto-fit columns
        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = max_len + 4
        
        # Add summary sheet
        summary_data = {
            "Metric": ["Total Revenue", "Total Units", "Avg Sale", "Best Month"],
            "Value": [
                f"KES {df['revenue'].sum():,.0f}",
                f"{df['units'].sum():,}",
                f"KES {df['revenue'].mean():,.0f}",
                df.loc[df['revenue'].idxmax(), 'month']
            ]
        }
        pd.DataFrame(summary_data).to_excel(
            writer, sheet_name="Summary", index=False
        )
    
    print(f"✅ Report saved: {output_path}")

# Sample data
sales_data = {
    "month": ["Jan","Feb","Mar","Apr","May","Jun"],
    "revenue": [420000, 385000, 510000, 490000, 620000, 580000],
    "units": [140, 128, 170, 163, 207, 193],
    "region": ["Nairobi"]*6
}

create_sales_report(sales_data, "outputs/sales_report.xlsx")
```

---

## Apache Airflow — Intro

```python
# Airflow orchestrates complex data pipelines as DAGs
# DAG = Directed Acyclic Graph (a sequence of tasks)

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments
default_args = {
    "owner": "beatrice",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email": ["beatiewakarima1@gmail.com"],
    "email_on_failure": True
}

# Define the DAG
with DAG(
    dag_id="bank_marketing_pipeline",
    default_args=default_args,
    description="Daily bank marketing ETL pipeline",
    schedule_interval="0 6 * * *",      # Run daily at 6am
    catchup=False,
    tags=["bank", "etl", "daily"]
) as dag:
    
    # Task functions
    def extract_task():
        import pandas as pd
        df = pd.read_csv("data/bank_marketing.csv")
        df.to_parquet("data/processed/raw.parquet")
        print(f"Extracted {len(df):,} rows")
    
    def transform_task():
        import pandas as pd
        df = pd.read_parquet("data/processed/raw.parquet")
        df = df.drop_duplicates().dropna()
        df.to_parquet("data/processed/clean.parquet")
        print(f"Transformed: {len(df):,} rows")
    
    def load_task():
        import pandas as pd
        df = pd.read_parquet("data/processed/clean.parquet")
        df.to_csv("data/outputs/final.csv", index=False)
        print(f"Loaded {len(df):,} rows")
    
    def notify_task():
        print("📧 Sending completion notification...")
        # send_report_email(...)
    
    # Define tasks
    t1 = PythonOperator(task_id="extract", python_callable=extract_task)
    t2 = PythonOperator(task_id="transform", python_callable=transform_task)
    t3 = PythonOperator(task_id="load", python_callable=load_task)
    t4 = PythonOperator(task_id="notify", python_callable=notify_task)
    
    # Set order: extract → transform → load → notify
    t1 >> t2 >> t3 >> t4
```

---

## Cron Schedule Syntax

```
# ┌─── minute (0-59)
# │ ┌─── hour (0-23)
# │ │ ┌─── day of month (1-31)
# │ │ │ ┌─── month (1-12)
# │ │ │ │ ┌─── day of week (0=Sun, 6=Sat)
# │ │ │ │ │
# * * * * *

"0 6 * * *"       # Daily at 6:00 AM
"0 6 * * 1"       # Every Monday at 6:00 AM
"0 8,17 * * *"    # 8 AM and 5 PM daily
"*/30 * * * *"    # Every 30 minutes
"0 0 1 * *"       # First day of every month at midnight
"0 6 * * 1-5"     # Weekdays at 6 AM
```

---

## Complete Automation Example

```python
"""
Daily data pipeline automation
Runs at 6 AM, processes data, emails report
"""
import schedule
import time
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(message)s")
logger = logging.getLogger("automation")

def daily_pipeline():
    logger.info("🚀 Starting daily pipeline")
    
    try:
        # 1. Extract
        df = pd.read_csv("data/sales.csv", parse_dates=["date"])
        logger.info(f"Extracted {len(df):,} records")
        
        # 2. Filter today's data
        today = datetime.now().date()
        today_df = df[df["date"].dt.date == today]
        logger.info(f"Today's records: {len(today_df)}")
        
        # 3. Calculate KPIs
        kpis = {
            "date": str(today),
            "revenue": today_df["amount"].sum(),
            "transactions": len(today_df),
            "avg_transaction": today_df["amount"].mean()
        }
        
        # 4. Save report
        Path("outputs").mkdir(exist_ok=True)
        pd.DataFrame([kpis]).to_csv(
            f"outputs/daily_{today}.csv", index=False
        )
        
        # 5. Send email
        body = f"""
        Date: {today}
        Revenue: KES {kpis['revenue']:,.0f}
        Transactions: {kpis['transactions']:,}
        Avg Transaction: KES {kpis['avg_transaction']:,.0f}
        """
        # send_report_email("manager@company.com", f"Daily Report {today}", body)
        
        logger.info("✅ Pipeline complete")
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {e}")

# Schedule
schedule.every().day.at("06:00").do(daily_pipeline)

logger.info("⏰ Automation started")
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Automation Toolkit Summary

| Tool | Use Case |
|---|---|
| `schedule` | Simple scheduled Python jobs |
| `cron` | Linux/Mac system scheduling |
| `Task Scheduler` | Windows scheduling |
| `Apache Airflow` | Complex pipeline orchestration |
| `Prefect` | Modern pipeline orchestration |
| `smtplib` | Automated email sending |
| `shutil/pathlib` | File automation |
| `watchdog` | File system event monitoring |

---

## Previous | Next
← [[19 - Virtual Environments and Project Structure]] | → [[Python MOC]]
