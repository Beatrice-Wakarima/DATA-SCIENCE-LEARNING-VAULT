# Secure Database Connections in Python

## Table of Contents

- [[#Environment Setup]]
- [[#Connection Libraries]]
- [[#Secure Connection Methods]]
- [[#MySQL Implementation]]
- [[#PostgreSQL Implementation]]
- [[#Data Loading with Pandas]]
- [[#Streamlit Integration]]
- [[#Security Best Practices]]
- [[#Error Handling]]
- [[#Connection Pooling]]

## Environment Setup

> [!tip] Environment Variables Always use environment variables or [[dotenv]] files to store sensitive database credentials.

Create a `.env` file in your project root:

```bash
# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=your_database
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=your_database
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
```

Install required packages:

```bash
pip install python-dotenv mysql-connector-python psycopg2-binary pandas sqlalchemy
```

## Connection Libraries

|Database|Primary Library|Alternative|[[SQLAlchemy]] Support|
|---|---|---|---|
|MySQL|`mysql-connector-python`|`PyMySQL`|✅|
|PostgreSQL|`psycopg2`|`asyncpg`|✅|

## Secure Connection Methods

### Basic Environment Loading

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_config(db_type):
    """Retrieve database configuration from environment variables"""
    if db_type == 'mysql':
        return {
            'host': os.getenv('MYSQL_HOST'),
            'port': int(os.getenv('MYSQL_PORT', 3306)),
            'database': os.getenv('MYSQL_DATABASE'),
            'user': os.getenv('MYSQL_USER'),
            'password': os.getenv('MYSQL_PASSWORD')
        }
    elif db_type == 'postgres':
        return {
            'host': os.getenv('POSTGRES_HOST'),
            'port': int(os.getenv('POSTGRES_PORT', 5432)),
            'database': os.getenv('POSTGRES_DATABASE'),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD')
        }
```

## MySQL Implementation

### Direct Connection

```python
import mysql.connector
from mysql.connector import Error

def create_mysql_connection():
    """Create secure MySQL connection"""
    try:
        config = get_db_config('mysql')
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            ssl_disabled=False,  # Enable SSL
            autocommit=False,    # Disable autocommit for transaction control
            use_unicode=True,
            charset='utf8mb4'
        )
        
        if connection.is_connected():
            print("MySQL connection established successfully")
            return connection
            
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
```

### SQLAlchemy MySQL Engine

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

def create_mysql_engine():
    """Create MySQL engine with connection pooling"""
    config = get_db_config('mysql')
    
    connection_string = (
        f"mysql+mysqlconnector://{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}/{config['database']}"
        f"?ssl_disabled=false&charset=utf8mb4"
    )
    
    engine = create_engine(
        connection_string,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Validate connections before use
        echo=False  # Set to True for SQL debugging
    )
    
    return engine
```

## PostgreSQL Implementation

### Direct Connection

```python
import psycopg2
from psycopg2 import OperationalError

def create_postgres_connection():
    """Create secure PostgreSQL connection"""
    try:
        config = get_db_config('postgres')
        connection = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            sslmode='prefer',  # Use SSL if available
            connect_timeout=10
        )
        
        print("PostgreSQL connection established successfully")
        return connection
        
    except OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None
```

### SQLAlchemy PostgreSQL Engine

```python
def create_postgres_engine():
    """Create PostgreSQL engine with connection pooling"""
    config = get_db_config('postgres')
    
    connection_string = (
        f"postgresql+psycopg2://{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}/{config['database']}"
        f"?sslmode=prefer"
    )
    
    engine = create_engine(
        connection_string,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        echo=False
    )
    
    return engine
```

## Data Loading with [[pandas]]

### Secure Data Retrieval

```python
import pandas as pd

class SecureDBLoader:
    def __init__(self, db_type='postgres'):
        self.db_type = db_type
        self.engine = self._create_engine()
    
    def _create_engine(self):
        """Create database engine based on type"""
        if self.db_type == 'mysql':
            return create_mysql_engine()
        elif self.db_type == 'postgres':
            return create_postgres_engine()
    
    def load_data(self, query, params=None):
        """Load data using parameterized queries"""
        try:
            # Use parameterized queries to prevent SQL injection
            df = pd.read_sql(
                sql=query,
                con=self.engine,
                params=params
            )
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()
    
    def load_table(self, table_name, limit=None):
        """Load entire table with optional limit"""
        query = f"SELECT * FROM {table_name}"
        if limit:
            query += f" LIMIT {limit}"
        
        return self.load_data(query)

# Usage example
loader = SecureDBLoader('postgres')

# Safe parameterized query
safe_query = "SELECT * FROM users WHERE user_id = %(user_id)s AND status = %(status)s"
params = {'user_id': 123, 'status': 'active'}
df = loader.load_data(safe_query, params)
```

## [[streamlit]] Integration

### Secure Streamlit Database Connection

```python
import streamlit as st
import pandas as pd
from functools import lru_cache

@st.cache_resource
def init_database_connection(db_type):
    """Initialize cached database connection"""
    if db_type == 'mysql':
        return create_mysql_engine()
    elif db_type == 'postgres':
        return create_postgres_engine()

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data_cached(_engine, query, params=None):
    """Load data with caching"""
    return pd.read_sql(query, _engine, params=params)

def streamlit_db_app():
    """Streamlit app with secure database integration"""
    st.title("Secure Database Dashboard")
    
    # Database selection
    db_type = st.selectbox("Select Database", ['postgres', 'mysql'])
    
    # Initialize connection
    engine = init_database_connection(db_type)
    
    # User input with validation
    user_id = st.number_input("User ID", min_value=1, value=1)
    
    if st.button("Load User Data"):
        # Secure parameterized query
        query = "SELECT * FROM users WHERE user_id = %(user_id)s"
        params = {'user_id': user_id}
        
        try:
            df = load_data_cached(engine, query, params)
            
            if not df.empty:
                st.dataframe(df)
            else:
                st.warning("No data found for the specified user.")
                
        except Exception as e:
            st.error(f"Database error: {e}")

if __name__ == "__main__":
    streamlit_db_app()
```

## Security Best Practices

> [!warning] Critical Security Measures Never hardcode credentials or use string concatenation for SQL queries.

### 1. Credential Management

- Use [[dotenv]] files for local development
- Use environment variables in production
- Consider secret management services (AWS Secrets Manager, HashiCorp Vault)

### 2. Connection Security

```python
# MySQL SSL Configuration
mysql_ssl_config = {
    'ssl_ca': '/path/to/ca-cert.pem',
    'ssl_cert': '/path/to/client-cert.pem',
    'ssl_key': '/path/to/client-key.pem',
    'ssl_verify_cert': True
}

# PostgreSQL SSL Configuration
postgres_ssl_config = {
    'sslmode': 'require',
    'sslcert': '/path/to/client-cert.pem',
    'sslkey': '/path/to/client-key.pem',
    'sslrootcert': '/path/to/ca-cert.pem'
}
```

### 3. Query Security

```python
# ❌ NEVER DO THIS - SQL Injection vulnerability
def unsafe_query(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

# ✅ ALWAYS DO THIS - Parameterized queries
def safe_query(user_id):
    query = "SELECT * FROM users WHERE id = %(user_id)s"
    params = {'user_id': user_id}
    return query, params
```

> [!tip] Additional Security Tips
> 
> - Use least privilege principle for database users
> - Enable SSL/TLS encryption
> - Implement connection timeouts
> - Use connection pooling to prevent resource exhaustion
> - Regularly rotate passwords and certificates

## Error Handling

### Comprehensive Error Handling

```python
import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def safe_db_connection(db_type):
    """Context manager for safe database connections"""
    connection = None
    try:
        if db_type == 'mysql':
            connection = create_mysql_connection()
        elif db_type == 'postgres':
            connection = create_postgres_connection()
        
        if connection is None:
            raise ConnectionError(f"Failed to establish {db_type} connection")
        
        yield connection
        
    except Exception as e:
        logger.error(f"Database error: {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if connection:
            connection.close()
            logger.info("Database connection closed")

# Usage
try:
    with safe_db_connection('postgres') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users LIMIT 10")
        results = cursor.fetchall()
except Exception as e:
    print(f"Operation failed: {e}")
```

## Connection Pooling

### Advanced Connection Pool Configuration

```python
from sqlalchemy.pool import StaticPool, QueuePool

def create_production_engine(db_type):
    """Create production-ready engine with optimized pooling"""
    
    base_config = {
        'pool_size': 20,
        'max_overflow': 30,
        'pool_timeout': 30,
        'pool_recycle': 3600,  # Recycle connections every hour
        'pool_pre_ping': True,
        'echo': False
    }
    
    if db_type == 'mysql':
        config = get_db_config('mysql')
        connection_string = (
            f"mysql+mysqlconnector://{config['user']}:{config['password']}"
            f"@{config['host']}:{config['port']}/{config['database']}"
            f"?ssl_disabled=false&charset=utf8mb4"
        )
    else:  # PostgreSQL
        config = get_db_config('postgres')
        connection_string = (
            f"postgresql+psycopg2://{config['user']}:{config['password']}"
            f"@{config['host']}:{config['port']}/{config['database']}"
            f"?sslmode=require"
        )
    
    return create_engine(
        connection_string,
        poolclass=QueuePool,
        **base_config
    )
```

> [!note] Performance Considerations
> 
> - Monitor connection pool metrics
> - Adjust pool size based on application load
> - Use connection pooling for high-traffic applications
> - Implement health checks for database connections

---

**Related Notes:** [[dotenv]], [[pandas]], [[streamlit]], [[SQL Security]], [[SQLAlchemy]], [[Database Performance]]

#mysql #postgresql #security #dotenv #python #pandas #streamlit #database #sqlalchemy #obsidian
up:: [[Data Engineering MOC]]
