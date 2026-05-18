# Python Log Handlers


_Master Python logging with different handlers for flexible and robust logging solutions_

## What are Log Handlers?

**Log Handlers** are components in Python's logging framework that determine where and how log messages are output. They act as the "destination" for your log records, sending them to different targets like files, console, email, or network endpoints.

> [!note] Think of Handlers as... Log handlers are like mail carriers - they take your log messages (letters) and deliver them to specific destinations (console, files, email, etc.). Each handler knows how to format and deliver messages to its assigned destination.

### Key Concepts

- **Handler**: Processes and routes log records to specific destinations
- **Formatter**: Defines the layout and content of log messages
- **Filter**: Controls which log records are processed by a handler
- **Level**: Determines minimum severity level for processing

## Why Log Handlers are Important

### Flexibility in Output Destinations

- Send logs to multiple destinations simultaneously
- Different log levels to different outputs
- Separate error logs from info logs
- Archive logs while maintaining live monitoring

### Production Requirements

- **File Logging**: Persistent storage for analysis and debugging
- **Console Logging**: Real-time monitoring during development
- **Log Rotation**: Prevent disk space issues with large log files
- **Remote Logging**: Centralized logging in distributed systems

### Debugging and Monitoring

- **Development**: Console output for immediate feedback
- **Testing**: File logs for test result analysis
- **Production**: Multiple handlers for different stakeholders
- **Incident Response**: Separate error logs for quick troubleshooting

## Types of Log Handlers

### Handler Hierarchy

```python
import logging

# All handlers inherit from logging.Handler
# Common handler types:
# - StreamHandler (console output)
# - FileHandler (single file)
# - RotatingFileHandler (size-based rotation)
# - TimedRotatingFileHandler (time-based rotation)
# - SMTPHandler (email notifications)
# - SysLogHandler (system logging)
# - SocketHandler (network logging)
```

## StreamHandler - Console Output

**StreamHandler** sends log messages to streams like `stdout` (console) or `stderr`. Default choice for console logging.

### Basic StreamHandler

```python
import logging

# Create logger
logger = logging.getLogger('console_app')
logger.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)

# Test logging
logger.debug('This will not appear (below INFO level)')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
```

### StreamHandler to Different Streams

```python
import logging
import sys

# Console handler for INFO and above
info_handler = logging.StreamHandler(sys.stdout)
info_handler.setLevel(logging.INFO)
info_handler.addFilter(lambda record: record.levelno < logging.ERROR)

# Error handler for ERROR and above
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.ERROR)

# Setup logger
logger = logging.getLogger('stream_app')
logger.setLevel(logging.DEBUG)
logger.addHandler(info_handler)
logger.addHandler(error_handler)

# Test different levels
logger.info('Info goes to stdout')
logger.error('Error goes to stderr')
```

### When to Use StreamHandler

- **Development**: Real-time feedback during coding
- **Interactive Applications**: User-facing status messages
- **Containerized Applications**: Docker logs capture stdout/stderr
- **Quick Debugging**: Immediate visibility of log messages

## FileHandler - Single File Logging

**FileHandler** writes log messages to a single file. Simple and reliable for basic file logging needs.

### Basic FileHandler

```python
import logging

# Create logger
logger = logging.getLogger('file_app')
logger.setLevel(logging.DEBUG)

# Create file handler
file_handler = logging.FileHandler('application.log')
file_handler.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(file_handler)

# Test logging
logger.debug('Debug message saved to file')
logger.info('Application started')
logger.error('An error occurred')
```

### FileHandler with Different Files by Level

```python
import logging

# Setup logger
logger = logging.getLogger('multi_file_app')
logger.setLevel(logging.DEBUG)

# General log file (all levels)
general_handler = logging.FileHandler('app_general.log')
general_handler.setLevel(logging.DEBUG)

# Error log file (errors only)
error_handler = logging.FileHandler('app_errors.log')
error_handler.setLevel(logging.ERROR)

# Formatters
general_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')

general_handler.setFormatter(general_formatter)
error_handler.setFormatter(error_formatter)

# Add handlers
logger.addHandler(general_handler)
logger.addHandler(error_handler)

# Test logging
logger.info('This goes to general log only')
logger.error('This goes to both general and error logs')
```

### FileHandler Mode Options

```python
import logging

# Append mode (default) - adds to existing file
append_handler = logging.FileHandler('append.log', mode='a')

# Write mode - overwrites existing file
overwrite_handler = logging.FileHandler('overwrite.log', mode='w')

# Write mode with encoding
utf8_handler = logging.FileHandler('utf8.log', mode='a', encoding='utf-8')

# Example usage
logger = logging.getLogger('file_modes')
logger.addHandler(utf8_handler)

logger.info('Message with unicode: ñáéíóú')
```

## RotatingFileHandler - Size-Based Rotation

**RotatingFileHandler** automatically rotates log files when they reach a specified size. Essential for production applications to prevent unbounded log file growth.

### Basic RotatingFileHandler

```python
import logging
from logging.handlers import RotatingFileHandler

# Create logger
logger = logging.getLogger('rotating_app')
logger.setLevel(logging.DEBUG)

# Create rotating file handler
# maxBytes: 5MB per file, backupCount: keep 3 backup files
rotating_handler = RotatingFileHandler(
    'rotating_app.log',
    maxBytes=5*1024*1024,  # 5 MB
    backupCount=3
)
rotating_handler.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(formatter)

# Add handler
logger.addHandler(rotating_handler)

# Test with many messages to trigger rotation
for i in range(10000):
    logger.info(f'Log message number {i} - This is a test message to fill up the log file')
```

### Advanced RotatingFileHandler Configuration

```python
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_rotating_logger(name, log_file, level=logging.INFO):
    """Setup a logger with rotating file handler"""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create rotating handler
    handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5,          # Keep 5 backup files
        encoding='utf-8'
    )
    handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger

# Usage
app_logger = setup_rotating_logger('myapp', 'logs/myapp.log')
error_logger = setup_rotating_logger('myapp.errors', 'logs/errors.log', logging.ERROR)

app_logger.info('Application started')
error_logger.error('Critical error occurred')
```

### Understanding Rotation Behavior

```python
import logging
from logging.handlers import RotatingFileHandler

# When rotation occurs:
# current_file.log (current)
# current_file.log.1 (most recent backup)
# current_file.log.2 (older backup)
# current_file.log.3 (oldest backup - gets deleted when new rotation occurs)

rotating_handler = RotatingFileHandler(
    'demo.log',
    maxBytes=1024,    # Very small for demo (1KB)
    backupCount=2     # Keep only 2 backups
)

logger = logging.getLogger('rotation_demo')
logger.addHandler(rotating_handler)
logger.setLevel(logging.INFO)

# Generate enough logs to see rotation
for i in range(100):
    logger.info(f'This is log message {i:03d} - Adding content to trigger rotation')
    
# Check filesystem to see:
# demo.log (current)
# demo.log.1 (first backup)
# demo.log.2 (second backup)
```

## TimedRotatingFileHandler - Time-Based Rotation

**TimedRotatingFileHandler** rotates log files based on time intervals (hourly, daily, weekly, etc.). Perfect for applications that need time-based log archival.

### Basic TimedRotatingFileHandler

```python
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# Create logger
logger = logging.getLogger('timed_app')
logger.setLevel(logging.DEBUG)

# Create timed rotating handler
# 'midnight' rotation - new file each day at midnight
timed_handler = TimedRotatingFileHandler(
    'timed_app.log',
    when='midnight',
    interval=1,
    backupCount=7  # Keep 7 days of logs
)
timed_handler.setLevel(logging.DEBUG)

# Formatter with date
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
timed_handler.setFormatter(formatter)

# Add handler
logger.addHandler(timed_handler)

# Test logging
logger.info(f'Application started at {datetime.now()}')
```

### Different Time Intervals

```python
import logging
from logging.handlers import TimedRotatingFileHandler

# Available 'when' options:
rotation_configs = {
    'hourly': {
        'when': 'H',        # Every hour
        'interval': 1,      # Every 1 hour
        'backupCount': 24   # Keep 24 hours
    },
    'daily': {
        'when': 'D',        # Every day
        'interval': 1,      # Every 1 day
        'backupCount': 30   # Keep 30 days
    },
    'weekly': {
        'when': 'W0',       # Every Monday (W0=Monday, W1=Tuesday, etc.)
        'interval': 1,      # Every 1 week
        'backupCount': 12   # Keep 12 weeks
    },
    'monthly': {
        'when': 'midnight', # At midnight
        'interval': 30,     # Every 30 days
        'backupCount': 12   # Keep 12 months
    }
}

def create_timed_logger(name, filename, config_key='daily'):
    """Create logger with timed rotation"""
    config = rotation_configs[config_key]
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    handler = TimedRotatingFileHandler(
        filename,
        when=config['when'],
        interval=config['interval'],
        backupCount=config['backupCount'],
        encoding='utf-8'
    )
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Create different loggers
hourly_logger = create_timed_logger('hourly_app', 'logs/hourly.log', 'hourly')
daily_logger = create_timed_logger('daily_app', 'logs/daily.log', 'daily')
weekly_logger = create_timed_logger('weekly_app', 'logs/weekly.log', 'weekly')
```

### Custom Suffix for Rotated Files

```python
import logging
from logging.handlers import TimedRotatingFileHandler

# Create handler with custom suffix
handler = TimedRotatingFileHandler(
    'custom_app.log',
    when='midnight',
    interval=1,
    backupCount=7
)

# Customize the suffix (default is %Y-%m-%d for daily rotation)
handler.suffix = '%Y-%m-%d_%H-%M-%S'

# This will create files like:
# custom_app.log (current)
# custom_app.log.2024-01-15_00-00-00 (rotated)
# custom_app.log.2024-01-14_00-00-00 (older)

logger = logging.getLogger('custom_suffix')
logger.addHandler(handler)
logger.info('Testing custom suffix rotation')
```

## Multiple Handlers - Combining Different Outputs

One of the most powerful features is using multiple handlers simultaneously to send logs to different destinations.

### Console + File Logging

```python
import logging

def setup_dual_logging(name, log_file, console_level=logging.INFO, file_level=logging.DEBUG):
    """Setup logger with both console and file output"""
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(file_level)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Usage
app_logger = setup_dual_logging('myapp', 'myapp.log')

app_logger.debug('Detailed debug info (file only)')
app_logger.info('General info (console + file)')
app_logger.warning('Warning message (console + file)')
app_logger.error('Error message (console + file)')
```

### Production Logging Setup

```python
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import sys
import os

def setup_production_logging(app_name, log_dir='logs'):
    """Production-ready logging setup with multiple handlers"""
    
    # Create log directory
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Main application logger
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # 1. Console handler (WARNING and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # 2. General application log (rotating by size)
    app_handler = RotatingFileHandler(
        f'{log_dir}/{app_name}.log',
        maxBytes=50*1024*1024,  # 50MB
        backupCount=5
    )
    app_handler.setLevel(logging.INFO)
    app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
    app_handler.setFormatter(app_formatter)
    
    # 3. Error log (daily rotation)
    error_handler = TimedRotatingFileHandler(
        f'{log_dir}/{app_name}_errors.log',
        when='midnight',
        interval=1,
        backupCount=30
    )
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s\n%(exc_info)s')
    error_handler.setFormatter(error_formatter)
    
    # 4. Debug log (hourly rotation, short retention)
    debug_handler = TimedRotatingFileHandler(
        f'{log_dir}/{app_name}_debug.log',
        when='H',
        interval=1,
        backupCount=24
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
    debug_handler.setFormatter(debug_formatter)
    
    # Add all handlers
    logger.addHandler(console_handler)
    logger.addHandler(app_handler)
    logger.addHandler(error_handler)
    logger.addHandler(debug_handler)
    
    return logger

# Usage
app_logger = setup_production_logging('production_app')

app_logger.debug('Detailed debug information')
app_logger.info('Application operation info')
app_logger.warning('Warning - visible on console too')
app_logger.error('Error - logged to multiple places')
```

### Level-Based Handler Filtering

```python
import logging

class LevelFilter(logging.Filter):
    """Filter to only allow specific log levels"""
    
    def __init__(self, min_level=None, max_level=None):
        super().__init__()
        self.min_level = min_level
        self.max_level = max_level
    
    def filter(self, record):
        if self.min_level and record.levelno < self.min_level:
            return False
        if self.max_level and record.levelno > self.max_level:
            return False
        return True

# Setup logger with filtered handlers
logger = logging.getLogger('filtered_app')
logger.setLevel(logging.DEBUG)

# Info handler (INFO and WARNING only)
info_handler = logging.FileHandler('info.log')
info_handler.addFilter(LevelFilter(logging.INFO, logging.WARNING))

# Error handler (ERROR and CRITICAL only)
error_handler = logging.FileHandler('errors.log')
error_handler.addFilter(LevelFilter(logging.ERROR))

# Debug handler (DEBUG only)
debug_handler = logging.FileHandler('debug.log')
debug_handler.addFilter(LevelFilter(logging.DEBUG, logging.DEBUG))

logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(debug_handler)

# Test filtering
logger.debug('Debug message -> debug.log only')
logger.info('Info message -> info.log only')
logger.warning('Warning message -> info.log only')
logger.error('Error message -> errors.log only')
```

## Advanced Handler Types

### SMTPHandler - Email Notifications

```python
import logging
from logging.handlers import SMTPHandler

# SMTP Handler for critical errors
def setup_email_alerts(logger_name, smtp_config):
    """Setup email notifications for critical errors"""
    
    logger = logging.getLogger(logger_name)
    
    smtp_handler = SMTPHandler(
        mailhost=(smtp_config['host'], smtp_config['port']),
        fromaddr=smtp_config['from_addr'],
        toaddrs=smtp_config['to_addrs'],
        subject=f'Critical Error in {logger_name}',
        credentials=(smtp_config['username'], smtp_config['password']),
        secure=()  # Use TLS
    )
    smtp_handler.setLevel(logging.CRITICAL)
    
    formatter = logging.Formatter(
        'Time: %(asctime)s\n'
        'Logger: %(name)s\n'
        'Level: %(levelname)s\n'
        'Function: %(funcName)s:%(lineno)d\n'
        'Message: %(message)s'
    )
    smtp_handler.setFormatter(formatter)
    
    logger.addHandler(smtp_handler)
    
    return logger

# Configuration (use environment variables in production)
smtp_config = {
    'host': 'smtp.gmail.com',
    'port': 587,
    'from_addr': 'alerts@myapp.com',
    'to_addrs': ['admin@myapp.com', 'devops@myapp.com'],
    'username': 'alerts@myapp.com',
    'password': 'your_app_password'
}

# Usage
critical_logger = setup_email_alerts('critical_app', smtp_config)
critical_logger.critical('Database connection failed!')
```

### SysLogHandler - System Logging

```python
import logging
from logging.handlers import SysLogHandler

# Syslog handler for Unix/Linux systems
syslog_handler = SysLogHandler(address='/dev/log')
syslog_handler.setLevel(logging.INFO)

# Or for remote syslog server
# syslog_handler = SysLogHandler(address=('syslog.example.com', 514))

formatter = logging.Formatter('%(name)s[%(process)d]: %(levelname)s - %(message)s')
syslog_handler.setFormatter(formatter)

logger = logging.getLogger('syslog_app')
logger.addHandler(syslog_handler)
logger.setLevel(logging.INFO)

logger.info('Application started - logged to syslog')
```

### Custom Handler Example

```python
import logging
import json
from datetime import datetime

class JSONFileHandler(logging.Handler):
    """Custom handler that logs to JSON format"""
    
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
    
    def emit(self, record):
        try:
            # Create log entry as dictionary
            log_entry = {
                'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                'level': record.levelname,
                'logger_name': record.name,
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno,
                'message': record.getMessage(),
                'thread': record.thread,
                'process': record.process
            }
            
            # Add exception info if present
            if record.exc_info:
                log_entry['exception'] = self.format(record)
            
            # Write to file as JSON
            with open(self.filename, 'a') as f:
                json.dump(log_entry, f)
                f.write('\n')
                
        except Exception:
            self.handleError(record)

# Usage
logger = logging.getLogger('json_app')
json_handler = JSONFileHandler('app_logs.json')
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)

logger.info('This will be logged as JSON')
logger.error('Error message with structured data')
```

## Best Practices

### Handler Configuration Best Practices

#### 1. Proper Logger Hierarchy

```python
import logging

# Use hierarchical logger names
main_logger = logging.getLogger('myapp')
db_logger = logging.getLogger('myapp.database')
auth_logger = logging.getLogger('myapp.auth')
api_logger = logging.getLogger('myapp.api')

# Configure root app logger with handlers
main_logger.setLevel(logging.INFO)
# Child loggers inherit handlers unless propagate=False
```

#### 2. Environment-Specific Configuration

```python
import logging
import os

def configure_logging():
    """Configure logging based on environment"""
    
    env = os.getenv('ENVIRONMENT', 'development')
    
    if env == 'development':
        # Development: Console output with debug info
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
    elif env == 'production':
        # Production: File logging with rotation
        setup_production_logging('myapp')
    elif env == 'testing':
        # Testing: Minimal logging to avoid noise
        logging.basicConfig(level=logging.WARNING)

configure_logging()
```

#### 3. Preventing Handler Duplication

```python
import logging

def get_logger(name, log_file=None):
    """Get logger with handlers, preventing duplication"""
    
    logger = logging.getLogger(name)
    
    # Only add handlers if none exist
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            logger.addHandler(file_handler)
    
    return logger

# Safe to call multiple times
logger1 = get_logger('myapp', 'app.log')
logger2 = get_logger('myapp', 'app.log')  # Won't duplicate handlers
```

### Performance Considerations

#### 1. Handler Level Filtering

```python
import logging

# Set appropriate levels to avoid unnecessary processing
logger = logging.getLogger('performance_app')

# Only process INFO and above for file
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)  # Ignore DEBUG messages

# Only process ERROR and above for email
email_handler = SMTPHandler(...)
email_handler.setLevel(logging.ERROR)  # Only critical issues

logger.addHandler(file_handler)
logger.addHandler(email_handler)
```

#### 2. Lazy Formatting

```python
import logging

logger = logging.getLogger('lazy_app')

# Good: Lazy evaluation - format string only if logged
logger.debug('Processing item %s with value %d', item_name, item_value)

# Avoid: Eager evaluation - always formats string
logger.debug(f'Processing item {item_name} with value {item_value}')

# Use isEnabledFor for expensive operations
if logger.isEnabledFor(logging.DEBUG):
    expensive_debug_info = calculate_expensive_debug_data()
    logger.debug('Debug data: %s', expensive_debug_info)
```

#### 3. Buffer Management

```python
import logging
from logging.handlers import MemoryHandler

# Use MemoryHandler to buffer logs and flush periodically
memory_handler = MemoryHandler(
    capacity=100,  # Buffer 100 records
    flushLevel=logging.ERROR,  # Flush immediately on ERROR
    target=logging.FileHandler('buffered.log')
)

logger = logging.getLogger('buffered_app')
logger.addHandler(memory_handler)

# Logs are buffered until capacity is reached or ERROR occurs
for i in range(150):
    logger.info(f'Message {i}')  # First 100 buffered, then flushed

logger.error('This triggers immediate flush of buffer')
```

## Real-World Use Cases

### Use Case 1: Web Application Logging

```python
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os

class WebAppLogger:
    """Production web application logging setup"""
    
    def __init__(self, app_name, log_dir='logs'):
        self.app_name = app_name
        self.log_dir = log_dir
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging for web application"""
        
        # Create log directory
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Main application logger
        self.logger = logging.getLogger(self.app_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()
        
        # 1. Access log (web requests)
        access_handler = TimedRotatingFileHandler(
            f'{self.log_dir}/access.log',
            when='midnight',
            backupCount=90  # 90 days retention
        )
        access_handler.setLevel(logging.INFO)
        access_formatter = logging.Formatter('%(asctime)s - %(message)s')
        access_handler.setFormatter(access_formatter)
        
        # 2. Error log (application errors)
        error_handler = RotatingFileHandler(
            f'{self.log_dir}/error.log',
            maxBytes=100*1024*1024,  # 100MB
            backupCount=10
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
        )
        error_handler.setFormatter(error_formatter)
        
        # 3. Application log (general application events)
        app_handler = RotatingFileHandler(
            f'{self.log_dir}/application.log',
            maxBytes=50*1024*1024,  # 50MB
            backupCount=5
        )
        app_handler.setLevel(logging.INFO)
        app_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
        )
        app_handler.setFormatter(app_formatter)
        
        # Add handlers
        self.logger.addHandler(access_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(app_handler)
        
        # Create specialized loggers
        self.access_logger = logging.getLogger(f'{self.app_name}.access')
        self.access_logger.addHandler(access_handler)
        self.access_logger.propagate = False  # Don't propagate to parent
        
    def log_request(self, request_method, request_path, status_code, response_time):
        """Log web request"""
        self.access_logger.info(f'{request_method} {request_path} {status_code} {response_time}ms')
    
    def log_error(self, error_msg, exception=None):
        """Log application error"""
        if exception:
            self.logger.error(error_msg, exc_info=exception)
        else:
            self.logger.error(error_msg)
    
    def log_info(self, message):
        """Log general information"""
        self.logger.info(message)

# Usage in web application
web_logger = WebAppLogger('my_web_app')

# Log requests
web_logger.log_request('GET', '/api/users', 200, 45)
web_logger.log_request('POST', '/api/login', 401, 23)

# Log application events
web_logger.log_info('Database connection established')
web_logger.log_error('Failed to process payment', ValueError('Invalid card'))
```

### Use Case 2: Data Processing Pipeline

```python
import logging
from logging.handlers import RotatingFileHandler
import json
import time

class DataPipelineLogger:
    """Logging setup for data processing pipelines"""
    
    def __init__(self, pipeline_name):
        self.pipeline_name = pipeline_name
        self.setup_loggers()
        
    def setup_loggers(self):
        """Setup specialized loggers for different pipeline stages"""
        
        base_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # 1. Main pipeline logger
        self.pipeline_logger = logging.getLogger(f'{self.pipeline_name}.pipeline')
        pipeline_handler = RotatingFileHandler(
            f'logs/{self.pipeline_name}_pipeline.log',
            maxBytes=50*1024*1024,
            backupCount=3
        )
        pipeline_handler.setFormatter(logging.Formatter(base_format))
        self.pipeline_logger.addHandler(pipeline_handler)
        self.pipeline_logger.setLevel(logging.INFO)
        
        # 2. Data quality logger
        self.quality_logger = logging.getLogger(f'{self.pipeline_name}.quality')
        quality_handler = RotatingFileHandler(
            f'logs/{self.pipeline_name}_quality.log',
            maxBytes=10*1024*1024,
            backupCount=10
        )
        quality_handler.setFormatter(logging.Formatter(base_format))
        self.quality_logger.addHandler(quality_handler)
        self.quality_logger.setLevel(logging.WARNING)
        
        # 3. Performance logger (JSON format for analysis)
        self.perf_logger = logging.getLogger(f'{self.pipeline_name}.performance')
        perf_handler = RotatingFileHandler(
            f'logs/{self.pipeline_name}_performance.log',
            maxBytes=20*1024*1024,
            backupCount=5
        )
        
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    'timestamp': self.formatTime(record),
                    'level': record.levelname,
                    'stage': getattr(record, 'stage', 'unknown'),
                    'duration': getattr(record, 'duration', 0),
                    'records_processed': getattr(record, 'records_processed', 0),
                    'message': record.getMessage()
                }
                return json.dumps(log_data)
        
        perf_handler.setFormatter(JSONFormatter())
        self.perf_logger.addHandler(perf_handler)
        self.perf_logger.setLevel(logging.INFO)
        
    def log_pipeline_start(self, stage, input_count):
        """Log pipeline stage start"""
        self.pipeline_logger.info(f'Starting {stage} with {input_count} records')
        
    def log_pipeline_complete(self, stage, output_count, duration):
        """Log pipeline stage completion"""
        self.pipeline_logger.info(f'Completed {stage}: {output_count} records in {duration:.2f}s')
        
        # Also log to performance logger with structured data
        extra = {
            'stage': stage,
            'duration': duration,
            'records_processed': output_count
        }
        self.perf_logger.info(f'Stage {stage} completed', extra=extra)
        
    def log_data_quality_issue(self, issue_type, details, severity='WARNING'):
        """Log data quality issues"""
        level = getattr(logging, severity)
        self.quality_logger.log(level, f'{issue_type}: {details}')
        
    def log_error(self, stage, error, record_id=None):
        """Log processing errors"""
        error_msg = f'Error in {stage}'
        if record_id:
            error_msg += f' (Record ID: {record_id})'
        error_msg += f': {error}'
        
        self.pipeline_logger.error(error_msg, exc_info=True)

# Usage in data pipeline
pipeline_logger = DataPipelineLogger('customer_etl')

# Start processing stage
start_time = time.time()
pipeline_logger.log_pipeline_start('data_extraction', 10000)

# Process data with error handling
try:
    # Simulate processing...
    processed_records = 9500
    
    # Log data quality issues
    pipeline_logger.log_data_quality_issue(
        'Missing Email', 
        '500 customer records missing email addresses'
    )
    
    # Log completion
    duration = time.time() - start_time
    pipeline_logger.log_pipeline_complete('data_extraction', processed_records, duration)
    
except Exception as e:
    pipeline_logger.log_error('data_extraction', str(e), record_id='CUST_12345')
```

### Use Case 3: Microservices Architecture

```python
import logging
from logging.handlers import RotatingFileHandler, SysLogHandler
import json
import os
import uuid

class MicroserviceLogger:
    """Logging setup for microservices with correlation tracking"""
    
    def __init__(self, service_name, service_version='1.0.0'):
        self.service_name = service_name
        self.service_version = service_version
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for microservice"""
        
        self.logger = logging.getLogger(self.service_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()
        
        # 1. Console handler for local development
        if os.getenv('ENVIRONMENT') == 'development':
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - [%(correlation_id)s] - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        
        # 2. JSON file handler for structured logging
        json_handler = RotatingFileHandler(
            f'logs/{self.service_name}.json',
            maxBytes=100*1024*1024,
            backupCount=5
        )
        json_handler.setLevel(logging.INFO)
        
        class MicroserviceJSONFormatter(logging.Formatter):
            def format(self, record):
                log_entry = {
                    'timestamp': self.formatTime(record, self.datefmt),
                    'service_name': record.name,
                    'service_version': getattr(record, 'service_version', '1.0.0'),
                    'level': record.levelname,
                    'correlation_id': getattr(record, 'correlation_id', 'N/A'),
                    'user_id': getattr(record, 'user_id', None),
                    'endpoint': getattr(record, 'endpoint', None),
                    'method': getattr(record, 'method', None),
                    'status_code': getattr(record, 'status_code', None),
                    'duration_ms': getattr(record, 'duration_ms', None),
                    'message': record.getMessage(),
                    'module': record.module,
                    'function': record.funcName,
                    'line': record.lineno
                }
                
                if record.exc_info:
                    log_entry['exception'] = self.formatException(record.exc_info)
                    
                return json.dumps(log_entry, default=str)
        
        json_handler.setFormatter(MicroserviceJSONFormatter())
        self.logger.addHandler(json_handler)
        
        # 3. Syslog handler for centralized logging (production)
        if os.getenv('ENVIRONMENT') == 'production':
            syslog_handler = SysLogHandler(address=('localhost', 514))
            syslog_handler.setLevel(logging.WARNING)
            syslog_formatter = logging.Formatter(
                f'{self.service_name}[%(process)d]: %(levelname)s - %(message)s'
            )
            syslog_handler.setFormatter(syslog_formatter)
            self.logger.addHandler(syslog_handler)
    
    def get_logger_with_context(self, correlation_id=None, user_id=None):
        """Get logger with context information"""
        if not correlation_id:
            correlation_id = str(uuid.uuid4())
            
        class ContextAdapter(logging.LoggerAdapter):
            def process(self, msg, kwargs):
                return msg, {
                    **kwargs,
                    'extra': {
                        **kwargs.get('extra', {}),
                        'correlation_id': self.extra['correlation_id'],
                        'user_id': self.extra['user_id'],
                        'service_version': self.extra['service_version']
                    }
                }
        
        return ContextAdapter(self.logger, {
            'correlation_id': correlation_id,
            'user_id': user_id,
            'service_version': self.service_version
        })
    
    def log_api_request(self, method, endpoint, status_code, duration_ms, correlation_id=None, user_id=None):
        """Log API request with context"""
        extra = {
            'correlation_id': correlation_id or str(uuid.uuid4()),
            'user_id': user_id,
            'method': method,
            'endpoint': endpoint,
            'status_code': status_code,
            'duration_ms': duration_ms,
            'service_version': self.service_version
        }
        
        self.logger.info(
            f'{method} {endpoint} {status_code} {duration_ms}ms',
            extra=extra
        )

# Usage in microservice
service_logger = MicroserviceLogger('user-service', '2.1.0')

# Log API requests
correlation_id = str(uuid.uuid4())
service_logger.log_api_request(
    'POST', '/api/users', 201, 145, 
    correlation_id=correlation_id, 
    user_id='user_123'
)

# Use context logger for related operations
logger = service_logger.get_logger_with_context(correlation_id, 'user_123')
logger.info('Processing user registration')
logger.warning('Email validation took longer than expected')
```

### Use Case 4: IoT Device Logging

```python
import logging
from logging.handlers import RotatingFileHandler, HTTPHandler
import json
import time

class IoTDeviceLogger:
    """Logging for IoT devices with local storage and remote sync"""
    
    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for IoT device"""
        
        self.logger = logging.getLogger(f'iot.{self.device_id}')
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()
        
        # 1. Local rotating file handler (space-constrained devices)
        local_handler = RotatingFileHandler(
            f'/var/log/iot_{self.device_id}.log',
            maxBytes=1*1024*1024,  # 1MB (small for IoT)
            backupCount=2          # Only 2 backups
        )
        local_handler.setLevel(logging.INFO)
        
        local_formatter = logging.Formatter(
            '%(asctime)s|%(levelname)s|%(message)s'  # Compact format
        )
        local_handler.setFormatter(local_formatter)
        self.logger.addHandler(local_handler)
        
        # 2. HTTP handler for remote logging (when connected)
        try:
            http_handler = HTTPHandler(
                'logging-server.example.com:8080',
                '/api/logs',
                method='POST'
            )
            http_handler.setLevel(logging.WARNING)  # Only important messages
            
            class IoTJSONFormatter(logging.Formatter):
                def format(self, record):
                    return json.dumps({
                        'device_id': self.device_id,
                        'device_type': self.device_type,
                        'timestamp': self.formatTime(record),
                        'level': record.levelname,
                        'message': record.getMessage(),
                        'sensor_data': getattr(record, 'sensor_data', {}),
                        'location': getattr(record, 'location', None)
                    })
            
            # Set device context
            http_formatter = IoTJSONFormatter()
            http_formatter.device_id = self.device_id
            http_formatter.device_type = self.device_type
            
            http_handler.setFormatter(http_formatter)
            self.logger.addHandler(http_handler)
            
        except Exception:
            # HTTP handler failed - device might be offline
            pass
        
    def log_sensor_reading(self, sensor_type, value, unit, location=None):
        """Log sensor reading"""
        extra = {
            'sensor_data': {
                'sensor_type': sensor_type,
                'value': value,
                'unit': unit,
                'reading_time': time.time()
            },
            'location': location
        }
        
        self.logger.info(
            f'Sensor reading: {sensor_type}={value}{unit}',
            extra=extra
        )
    
    def log_device_status(self, status, battery_level=None, signal_strength=None):
        """Log device status"""
        status_data = {'status': status}
        if battery_level is not None:
            status_data['battery_level'] = battery_level
        if signal_strength is not None:
            status_data['signal_strength'] = signal_strength
            
        extra = {'sensor_data': status_data}
        
        self.logger.info(f'Device status: {status}', extra=extra)
        
        # Log critical battery level
        if battery_level is not None and battery_level < 10:
            self.logger.warning(f'Low battery: {battery_level}%', extra=extra)
    
    def log_error(self, error_type, error_message):
        """Log device error"""
        self.logger.error(f'{error_type}: {error_message}')

# Usage in IoT device
iot_logger = IoTDeviceLogger('TEMP_001', 'temperature_sensor')

# Log sensor readings
iot_logger.log_sensor_reading(
    'temperature', 23.5, '°C', 
    location={'lat': 40.7128, 'lon': -74.0060}
)

# Log device status
iot_logger.log_device_status('operational', battery_level=85, signal_strength=-45)

# Log errors
iot_logger.log_error('SENSOR_FAILURE', 'Temperature sensor not responding')
```

## Configuration Files and External Configuration

### YAML Configuration

```yaml
# logging_config.yaml
version: 1
disable_existing_loggers: false

formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s'
  json:
    format: '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: simple
    stream: ext://sys.stdout

  file_info:
    class: logging.handlers.RotatingFileHandler
    level: INFO
    formatter: detailed
    filename: logs/info.log
    maxBytes: 52428800  # 50MB
    backupCount: 5

  file_error:
    class: logging.handlers.RotatingFileHandler
    level: ERROR
    formatter: detailed
    filename: logs/error.log
    maxBytes: 52428800
    backupCount: 10

  email_critical:
    class: logging.handlers.SMTPHandler
    level: CRITICAL
    formatter: detailed
    mailhost: [smtp.gmail.com, 587]
    fromaddr: alerts@myapp.com
    toaddrs: [admin@myapp.com]
    subject: 'Critical Error Alert'

loggers:
  myapp:
    level: DEBUG
    handlers: [console, file_info, file_error]
    propagate: false

  myapp.database:
    level: INFO
    handlers: [file_info]
    propagate: true

  myapp.auth:
    level: WARNING
    handlers: [console, file_error, email_critical]
    propagate: false

root:
  level: WARNING
  handlers: [console]
```

### Loading YAML Configuration

```python
import logging.config
import yaml
import os

def setup_logging_from_config(config_path='logging_config.yaml'):
    """Load logging configuration from YAML file"""
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        logging.config.dictConfig(config)
        
        logger = logging.getLogger('myapp')
        logger.info('Logging configured from YAML file')
        return logger
    else:
        # Fallback to basic configuration
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger('myapp')
        logger.warning(f'Config file {config_path} not found, using basic configuration')
        return logger

# Usage
logger = setup_logging_from_config()
logger.info('Application started with YAML configuration')
```

### JSON Configuration

```python
import logging.config
import json

# logging_config.json
config_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "rotating_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "logs/app.log",
            "maxBytes": 52428800,
            "backupCount": 5
        }
    },
    "loggers": {
        "myapp": {
            "level": "DEBUG",
            "handlers": ["console", "rotating_file"],
            "propagate": False
        }
    }
}

# Apply configuration
logging.config.dictConfig(config_dict)
logger = logging.getLogger('myapp')
logger.info('Configured via dictionary')
```

## Testing and Debugging Log Handlers

### Testing Handler Configuration

```python
import logging
import tempfile
import os
from logging.handlers import RotatingFileHandler

def test_logging_setup():
    """Test logging configuration"""
    
    # Create temporary log file
    temp_dir = tempfile.mkdtemp()
    log_file = os.path.join(temp_dir, 'test.log')
    
    # Setup logger
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.DEBUG)
    
    # Add handler
    handler = RotatingFileHandler(log_file, maxBytes=1024, backupCount=2)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Test logging
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    
    # Verify file was created and contains logs
    assert os.path.exists(log_file), "Log file was not created"
    
    with open(log_file, 'r') as f:
        content = f.read()
        assert 'INFO - Info message' in content
        assert 'ERROR - Error message' in content
        print("✓ Logging test passed")
    
    # Test rotation
    for i in range(100):
        logger.info(f'Rotation test message {i}')
    
    # Check if rotation occurred
    log_files = [f for f in os.listdir(temp_dir) if f.startswith('test.log')]
    print(f"✓ Rotation test: {len(log_files)} log files created")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)

if __name__ == '__main__':
    test_logging_setup()
```

### Memory Handler for Testing

```python
import logging
from io import StringIO

class TestLogHandler(logging.Handler):
    """Custom handler for capturing logs during testing"""
    
    def __init__(self):
        super().__init__()
        self.records = []
        
    def emit(self, record):
        self.records.append(record)
        
    def get_messages(self, level=None):
        """Get log messages, optionally filtered by level"""
        if level:
            return [r.getMessage() for r in self.records if r.levelno == level]
        return [r.getMessage() for r in self.records]
    
    def clear(self):
        """Clear captured records"""
        self.records.clear()

# Usage in tests
def test_application_function():
    """Test function with log capture"""
    
    # Setup test logger
    logger = logging.getLogger('test_app')
    test_handler = TestLogHandler()
    logger.addHandler(test_handler)
    logger.setLevel(logging.DEBUG)
    
    # Function to test
    def process_data(items):
        logger.info(f'Processing {len(items)} items')
        for item in items:
            if item < 0:
                logger.warning(f'Negative value found: {item}')
        logger.info('Processing completed')
    
    # Test the function
    test_data = [1, 2, -3, 4, -5]
    process_data(test_data)
    
    # Verify logs
    messages = test_handler.get_messages()
    assert 'Processing 5 items' in messages[0]
    assert 'Processing completed' in messages[-1]
    
    warning_messages = test_handler.get_messages(logging.WARNING)
    assert len(warning_messages) == 2  # Two negative values
    
    print("✓ Application function test passed")

test_application_function()
```

## Summary

### Key Concepts Mastered

- **Handler Purpose**: Route log messages to different destinations (console, files, email, etc.)
- **Handler Types**: StreamHandler, FileHandler, RotatingFileHandler, TimedRotatingFileHandler, SMTPHandler
- **Multiple Handlers**: Send logs to multiple destinations simultaneously with different levels
- **Log Rotation**: Prevent disk space issues with automatic file rotation
- **Formatters**: Control message format and content for each destination

### Essential Handler Types

- **StreamHandler**: Console output for development and real-time monitoring
- **FileHandler**: Simple file logging for persistent storage
- **RotatingFileHandler**: Size-based rotation for production applications
- **TimedRotatingFileHandler**: Time-based rotation for archival and compliance
- **SMTPHandler**: Email notifications for critical errors

### Best Practices Applied

✅ **Environment-specific configuration** - Different setups for dev/test/prod  
✅ **Proper level filtering** - Avoid unnecessary processing and storage  
✅ **Handler deduplication** - Prevent adding handlers multiple times  
✅ **Log rotation** - Manage disk space with size and time-based rotation  
✅ **Structured logging** - Use JSON format for machine-readable logs  
✅ **Context preservation** - Include correlation IDs and user context

### Production Considerations

- **Multiple outputs**: Console for monitoring, files for persistence, email for alerts
- **Rotation strategy**: Balance between retention needs and disk space
- **Performance impact**: Use appropriate levels and lazy formatting
- **Security**: Sanitize sensitive data before logging
- **Monitoring**: Set up alerts for error patterns and log volume

### Real-World Applications

- **Web Applications**: Access logs, error logs, application logs
- **Data Pipelines**: Processing logs, quality logs, performance logs
- **Microservices**: Distributed tracing with correlation IDs
- **IoT Devices**: Local storage with remote sync capabilities
- **APIs**: Request/response logging with structured data

### What You Can Do Now

- ✅ Configure multiple handlers for different output destinations
- ✅ Implement log rotation strategies for production applications
- ✅ Set up environment-specific logging configurations
- ✅ Create custom handlers for specialized logging needs
- ✅ Use structured logging for better log analysis
- ✅ Test and debug logging configurations effectively
- ✅ Design logging architecture for distributed systems

### Next Steps

- Learn about [[Python Logging Formatters]] for advanced message formatting
- Explore [[Python Logging Filters]] for fine-grained log control
- Study [[Centralized Logging]] patterns for distributed systems
- Practice [[Log Analysis]] techniques for troubleshooting
- Investigate [[Logging Performance]] optimization strategies

> [!tip] Production Checklist Before deploying logging to production:
> 
> - ✅ Configure log rotation to prevent disk fill-up
> - ✅ Set appropriate log levels for each environment
> - ✅ Test handler configuration under load
> - ✅ Set up monitoring for log volume and error rates
> - ✅ Implement log retention policies for compliance
> - ✅ Sanitize sensitive data in log messages

---

_Tags: #Python #Logging #LogHandlers #StreamHandler #FileHandler #RotatingFileHandler #ProductionLogging #LogRotation #MultipleHandlers #PythonDevelopment_