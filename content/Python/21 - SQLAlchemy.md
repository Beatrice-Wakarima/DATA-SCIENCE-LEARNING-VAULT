---
title: SQLAlchemy — Python + Databases
tags: [python, sql, databases, data-engineering]
created: 2026-05-20
up:: [[Python MOC]]
---

# 🗄️ SQLAlchemy — Python + Databases

> SQLAlchemy is the industry-standard Python library for working with databases. It lets you connect to PostgreSQL, MySQL, SQLite and more — using Python instead of raw SQL strings.

---

## Installation

```bash
pip install sqlalchemy psycopg2-binary  # PostgreSQL
pip install sqlalchemy                  # SQLite (built-in)
```

---

## Connection Strings

```python
from sqlalchemy import create_engine

# SQLite (local file — great for testing)
engine = create_engine("sqlite:///my_database.db")

# PostgreSQL
engine = create_engine("postgresql://username:password@localhost:5432/dbname")

# With environment variables (production best practice)
import os
from dotenv import load_dotenv
load_dotenv()

DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URL)

# MySQL
engine = create_engine("mysql+pymysql://user:password@localhost/dbname")

# Test connection
with engine.connect() as conn:
    print("✅ Connected to database!")
```

---

## Pandas + SQLAlchemy — The Power Combo

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://beatrice:password@localhost:5432/sales_db")

# Read entire table into DataFrame
df = pd.read_sql_table("customers", engine)

# Run SQL query → DataFrame
df = pd.read_sql("""
    SELECT 
        c.customer_id,
        c.name,
        c.tier,
        COUNT(t.transaction_id) AS total_transactions,
        SUM(t.amount) AS total_spend
    FROM customers c
    LEFT JOIN transactions t ON c.customer_id = t.customer_id
    WHERE c.is_active = TRUE
    GROUP BY c.customer_id, c.name, c.tier
    ORDER BY total_spend DESC
    LIMIT 100
""", engine)

print(df.head())
print(f"Loaded {len(df):,} customers")

# Write DataFrame to database
df_clean.to_sql(
    name="customers_clean",
    con=engine,
    if_exists="replace",    # or "append" or "fail"
    index=False,
    chunksize=1000          # Write in batches
)
print("✅ Data written to database")
```

---

## Core SQLAlchemy — Running SQL

```python
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://beatrice:password@localhost:5432/sales_db")

# Execute raw SQL
with engine.connect() as conn:
    
    # SELECT
    result = conn.execute(text("SELECT * FROM customers LIMIT 5"))
    for row in result:
        print(row)
    
    # INSERT
    conn.execute(text("""
        INSERT INTO customers (name, email, tier, balance)
        VALUES (:name, :email, :tier, :balance)
    """), {
        "name": "Beatrice Wakarima",
        "email": "beatrice@gmail.com",
        "tier": "Gold",
        "balance": 95000
    })
    conn.commit()
    
    # UPDATE
    conn.execute(text("""
        UPDATE customers 
        SET tier = 'Platinum', updated_at = NOW()
        WHERE balance > 100000
    """))
    conn.commit()
    
    # DELETE
    conn.execute(text("DELETE FROM temp_staging WHERE created_at < NOW() - INTERVAL '7 days'"))
    conn.commit()
```

---

## ORM — Define Tables as Python Classes

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime

Base = declarative_base()

# Define table as a Python class
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    tier = Column(String(20), default="Bronze")
    balance = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Customer(id={self.id}, name={self.name}, tier={self.tier})"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables in database
engine = create_engine("sqlite:///bank.db")
Base.metadata.create_all(engine)
print("✅ Tables created!")
```

---

## ORM — CRUD Operations

```python
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///bank.db")

# CREATE — Add records
with Session(engine) as session:
    new_customer = Customer(
        name="Beatrice Wakarima",
        email="beatrice@gmail.com",
        tier="Gold",
        balance=95000
    )
    session.add(new_customer)
    
    # Add multiple at once
    customers = [
        Customer(name="John Doe", email="john@gmail.com", balance=45000),
        Customer(name="Alice Smith", email="alice@gmail.com", tier="Platinum", balance=250000)
    ]
    session.add_all(customers)
    session.commit()
    print("✅ Customers added")

# READ — Query records
with Session(engine) as session:
    
    # All customers
    all_customers = session.query(Customer).all()
    
    # Filter
    premium = session.query(Customer).filter(Customer.balance > 100000).all()
    
    # First match
    beatrice = session.query(Customer).filter_by(name="Beatrice Wakarima").first()
    print(beatrice)
    
    # Count
    total = session.query(Customer).count()
    print(f"Total customers: {total}")
    
    # Order
    top_customers = session.query(Customer)\
                           .order_by(Customer.balance.desc())\
                           .limit(10).all()

# UPDATE
with Session(engine) as session:
    customer = session.query(Customer).filter_by(email="beatrice@gmail.com").first()
    customer.balance += 50000
    customer.tier = "Platinum"
    session.commit()
    print("✅ Customer updated")

# DELETE
with Session(engine) as session:
    inactive = session.query(Customer).filter_by(is_active=False).all()
    for c in inactive:
        session.delete(c)
    session.commit()
    print(f"✅ Deleted {len(inactive)} inactive customers")
```

---

## Real World Example — Bank Marketing Pipeline

```python
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class BankDataWarehouse:
    """Load bank marketing data into PostgreSQL warehouse"""
    
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        logger.info("Connected to data warehouse")
    
    def load_staging(self, csv_path):
        """Load CSV into staging table"""
        df = pd.read_csv(csv_path)
        df.to_sql("stg_bank_marketing", self.engine,
                  if_exists="replace", index=False)
        logger.info(f"Loaded {len(df):,} rows to staging")
        return df
    
    def run_transformations(self):
        """Run SQL transformations on staged data"""
        with self.engine.connect() as conn:
            
            # Create clean customers table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS dim_customers AS
                SELECT DISTINCT
                    ROW_NUMBER() OVER() AS customer_id,
                    age,
                    job,
                    marital,
                    education,
                    CASE 
                        WHEN balance > 10000 THEN 'High'
                        WHEN balance > 1000  THEN 'Medium'
                        ELSE 'Low'
                    END AS balance_segment
                FROM stg_bank_marketing
            """))
            
            # Create campaign facts table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS fact_campaigns AS
                SELECT
                    campaign,
                    contact,
                    month,
                    COUNT(*) AS contacts_made,
                    SUM(CASE WHEN y = 'yes' THEN 1 ELSE 0 END) AS subscriptions,
                    ROUND(
                        100.0 * SUM(CASE WHEN y = 'yes' THEN 1 ELSE 0 END) / COUNT(*), 2
                    ) AS conversion_rate
                FROM stg_bank_marketing
                GROUP BY campaign, contact, month
            """))
            
            conn.commit()
            logger.info("✅ Transformations complete")
    
    def get_kpis(self):
        """Fetch KPI summary"""
        return pd.read_sql("""
            SELECT 
                month,
                SUM(contacts_made) AS total_contacts,
                SUM(subscriptions) AS total_subscriptions,
                ROUND(AVG(conversion_rate), 2) AS avg_conversion_rate
            FROM fact_campaigns
            GROUP BY month
            ORDER BY total_subscriptions DESC
        """, self.engine)


# Run it
dw = BankDataWarehouse("postgresql://beatrice:pass@localhost:5432/bank_dw")
dw.load_staging("data/bank_marketing.csv")
dw.run_transformations()
kpis = dw.get_kpis()
print(kpis)
```

---

## Connection Pooling (Production)

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Production engine with connection pooling
engine = create_engine(
    "postgresql://beatrice:password@localhost:5432/sales_db",
    poolclass=QueuePool,
    pool_size=5,            # Keep 5 connections open
    max_overflow=10,        # Allow 10 extra in peak
    pool_timeout=30,        # Wait max 30s for connection
    pool_recycle=1800,      # Recycle connections every 30min
    echo=False              # Set True to log all SQL
)
```

---

## Quick Reference

```python
# Connect
engine = create_engine("dialect://user:pass@host:port/db")

# Pandas integration
pd.read_sql("SELECT ...", engine)
pd.read_sql_table("tablename", engine)
df.to_sql("tablename", engine, if_exists="replace")

# Raw SQL
with engine.connect() as conn:
    result = conn.execute(text("SELECT ..."))
    conn.execute(text("INSERT ..."), params)
    conn.commit()

# ORM
Base = declarative_base()
class MyTable(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True)
    name = Column(String)

with Session(engine) as session:
    session.add(MyTable(name="test"))
    session.query(MyTable).filter_by(name="test").first()
    session.commit()
```

---

## Previous | Next
← [[20 - Python for Automation]] | → [[22 - FastAPI — Building Data APIs]]
