## Security Hardening for PostgreSQL in Docker

### 🎯 Why It Matters

- Protects sensitive data from unauthorized access
    
- Reduces attack surface in containerized environments
    
- Aligns with compliance standards (e.g., GDPR, HIPAA)
    

> 🔗 Backlink: [[best practices]] | [[backup strategy]] | [[pg_hba.conf]]

### 🔑 1. Use Strong, Unique Passwords

#### 🧬 Generate Secure Password

bash

```
export POSTGRES_PASSWORD=$(openssl rand -base64 32)
echo "$POSTGRES_PASSWORD" > postgres-password.txt
```

- Avoid default or weak credentials
    
- Store securely (e.g., `.env`, password manager)
    

> 🔗 Backlink: [[Environment Variables]] | [[PostgreSQL Setup]]

### 🌐 2. Restrict Network Access

#### 🧱 Bind to Localhost

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 127.0.0.1:5432:5432 \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres
```

- Prevents external machines from connecting
    
- Ideal for local dev and CI/CD pipelines
    

> 🔗 Backlink: [[Networking]] | [[pgAdmin Integration]]

### 🧾 3. Harden PostgreSQL Configuration

#### 🔧 Sample `postgresql.conf`

conf

```
ssl = on
ssl_cert_file = '/etc/ssl/certs/ssl-cert.pem'
ssl_key_file = '/etc/ssl/private/ssl-key.pem'
max_connections = 100
authentication_timeout = 1min
listen_addresses = 'localhost'
```

#### 📦 Mount Config Files

bash

```
docker run --name postgres-db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v ./pg_hba.conf:/var/lib/postgresql/data/pg_hba.conf \
  -v ./postgresql.conf:/var/lib/postgresql/data/postgresql.conf \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres
```

> 🔗 Backlink: [[postgresql.conf]] | [[pg_hba.conf]] | [[Volumes]]

### 🔁 4. Keep PostgreSQL Updated

bash

```
docker pull postgres:latest
docker stop postgres-db
docker rm postgres-db
# Recreate with latest image
```

- Apply security patches and bug fixes
    
- Review release notes before upgrading
    

> 🔗 Backlink: [[Upgrade Workflow]] | [[Maintenance]]