## 🧠 Python + PostgreSQL with psycopg2: FAQ Summary

### 🧬 1. psycopg2 vs psycopg2-binary

- `psycopg2`: Source build; allows custom compilation and debugging
    
- `psycopg2-binary`: Precompiled wheel; faster install, but not recommended for production due to potential binary incompatibilities
    

> 🔗 Backlink: [[Environment Setup]] | [[Dependencies]]

### 🛡️ 2. Handling Connection Errors

Use `try/except` blocks with `psycopg2.Error` or specific subclasses:

python

```
import psycopg2
try:
    conn = psycopg2.connect(...)
except psycopg2.OperationalError as e:
    print("Connection failed:", e)
```

> 🔗 Backlink: [[Troubleshooting]] | [[Connection Management]]

### 🌐 3. Connecting to Remote PostgreSQL

python

```
psycopg2.connect(
    host="remote.host.com",
    port=5432,
    dbname="mydb",
    user="myuser",
    password="mypassword"
)
```

Ensure:

- Remote DB allows external connections
    
- Firewall and `pg_hba.conf` are configured
    

> 🔗 Backlink: [[Networking]] | [[Security Hardening]]

### 🔐 4. Using Environment Variables

python

```
import os
psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)
```

Store credentials in `.env` or secret manager; never hardcode

> 🔗 Backlink: [[Security Hardening]] | [[Environment Variables]]

### 🧼 5. Preventing SQL Injection

Use parameterized queries:

python

```
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

Avoid string interpolation or f-strings for SQL

> 🔗 Backlink: [[Security Hardening]] | [[Query Safety]]

### 🔁 6. Updating Multiple Rows

Use `executemany()` or batch logic:

python

```
updates = [(new_val1, id1), (new_val2, id2)]
cursor.executemany("UPDATE table SET col = %s WHERE id = %s", updates)
```

> 🔗 Backlink: [[Bulk Operations]] | [[Data Manipulation]]

### 🧮 7. PostgreSQL ↔ Python Data Types

|PostgreSQL|Python|
|---|---|
|INTEGER|int|
|TEXT/VARCHAR|str|
|BOOLEAN|bool|
|DATE/TIMESTAMP|datetime.date / datetime.datetime|
|JSON/JSONB|dict / str|
|BYTEA|bytes|

> 🔗 Backlink: [[Data Types]] | [[Schema Mapping]]

### 📤 8. Export to CSV

python

```
import csv
cursor.execute("SELECT * FROM mytable")
with open("export.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([desc[0] for desc in cursor.description])
    writer.writerows(cursor.fetchall())
```

> 🔗 Backlink: [[Data Export]] | [[Reporting]]

### 📓 9. Using Jupyter Notebook

Yes! Install `psycopg2` in your Jupyter environment and run queries interactively. Great for prototyping and analysis.

> 🔗 Backlink: [[Notebook Workflows]] | [[Exploratory Analysis]]

### 🐞 10. Debugging SQL Failures

- Print full query and parameters
    
- Use `EXPLAIN` or `EXPLAIN ANALYZE` in PostgreSQL
    
- Catch exceptions and log stack traces
    
- Enable verbose logging in PostgreSQL
    

> 🔗 Backlink: [[Troubleshooting]] | [[Query Optimization]]