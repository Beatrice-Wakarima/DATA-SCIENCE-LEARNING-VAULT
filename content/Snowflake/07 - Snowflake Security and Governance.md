---
title: Snowflake Security and Governance
tags: [snowflake, security, rbac, governance, data-masking]
created: 2026-05-20
up:: [[Snowflake MOC]]
---

# 🔒 Snowflake Security & Governance

> Snowflake's security model is enterprise-grade and granular. Role-Based Access Control (RBAC), Dynamic Data Masking, Row Access Policies, and Column-Level Security give you precise control over who sees what — essential for production data platforms.

---

## Role-Based Access Control (RBAC)

```
Snowflake security hierarchy:

ACCOUNTADMIN           ← Highest privilege (use sparingly!)
    ↓
SECURITYADMIN          ← Manages users and roles
    ↓
SYSADMIN               ← Creates databases, warehouses, objects
    ↓
Custom Roles           ← DATA_ENGINEER, DATA_ANALYST, BI_READER
    ↓
PUBLIC                 ← Default role (all users have this)
```

---

## Creating a Secure Role Hierarchy

```sql
-- Run as SECURITYADMIN
USE ROLE SECURITYADMIN;

-- ── CREATE ROLES ──────────────────────────────────────

-- Data Engineering team
CREATE ROLE IF NOT EXISTS DATA_ENGINEER
    COMMENT = 'Full access to bronze/silver/staging schemas';

-- Data Analytics team
CREATE ROLE IF NOT EXISTS DATA_ANALYST
    COMMENT = 'Read access to silver and gold schemas';

-- BI tools (Power BI service account)
CREATE ROLE IF NOT EXISTS BI_READER
    COMMENT = 'Read-only access to gold schema for BI tools';

-- dbt service account
CREATE ROLE IF NOT EXISTS DBT_TRANSFORMER
    COMMENT = 'dbt transformations — read bronze, write silver/gold';

-- ── CREATE USERS ──────────────────────────────────────

CREATE USER IF NOT EXISTS beatrice_wakarima
    PASSWORD = 'SecurePassword123!'
    DEFAULT_ROLE = DATA_ENGINEER
    DEFAULT_WAREHOUSE = ETL_WH
    DEFAULT_NAMESPACE = DATA_VAULT.SILVER
    MUST_CHANGE_PASSWORD = TRUE
    COMMENT = 'Data Engineer — Beatrice Wakarima';

CREATE USER IF NOT EXISTS dbt_service_account
    PASSWORD = 'DbtServicePassword123!'
    DEFAULT_ROLE = DBT_TRANSFORMER
    DEFAULT_WAREHOUSE = ETL_WH
    COMMENT = 'dbt service account for CI/CD pipeline';

CREATE USER IF NOT EXISTS powerbi_service
    PASSWORD = 'PBIServicePassword123!'
    DEFAULT_ROLE = BI_READER
    DEFAULT_WAREHOUSE = BI_WH
    COMMENT = 'Power BI service account';

-- ── ASSIGN ROLES TO USERS ─────────────────────────────

GRANT ROLE DATA_ENGINEER TO USER beatrice_wakarima;
GRANT ROLE DBT_TRANSFORMER TO USER dbt_service_account;
GRANT ROLE BI_READER TO USER powerbi_service;

-- Role hierarchy (roles can be granted to roles)
GRANT ROLE BI_READER TO ROLE DATA_ANALYST;      -- Analysts get BI access too
GRANT ROLE DATA_ANALYST TO ROLE DATA_ENGINEER;  -- Engineers get analyst access
```

---

## Granting Object Privileges

```sql
-- Run as SYSADMIN
USE ROLE SYSADMIN;

-- ── DATA ENGINEER: Full access to all schemas ──────────

GRANT USAGE ON DATABASE DATA_VAULT TO ROLE DATA_ENGINEER;
GRANT USAGE ON ALL SCHEMAS IN DATABASE DATA_VAULT TO ROLE DATA_ENGINEER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA DATA_VAULT.BRONZE TO ROLE DATA_ENGINEER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA DATA_VAULT.SILVER TO ROLE DATA_ENGINEER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA DATA_VAULT.GOLD TO ROLE DATA_ENGINEER;
GRANT USAGE ON WAREHOUSE ETL_WH TO ROLE DATA_ENGINEER;

-- Future tables get same privileges automatically
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA DATA_VAULT.BRONZE TO ROLE DATA_ENGINEER;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA DATA_VAULT.SILVER TO ROLE DATA_ENGINEER;

-- ── DBT TRANSFORMER: Read bronze, write silver/gold ────

GRANT USAGE ON DATABASE DATA_VAULT TO ROLE DBT_TRANSFORMER;
GRANT USAGE ON SCHEMA DATA_VAULT.BRONZE TO ROLE DBT_TRANSFORMER;
GRANT SELECT ON ALL TABLES IN SCHEMA DATA_VAULT.BRONZE TO ROLE DBT_TRANSFORMER;

GRANT USAGE ON SCHEMA DATA_VAULT.SILVER TO ROLE DBT_TRANSFORMER;
GRANT ALL ON ALL TABLES IN SCHEMA DATA_VAULT.SILVER TO ROLE DBT_TRANSFORMER;
GRANT CREATE TABLE ON SCHEMA DATA_VAULT.SILVER TO ROLE DBT_TRANSFORMER;
GRANT CREATE VIEW ON SCHEMA DATA_VAULT.SILVER TO ROLE DBT_TRANSFORMER;

GRANT USAGE ON SCHEMA DATA_VAULT.GOLD TO ROLE DBT_TRANSFORMER;
GRANT ALL ON ALL TABLES IN SCHEMA DATA_VAULT.GOLD TO ROLE DBT_TRANSFORMER;
GRANT CREATE TABLE ON SCHEMA DATA_VAULT.GOLD TO ROLE DBT_TRANSFORMER;

GRANT USAGE ON WAREHOUSE ETL_WH TO ROLE DBT_TRANSFORMER;

-- Future grants
GRANT SELECT ON FUTURE TABLES IN SCHEMA DATA_VAULT.BRONZE TO ROLE DBT_TRANSFORMER;
GRANT ALL ON FUTURE TABLES IN SCHEMA DATA_VAULT.SILVER TO ROLE DBT_TRANSFORMER;
GRANT ALL ON FUTURE TABLES IN SCHEMA DATA_VAULT.GOLD TO ROLE DBT_TRANSFORMER;

-- ── BI READER: Read-only gold schema ──────────────────

GRANT USAGE ON DATABASE DATA_VAULT TO ROLE BI_READER;
GRANT USAGE ON SCHEMA DATA_VAULT.GOLD TO ROLE BI_READER;
GRANT SELECT ON ALL TABLES IN SCHEMA DATA_VAULT.GOLD TO ROLE BI_READER;
GRANT SELECT ON ALL VIEWS IN SCHEMA DATA_VAULT.GOLD TO ROLE BI_READER;
GRANT USAGE ON WAREHOUSE BI_WH TO ROLE BI_READER;

GRANT SELECT ON FUTURE TABLES IN SCHEMA DATA_VAULT.GOLD TO ROLE BI_READER;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA DATA_VAULT.GOLD TO ROLE BI_READER;
```

---

## Dynamic Data Masking

```sql
-- Dynamic masking shows different data to different roles
-- The table stores real data; the policy controls visibility

-- ── CREATE MASKING POLICIES ───────────────────────────

-- Mask email addresses (show only domain for non-privileged users)
CREATE MASKING POLICY mask_email
    AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('DATA_ENGINEER', 'SYSADMIN')
            THEN val                                    -- Full email
        WHEN CURRENT_ROLE() = 'DATA_ANALYST'
            THEN REGEXP_REPLACE(val, '^[^@]+', '***')  -- ***@domain.com
        ELSE '***@***.***'                             -- Fully masked
    END;

-- Mask phone numbers
CREATE MASKING POLICY mask_phone
    AS (val STRING) RETURNS STRING ->
    CASE
        WHEN CURRENT_ROLE() IN ('DATA_ENGINEER', 'SYSADMIN') THEN val
        ELSE LEFT(val, 3) || '****' || RIGHT(val, 2)
    END;

-- Mask financial data (show ranges instead of exact values)
CREATE MASKING POLICY mask_balance
    AS (val NUMBER) RETURNS NUMBER ->
    CASE
        WHEN CURRENT_ROLE() IN ('DATA_ENGINEER', 'SYSADMIN') THEN val
        WHEN CURRENT_ROLE() = 'DATA_ANALYST'
            THEN ROUND(val / 10000) * 10000            -- Round to nearest 10K
        ELSE NULL                                       -- Hide completely
    END;

-- ── APPLY POLICIES TO COLUMNS ─────────────────────────

-- Apply to customers table
ALTER TABLE DATA_VAULT.SILVER.BANK_CUSTOMERS
    MODIFY COLUMN email
    SET MASKING POLICY mask_email;

ALTER TABLE DATA_VAULT.SILVER.BANK_CUSTOMERS
    MODIFY COLUMN balance
    SET MASKING POLICY mask_balance;

-- Test: Different roles see different data
USE ROLE BI_READER;
SELECT customer_sk, email, balance FROM SILVER.BANK_CUSTOMERS LIMIT 3;
-- email: ***@***.***  balance: NULL

USE ROLE DATA_ANALYST;
SELECT customer_sk, email, balance FROM SILVER.BANK_CUSTOMERS LIMIT 3;
-- email: ***@gmail.com  balance: 90000 (rounded)

USE ROLE DATA_ENGINEER;
SELECT customer_sk, email, balance FROM SILVER.BANK_CUSTOMERS LIMIT 3;
-- email: beatrice@gmail.com  balance: 95230 (exact)
```

---

## Row Access Policies

```sql
-- Row access policies control WHICH ROWS a role can see
-- Useful for multi-tenant data, regional access control

-- Create a mapping table
CREATE TABLE DATA_VAULT.REFERENCE.ROLE_REGION_ACCESS (
    role_name   VARCHAR(100),
    region      VARCHAR(50)
);

INSERT INTO DATA_VAULT.REFERENCE.ROLE_REGION_ACCESS VALUES
    ('DATA_ENGINEER', 'Nairobi'),
    ('DATA_ENGINEER', 'Mombasa'),
    ('DATA_ENGINEER', 'Kisumu'),
    ('NAIROBI_ANALYST', 'Nairobi'),
    ('COAST_ANALYST', 'Mombasa');

-- Create row access policy
CREATE ROW ACCESS POLICY region_access_policy
    AS (city VARCHAR) RETURNS BOOLEAN ->
    EXISTS (
        SELECT 1
        FROM DATA_VAULT.REFERENCE.ROLE_REGION_ACCESS
        WHERE role_name = CURRENT_ROLE()
          AND region = city
    );

-- Apply to table
ALTER TABLE DATA_VAULT.SILVER.BANK_CUSTOMERS
    ADD ROW ACCESS POLICY region_access_policy ON (city);

-- Now:
-- DATA_ENGINEER sees all regions
-- NAIROBI_ANALYST sees only Nairobi customers
-- COAST_ANALYST sees only Mombasa customers
```

---

## Column-Level Security (Object Tagging)

```sql
-- Tag sensitive columns for governance tracking

-- Create tags
CREATE TAG DATA_VAULT.GOVERNANCE.PII
    COMMENT = 'Personally Identifiable Information';

CREATE TAG DATA_VAULT.GOVERNANCE.FINANCIAL
    COMMENT = 'Financial/sensitive data';

-- Apply tags to columns
ALTER TABLE DATA_VAULT.SILVER.BANK_CUSTOMERS
    MODIFY COLUMN email SET TAG DATA_VAULT.GOVERNANCE.PII = 'email';

ALTER TABLE DATA_VAULT.SILVER.BANK_CUSTOMERS
    MODIFY COLUMN balance SET TAG DATA_VAULT.GOVERNANCE.FINANCIAL = 'account_balance';

-- Query tagged columns across the account
SELECT
    table_name,
    column_name,
    tag_name,
    tag_value
FROM TABLE(SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES_ALL_COLUMNS(
    'DATA_VAULT.SILVER.BANK_CUSTOMERS',
    'table'
));

-- Find all PII columns in account
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES
WHERE tag_name = 'PII'
ORDER BY table_name;
```

---

## Network Policies — IP Restrictions

```sql
-- Restrict access to specific IP ranges

CREATE NETWORK POLICY office_access_only
    ALLOWED_IP_LIST = (
        '197.232.0.0/16',       -- Nairobi office range
        '41.215.0.0/16',        -- Backup range
        '10.0.0.0/8'            -- VPN
    )
    BLOCKED_IP_LIST = ()
    COMMENT = 'Only allow connections from office/VPN IPs';

-- Apply to specific user
ALTER USER powerbi_service
    SET NETWORK_POLICY = office_access_only;

-- Apply to entire account (careful!)
ALTER ACCOUNT SET NETWORK_POLICY = office_access_only;

-- Remove policy
ALTER USER powerbi_service UNSET NETWORK_POLICY;
```

---

## Multi-Factor Authentication (MFA)

```sql
-- Enforce MFA for sensitive roles

-- Check MFA status for users
SELECT name, has_mfa
FROM SNOWFLAKE.ACCOUNT_USAGE.USERS
WHERE has_mfa = FALSE
  AND DISABLED = FALSE;

-- Enforce MFA policy (Enterprise+)
CREATE AUTHENTICATION POLICY require_mfa
    MFA_AUTHENTICATION_METHODS = ('PASSWORD')
    MFA_ENROLLMENT = REQUIRED
    COMMENT = 'Require MFA for all logins';

-- Apply to user
ALTER USER beatrice_wakarima
    SET AUTHENTICATION POLICY require_mfa;
```

---

## Audit Logging

```sql
-- Everything is logged in SNOWFLAKE.ACCOUNT_USAGE

-- Login history
SELECT
    user_name,
    event_timestamp,
    is_success,
    error_code,
    error_message,
    client_application_id
FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
WHERE event_timestamp >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())
  AND is_success = 'NO'           -- Failed logins
ORDER BY event_timestamp DESC;

-- Who accessed what data?
SELECT
    user_name,
    role_name,
    LEFT(query_text, 200)         AS query_preview,
    start_time,
    database_name,
    schema_name
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD(DAY, -1, CURRENT_TIMESTAMP())
  AND query_text ILIKE '%bank_customers%'
ORDER BY start_time DESC;

-- Privilege changes audit
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_USERS
WHERE granted_on >= DATEADD(DAY, -30, CURRENT_TIMESTAMP())
ORDER BY granted_on DESC;
```

---

## Security Best Practices

```
Account:
  ✅ Use ACCOUNTADMIN only for account-level tasks
  ✅ Create custom roles — never use SYSADMIN for daily work
  ✅ Enable MFA for all human users
  ✅ Use Network Policies to restrict IP access
  ✅ Rotate passwords/keys regularly

Roles:
  ✅ Principle of least privilege
  ✅ Separate roles for ETL, Analytics, BI
  ✅ Service accounts have their own roles
  ✅ Never share credentials

Data:
  ✅ Dynamic masking on PII columns
  ✅ Row access policies for multi-tenant data
  ✅ Tag sensitive columns for governance
  ✅ Encrypt data at rest and in transit (automatic in Snowflake)

Monitoring:
  ✅ Regular audit of QUERY_HISTORY
  ✅ Alert on failed logins
  ✅ Review GRANTS_TO_USERS monthly
  ✅ Monitor for unusual data access patterns
```

---

## Quick Reference

```sql
-- Roles
CREATE ROLE role_name;
GRANT ROLE role_name TO USER username;
GRANT ROLE role_name TO ROLE parent_role;
GRANT privilege ON object TO ROLE role_name;
GRANT SELECT ON FUTURE TABLES IN SCHEMA s TO ROLE r;
SHOW GRANTS TO ROLE role_name;
SHOW GRANTS ON TABLE table_name;

-- Masking
CREATE MASKING POLICY policy_name AS (val TYPE) RETURNS TYPE -> CASE...;
ALTER TABLE t MODIFY COLUMN c SET MASKING POLICY policy_name;
ALTER TABLE t MODIFY COLUMN c UNSET MASKING POLICY;

-- Row access
CREATE ROW ACCESS POLICY policy AS (col TYPE) RETURNS BOOLEAN -> condition;
ALTER TABLE t ADD ROW ACCESS POLICY policy ON (col);
ALTER TABLE t DROP ROW ACCESS POLICY policy;

-- Network
CREATE NETWORK POLICY p ALLOWED_IP_LIST = ('x.x.x.x/24');
ALTER USER u SET NETWORK_POLICY = p;
ALTER ACCOUNT SET NETWORK_POLICY = p;

-- Audit
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY;
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY;
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_USERS;
```

---

## Previous | Next
← [[06 - Snowflake Time Travel and Cloning]] | → [[08 - Snowflake with dbt and Python]]
