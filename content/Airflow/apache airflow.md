# Apache Airflow

_Open-source platform for developing, scheduling, and monitoring workflows_

## Overview

**Apache Airflow** is a platform to programmatically author, schedule, and monitor workflows. Developed by Airbnb and now an Apache Software Foundation project, Airflow allows you to define workflows as code using [[Python]] and provides a rich [[Web Interface]] for monitoring and managing [[DAGs]].

> [!note] Core Philosophy Workflows are defined as code (Python), making them maintainable, versionable, testable, and collaborative.

## Key Concepts

### DAGs (Directed Acyclic Graphs)

- **Definition**: Collections of tasks with defined dependencies and relationships
- **Structure**: Must be acyclic (no loops) to prevent infinite execution
- **File Location**: Stored in the `dags/` folder
- **Discovery**: Airflow automatically discovers DAG files

python

```python
from airflow import DAG
from datetime import datetime

dag = DAG(
    'my_workflow',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
)
```

### Tasks and Operators

**[[Operators]]** define what actually gets executed in a workflow:

- **[[BashOperator]]**: Execute bash commands
- **[[PythonOperator]]**: Execute Python functions
- **[[SQLOperator]]**: Execute SQL queries
- **[[EmailOperator]]**: Send email notifications
- **[[S3Operator]]**: Interact with AWS S3
- **[[KubernetesOperator]]**: Run containers in Kubernetes

### Task Dependencies

Multiple ways to define task relationships:

python

```python
# Method 1: >> and << operators
task1 >> task2 >> task3

# Method 2: set_downstream/set_upstream
task1.set_downstream(task2)

# Method 3: Using lists
task1 >> [task2, task3] >> task4
```

## Architecture Components

### Core Components

- **[[Airflow Scheduler]]**: Orchestrates task execution
- **[[Airflow Webserver]]**: Provides web-based UI
- **[[Airflow Worker]]**: Executes tasks (in distributed setup)
- **[[Metadata Database]]**: Stores DAG and task state
- **[[Executor]]**: Defines how tasks are executed

### Executors

|Executor Type|Use Case|Scalability|
|---|---|---|
|**[[SequentialExecutor]]**|Development/Testing|Single-threaded|
|**[[LocalExecutor]]**|Single machine|Multi-threaded|
|**[[CeleryExecutor]]**|Distributed|High scalability|
|**[[KubernetesExecutor]]**|Cloud-native|Auto-scaling|

## Installation and Setup

### Local Development Setup

bash

```bash
# Install Airflow
pip install apache-airflow

# Initialize database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Start webserver and scheduler
airflow webserver --port 8080
airflow scheduler
```

### [[Docker Compose]] Setup

- **Benefits**: Consistent environment, easy to share
- **Components**: Webserver, scheduler, worker, database
- **Persistence**: Volumes for DAGs and logs
- **Related**: [[Container Orchestration]], [[Development Environment]]

## DAG Development Best Practices

### Code Structure

python

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Default arguments
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# DAG definition
dag = DAG(
    'data_pipeline',
    default_args=default_args,
    description='Daily data processing pipeline',
    schedule_interval='@daily',
    catchup=False,
    tags=['data', 'etl', 'daily']
)
```

### Task Design Principles

- **[[Idempotency]]**: Tasks should produce same results when re-run
- **[[Atomicity]]**: Each task should do one thing well
- **[[Error Handling]]**: Implement proper exception handling
- **[[Logging]]**: Use Airflow's logging for debugging

> [!tip] Performance Optimization
> 
> - Use [[XComs]] sparingly for small data only
> - Implement [[Task Groups]] for logical organization
> - Consider [[Dynamic DAGs]] for similar workflows
> - Use [[Sensors]] for external dependencies

## Common Operators

### Data Processing

- **[[PythonOperator]]**: Custom Python functions
- **[[BashOperator]]**: Shell commands and scripts
- **[[DockerOperator]]**: Containerized tasks
- **[[SparkSubmitOperator]]**: Apache Spark jobs

### Database Operations

- **[[PostgresOperator]]**: PostgreSQL queries
- **[[MySqlOperator]]**: MySQL operations
- **[[SqliteOperator]]**: SQLite database tasks
- **[[BigQueryOperator]]**: Google BigQuery operations

### Cloud Services

- **[[S3FileTransformOperator]]**: AWS S3 operations
- **[[GCSOperator]]**: Google Cloud Storage
- **[[AzureBlobStorageOperator]]**: Azure storage operations

## Scheduling and Execution

### Schedule Intervals

|Expression|Description|Use Case|
|---|---|---|
|`@once`|Run once|One-time jobs|
|`@daily`|Every day at midnight|Daily reports|
|`@hourly`|Every hour|Real-time processing|
|`0 0 * * 1`|Every Monday|Weekly aggregations|
|`None`|Manual trigger only|Ad-hoc workflows|

### [[Task States]]

- **Success**: ✅ Task completed successfully
- **Failed**: ❌ Task failed with error
- **Running**: 🔄 Currently executing
- **Upstream Failed**: ⬆️ Dependency failed
- **Skipped**: ⏭️ Intentionally skipped
- **Retry**: 🔄 Will retry on failure

## Monitoring and Observability

### Web Interface Features

- **[[DAG View]]**: Visual representation of workflows
- **[[Tree View]]**: Historical task execution
- **[[Gantt Chart]]**: Task duration analysis
- **[[Graph View]]**: Task dependencies
- **[[Log Viewer]]**: Task execution logs

### [[Alerting and Notifications]]

python

```python
# Email alerts on failure
default_args = {
    'email_on_failure': True,
    'email': ['admin@company.com'],
    'email_on_retry': False
}

# Slack notifications
from airflow.providers.slack.operators.slack import SlackAPIPostOperator

slack_alert = SlackAPIPostOperator(
    task_id='slack_notification',
    token='your-slack-token',
    text='DAG {{ dag.dag_id }} failed!',
    channel='#alerts'
)
```

### [[Metrics and Logging]]

- **Task Duration**: Monitor performance trends
- **Success Rates**: Track reliability
- **Resource Usage**: Memory and CPU utilization
- **Custom Metrics**: Business-specific KPIs

## Advanced Features

### [[XComs]] (Cross-Communication)

python

```python
# Push data
def push_data(**context):
    return "Hello from upstream task"

# Pull data  
def pull_data(**context):
    message = context['task_instance'].xcom_pull(task_ids='push_task')
    print(message)
```

### [[Task Groups]]

python

```python
from airflow.utils.task_group import TaskGroup

with TaskGroup("data_processing") as processing_group:
    extract_task = PythonOperator(...)
    transform_task = PythonOperator(...)
    load_task = PythonOperator(...)
    
    extract_task >> transform_task >> load_task
```

### [[Sensors]]

python

```python
from airflow.sensors.filesystem import FileSensor

# Wait for file to arrive
file_sensor = FileSensor(
    task_id='wait_for_file',
    filepath='/data/input/file.csv',
    poke_interval=60,
    timeout=300
)
```

### [[Hooks]] and [[Connections]]

- **Purpose**: Abstract connection details
- **Configuration**: Store in Airflow UI or environment variables
- **Security**: Encrypted password storage
- **Reusability**: Share across multiple DAGs

## Production Deployment

### [[High Availability Setup]]

- **Load Balancer**: Multiple webserver instances
- **Database**: PostgreSQL with replication
- **Message Broker**: Redis or RabbitMQ for Celery
- **Storage**: Shared filesystem for logs and DAGs

### [[Security Best Practices]]

- **Authentication**: LDAP, OAuth, or database auth
- **Authorization**: Role-based access control ([[RBAC]])
- **Encryption**: TLS for web traffic, encrypted connections
- **Secrets Management**: External secret backends
- **Network Security**: VPC, security groups, firewalls

### [[Scaling Strategies]]

- **Horizontal Scaling**: Multiple worker nodes
- **Vertical Scaling**: Increase resource allocation
- **Auto-scaling**: Kubernetes-based dynamic scaling
- **Resource Pools**: Limit concurrent task execution

## Integration Patterns

### [[ETL Pipelines]]

python

```python
# Typical ETL pattern
extract_task >> transform_task >> load_task >> validate_task
```

### [[Machine Learning Workflows]]

- **[[Data Preparation]]**: Feature engineering tasks
- **[[Model Training]]**: ML model training jobs
- **[[Model Deployment]]**: Deploy to production
- **[[Model Monitoring]]**: Performance tracking

### [[CI/CD Integration]]

- **[[Git Integration]]**: Version control for DAGs
- **[[Testing]]**: Unit tests for DAG logic
- **[[Deployment Automation]]**: Automated DAG deployment
- **[[Environment Promotion]]**: Dev → Test → Prod

## Troubleshooting Common Issues

### Performance Problems

- **[[Zombie Tasks]]**: Tasks that appear running but aren't
- **[[Dead Workers]]**: Worker nodes that stopped responding
- **[[Database Locks]]**: Concurrent access issues
- **[[Memory Leaks]]**: Long-running tasks consuming memory

### Configuration Issues

- **[[Connection Timeouts]]**: Database or external service timeouts
- **[[Resource Constraints]]**: CPU or memory limitations
- **[[Permission Errors]]**: File system or database permissions
- **[[Import Errors]]**: Missing dependencies or Python path issues

## Related Technologies

### Workflow Orchestrators

- **[[Apache Oozie]]**: Hadoop ecosystem workflows
- **[[Luigi]]**: Python-based pipeline framework
- **[[Prefect]]**: Modern Python workflow engine
- **[[Dagster]]**: Data-aware orchestration platform
- **[[Kubeflow]]**: ML workflows on Kubernetes

### Complementary Tools

- **[[Apache Spark]]**: Large-scale data processing
- **[[Kafka]]**: Stream processing integration
- **[[dbt]]**: Data transformation tool
- **[[Great Expectations]]**: Data quality testing
- **[[MLflow]]**: ML lifecycle management

## Best Practices Summary

### Development

- [ ]  Use [[Version Control]] for all DAG files
- [ ]  Implement proper [[Error Handling]] and retries
- [ ]  Write [[Unit Tests]] for custom operators
- [ ]  Use [[Configuration Management]] for environments
- [ ]  Document DAG purpose and dependencies

### Operations

- [ ]  Monitor [[System Resources]] and performance
- [ ]  Set up [[Alerting]] for failures and SLA breaches
- [ ]  Implement [[Log Aggregation]] for debugging
- [ ]  Regular [[Database Maintenance]] and backups
- [ ]  Plan for [[Disaster Recovery]] scenarios

### Security

- [ ]  Use [[Secret Management]] for sensitive data
- [ ]  Implement [[Network Segmentation]]
- [ ]  Enable [[Audit Logging]] for compliance
- [ ]  Regular [[Security Updates]] and patches
- [ ]  [[Access Control]] with least privilege principle

## Learning Resources

### Official Documentation

- **[[Airflow Documentation]]**: Comprehensive official docs
- **[[Airflow GitHub]]**: Source code and issues
- **[[Airflow Community]]**: Forums and discussion

### Training and Courses

- **[[Apache Airflow Fundamentals]]**: Astronomer course
- **[[Data Engineering with Airflow]]**: Advanced patterns
- **[[Airflow for Data Science]]**: ML workflow patterns

### Books and Articles

- **[[Data Pipelines with Apache Airflow]]**: Comprehensive guide
- **[[Airflow Best Practices]]**: Production deployment patterns
- **[[Workflow Orchestration Patterns]]**: Design principles

---

_Tags: #airflow #workflow-orchestration #data-engineering #python #etl #scheduling #dag #apache_

_Related: [[Data Engineering]], [[ETL Pipelines]], [[Python]], [[Docker]], [[Kubernetes]], [[Data Workflows]], [[Task Scheduling]]_



# Apache Airflow - Complete Beginner's Guide

_Learn workflow orchestration from scratch with practical examples and clear explanations_

## What is Apache Airflow?

**Apache Airflow** is like a smart scheduler for your computer tasks - imagine having a personal assistant that can run your data processing jobs, send emails, backup files, and coordinate complex workflows automatically.

> [!note] Real-World Analogy Think of Airflow like a factory assembly line manager. It knows which tasks need to run, in what order, when they should start, and what to do if something goes wrong.

### Why Do We Need Airflow?

Before Airflow, data teams had problems like:

- **Cron jobs everywhere**: Hard to manage and monitor
- **No visibility**: When tasks failed, nobody knew why
- **Complex dependencies**: If Task A fails, Tasks B and C shouldn't run
- **No retry logic**: Manual intervention needed for failures

**Airflow solves these problems** by providing a visual interface, automatic retries, dependency management, and much more.

## Core Concepts Explained Simply

### 1. DAG (Directed Acyclic Graph)

A **DAG** is your workflow - a collection of tasks that run in a specific order.

> [!important] DAG Rules
> 
> - **Directed**: Tasks flow in one direction (A → B → C)
> - **Acyclic**: No loops allowed (prevents infinite execution)
> - **Graph**: Visual representation of task relationships

**Example DAG in plain English:**

1. Download sales data from database
2. Clean and validate the data
3. Generate monthly report
4. Email report to managers

python

```python
# Simple DAG structure
from airflow import DAG
from datetime import datetime

# This creates your workflow
my_first_dag = DAG(
    'daily_sales_report',           # Name of your workflow
    start_date=datetime(2024, 1, 1), # When it should start
    schedule_interval='@daily'        # How often it runs
)
```

### 2. Tasks and Operators

**Tasks** are individual jobs in your workflow. **Operators** define what type of work each task does.

#### Common Operators for Beginners

|Operator|What It Does|Example Use|
|---|---|---|
|`PythonOperator`|Runs Python code|Data analysis, calculations|
|`BashOperator`|Runs shell commands|File operations, system tasks|
|`EmailOperator`|Sends emails|Notifications, reports|
|`SqlOperator`|Runs database queries|Data extraction, updates|

python

```python
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Python task
def say_hello():
    print("Hello from Airflow!")

python_task = PythonOperator(
    task_id='greet_user',
    python_callable=say_hello,
    dag=my_first_dag
)

# Bash task
bash_task = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=my_first_dag
)
```

### 3. Task Dependencies

Dependencies tell Airflow the order in which tasks should run.

python

```python
# Simple dependency: task1 runs before task2
task1 >> task2

# Multiple dependencies
task1 >> [task2, task3] >> task4
```

**Visual representation:**

```
task1 → task2 → task4
    ↘   task3   ↗
```

## Your First Airflow Project

Let's build a simple daily weather report workflow step by step.

### Step 1: Installation

bash

```bash
# Install Airflow (simple method)
pip install apache-airflow

# Initialize the database
airflow db init

# Create an admin user
airflow users create \
    --username admin \
    --password admin \
    --firstname Your \
    --lastname Name \
    --role Admin \
    --email admin@example.com
```

### Step 2: Create Your First DAG

Create a file called `weather_report_dag.py` in your `dags/` folder:

python

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
import requests

# Default settings for all tasks
default_args = {
    'owner': 'beginner',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'weather_report',
    default_args=default_args,
    description='Daily weather report workflow',
    schedule_interval='@daily',  # Run every day
    catchup=False  # Don't run for past dates
)

# Task 1: Get weather data
def fetch_weather_data():
    """Fetch weather data from API"""
    # Simple weather API call (you'd use a real API key)
    weather_info = "Today: Sunny, 75°F, Light breeze"
    print(f"Weather data retrieved: {weather_info}")
    return weather_info

weather_task = PythonOperator(
    task_id='get_weather',
    python_callable=fetch_weather_data,
    dag=dag
)

# Task 2: Process the data
def process_weather_data(**context):
    """Process and format weather data"""
    # Get data from previous task
    weather_data = context['task_instance'].xcom_pull(task_ids='get_weather')
    processed_data = f"🌤️ Daily Weather Report: {weather_data}"
    print(f"Processed: {processed_data}")
    return processed_data

process_task = PythonOperator(
    task_id='process_weather',
    python_callable=process_weather_data,
    dag=dag
)

# Task 3: Send email (optional - configure email settings first)
def send_weather_update(**context):
    """Send weather update"""
    weather_report = context['task_instance'].xcom_pull(task_ids='process_weather')
    print(f"Sending email with: {weather_report}")
    # In real scenario, you'd send actual email

email_task = PythonOperator(
    task_id='send_email',
    python_callable=send_weather_update,
    dag=dag
)

# Define task order
weather_task >> process_task >> email_task
```

### Step 3: Run Your DAG

bash

```bash
# Start the web server (in one terminal)
airflow webserver --port 8080

# Start the scheduler (in another terminal)
airflow scheduler
```

Visit `http://localhost:8080` and you'll see the Airflow web interface!

## Understanding the Web Interface

### Main Views Explained

#### 1. **DAGs View** (Home Page)

- **Green**: DAG is active and healthy
- **Red**: DAG has failures
- **Grey**: DAG is paused
- **Toggle Switch**: Pause/unpause DAGs

#### 2. **Tree View**

Shows your DAG's execution history in a tree format:

- **Green squares**: Successful task runs
- **Red squares**: Failed task runs
- **Yellow squares**: Running tasks

#### 3. **Graph View**

Visual representation of your DAG structure:

- **Boxes**: Individual tasks
- **Arrows**: Dependencies between tasks
- **Colors**: Task states (green=success, red=failure)

#### 4. **Log View**

Click on any task to see its execution logs - crucial for debugging!

## Common Beginner Patterns

### Pattern 1: ETL Pipeline

**Extract → Transform → Load** is the most common data workflow:

python

```python
# Extract data from source
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_from_database
)

# Transform/clean the data  
transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=clean_and_process
)

# Load to destination
load_task = PythonOperator(
    task_id='load_data',
    python_callable=save_to_warehouse
)

# Set up the pipeline
extract_task >> transform_task >> load_task
```

### Pattern 2: Parallel Processing

Some tasks can run at the same time:

python

```python
# These can run simultaneously
task_a = PythonOperator(task_id='process_region_a', ...)
task_b = PythonOperator(task_id='process_region_b', ...)
task_c = PythonOperator(task_id='process_region_c', ...)

# Final task waits for all to complete
final_task = PythonOperator(task_id='combine_results', ...)

# Parallel execution
[task_a, task_b, task_c] >> final_task
```

### Pattern 3: Conditional Logic

Run different tasks based on conditions:

python

```python
from airflow.operators.python import BranchPythonOperator

def choose_path(**context):
    # Your logic here
    if some_condition:
        return 'task_for_weekday'
    else:
        return 'task_for_weekend'

branch_task = BranchPythonOperator(
    task_id='choose_branch',
    python_callable=choose_path
)

weekday_task = PythonOperator(task_id='task_for_weekday', ...)
weekend_task = PythonOperator(task_id='task_for_weekend', ...)

branch_task >> [weekday_task, weekend_task]
```

## Scheduling Made Simple

### Schedule Intervals

|Schedule|When It Runs|Use Case|
|---|---|---|
|`'@once'`|One time only|One-off jobs|
|`'@daily'`|Every day at midnight|Daily reports|
|`'@weekly'`|Every Sunday at midnight|Weekly summaries|
|`'@monthly'`|First day of month|Monthly billing|
|`'@hourly'`|Every hour|Real-time processing|
|`'0 9 * * 1-5'`|9 AM on weekdays|Business day jobs|

> [!tip] Cron Expression Helper Use [crontab.guru](https://crontab.guru/) to build custom cron expressions!

### Understanding Start Date

python

```python
# This DAG will run daily starting from Jan 1, 2024
dag = DAG(
    'my_dag',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily'
)
```

**Important**: If today is March 1st and you set start_date to January 1st, Airflow will try to "catch up" and run all missed dates unless you set `catchup=False`.

## Error Handling and Monitoring

### Task States Explained

|State|Color|Meaning|What to Do|
|---|---|---|---|
|**Success**|🟢 Green|Task completed successfully|Nothing - celebrate!|
|**Failed**|🔴 Red|Task encountered an error|Check logs, fix issue|
|**Running**|🟡 Yellow|Task is currently executing|Wait and monitor|
|**Retry**|🟠 Orange|Task failed but will retry|Monitor next attempt|
|**Skipped**|💙 Blue|Task was intentionally skipped|Expected behavior|

### Setting Up Retries

python

```python
default_args = {
    'retries': 3,                    # Try 3 times if task fails
    'retry_delay': timedelta(minutes=5), # Wait 5 minutes between retries
    'email_on_failure': True,       # Send email when task fails
    'email': ['your@email.com']     # Where to send alerts
}
```

### Common Error Debugging Steps

1. **Check Task Logs**: Click on failed task → View Logs
2. **Look for Error Messages**: Python tracebacks, connection errors
3. **Check Dependencies**: Are upstream tasks successful?
4. **Verify Configuration**: Database connections, file paths
5. **Test Locally**: Run the Python function outside Airflow

## Best Practices for Beginners

### 1. Start Simple

python

```python
# ✅ Good: Simple, clear task
def process_daily_sales():
    # Load data
    # Process data  
    # Save results
    pass

# ❌ Avoid: Complex, multi-purpose task
def do_everything():
    # 50 lines of mixed operations
    pass
```

### 2. Use Descriptive Names

python

```python
# ✅ Good: Clear purpose
extract_customer_data = PythonOperator(
    task_id='extract_customer_data_from_crm',
    ...
)

# ❌ Avoid: Unclear purpose
task1 = PythonOperator(
    task_id='task1',
    ...
)
```

### 3. Add Documentation

python

```python
dag = DAG(
    'customer_analysis_pipeline',
    description='Daily customer behavior analysis and reporting',
    doc_md="""
    ## Customer Analysis Pipeline
    
    This DAG processes customer data daily and generates insights:
    1. Extract customer transactions from database
    2. Calculate behavior metrics
    3. Generate executive dashboard
    4. Send alerts for unusual patterns
    """,
    tags=['customer', 'analytics', 'daily']
)
```

## Practical Examples for Learning

### Example 1: File Processing Pipeline

python

```python
def check_for_new_files():
    """Check if new files are available for processing"""
    # Your file checking logic
    return True

def process_file():
    """Process the file"""
    print("Processing file...")
    # Your processing logic

def archive_file():
    """Archive processed file"""
    print("Archiving file...")
    # Your archiving logic

# Create tasks
check_task = PythonOperator(task_id='check_files', python_callable=check_for_new_files)
process_task = PythonOperator(task_id='process_file', python_callable=process_file)
archive_task = PythonOperator(task_id='archive_file', python_callable=archive_file)

# Link them together
check_task >> process_task >> archive_task
```

### Example 2: Database Backup Workflow

python

```python
from airflow.operators.bash import BashOperator

# Backup database
backup_db = BashOperator(
    task_id='backup_database',
    bash_command='pg_dump mydb > /backups/backup_{{ ds }}.sql'
)

# Verify backup
verify_backup = BashOperator(
    task_id='verify_backup',
    bash_command='ls -la /backups/backup_{{ ds }}.sql'
)

# Upload to cloud storage (simulated)
upload_backup = BashOperator(
    task_id='upload_to_cloud',
    bash_command='echo "Uploading backup_{{ ds }}.sql to cloud storage"'
)

backup_db >> verify_backup >> upload_backup
```

## Troubleshooting Common Issues

### Issue 1: "DAG Not Showing Up"

**Problem**: Your DAG file exists but doesn't appear in the web interface.

**Solutions**:

- Check file is in correct `dags/` folder
- Ensure no Python syntax errors (`python your_dag.py`)
- Verify DAG name is unique
- Check Airflow logs for import errors

### Issue 2: "Task Stuck in Running State"

**Problem**: Task shows as running but never completes.

**Solutions**:

- Check system resources (CPU, memory)
- Look for infinite loops in your code
- Verify external services are responding
- Check if task is waiting for user input

### Issue 3: "Connection Errors"

**Problem**: Can't connect to databases or external services.

**Solutions**:

- Verify connection settings in Airflow UI (Admin → Connections)
- Test connectivity from command line
- Check firewall and network settings
- Verify credentials and permissions

## Next Steps: Growing Your Skills

### Phase 1: Master the Basics

- [ ]  Create 3-5 simple DAGs with different operators
- [ ]  Practice setting up dependencies and scheduling
- [ ]  Learn to read logs and debug failures
- [ ]  Understand task states and error handling

### Phase 2: Intermediate Features

- [ ]  Learn about [[XComs]] for task communication
- [ ]  Explore [[Sensors]] for external dependencies
- [ ]  Practice with [[BranchPythonOperator]] for conditional logic
- [ ]  Set up email notifications and alerts

### Phase 3: Advanced Topics

- [ ]  Study [[Airflow Hooks]] and [[Connections]]
- [ ]  Learn about [[Task Groups]] for organization
- [ ]  Explore [[Dynamic DAGs]] for programmatic creation
- [ ]  Practice [[Testing]] your DAGs

### Phase 4: Production Deployment

- [ ]  Learn [[Docker]] deployment methods
- [ ]  Study [[Security]] best practices
- [ ]  Understand [[Scaling]] and [[High Availability]]
- [ ]  Master [[Monitoring]] and [[Observability]]

## Learning Resources

### Essential Documentation

- **[[Official Airflow Docs]]**: Start with the tutorial
- **[[Airflow Examples]]**: Sample DAGs in the official repo
- **[[Community Forum]]**: Get help from other users

### Recommended Courses

- **[[Apache Airflow: The Complete Hands-On Course]]**: Udemy
- **[[Airflow Fundamentals]]**: Astronomer Academy (free)
- **[[Data Engineering with Python]]**: Includes Airflow modules

### Practice Projects

- **Daily Weather Report**: API calls and email notifications
- **File Processing Pipeline**: Monitor folders, process files
- **Database ETL**: Extract, transform, load data between systems
- **Web Scraping Workflow**: Scheduled data collection
- **Report Generation**: Automated business reports

## Common Vocabulary

|Term|Simple Explanation|
|---|---|
|**DAG**|Your workflow (collection of tasks)|
|**Task**|Individual job in your workflow|
|**Operator**|Defines what type of work a task does|
|**Scheduler**|Airflow component that runs your tasks|
|**Webserver**|Provides the web interface you see|
|**Executor**|Determines how tasks are executed|
|**XCom**|Way for tasks to share small amounts of data|
|**Sensor**|Special task that waits for external events|
|**Hook**|Connects to external systems (databases, APIs)|

---

> [!success] You're Ready to Start! With this foundation, you can begin creating your own workflows in Airflow. Start with simple DAGs and gradually add complexity as you learn.

_Tags: #airflow #beginner #workflow #orchestration #python #data-engineering #tutorial_

_Related: [[Python Programming]], [[Data Engineering]], [[ETL Processes]], [[Task Scheduling]], [[Database Operations]], [[API Integration]]_