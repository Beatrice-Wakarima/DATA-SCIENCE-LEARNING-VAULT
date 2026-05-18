# Downloading Data with curl and wget

#Linux #DataProcessing #curl #wget #CLI

**Related:** [[Linux Basics]] | [[Data Engineering Tools]] | [[Command Line Interface]] | [[Network Protocols]]

---

## Overview

This guide covers downloading data using two essential command-line tools: `curl` and `wget`. Both tools are powerful for data acquisition, API interactions, and automated downloads in data engineering workflows.

**Prerequisites:** Basic [[Linux Basics]] knowledge and familiarity with [[Command Line Interface]]

---

## Module 1: curl Basics

### What is curl?

`curl` (Client URL) is a command-line tool for transferring data from or to servers using various protocols (HTTP, HTTPS, FTP, SFTP, etc.). It's particularly useful for API interactions and testing web services.

### Basic curl Syntax

```bash
curl [options] [URL]
```

### Essential curl Commands

#### 1. Basic GET Request

```bash
# Download a webpage
curl https://example.com

# Save output to file
curl https://example.com > webpage.html
curl -o webpage.html https://example.com
```

#### 2. Follow Redirects

```bash
# Follow HTTP redirects automatically
curl -L https://bit.ly/shortened-url
```

#### 3. Download Files

```bash
# Download and save with original filename
curl -O https://example.com/data.csv

# Download with custom filename
curl -o mydata.csv https://example.com/data.csv
```

#### 4. Show Headers and Progress

```bash
# Include response headers in output
curl -i https://api.example.com/data

# Show only headers
curl -I https://api.example.com/data

# Show progress bar
curl -# -O https://example.com/largefile.zip
```

#### 5. Handle Authentication

```bash
# Basic authentication
curl -u username:password https://api.example.com/data

# Bearer token authentication
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/data

# API key in header
curl -H "X-API-Key: YOUR_API_KEY" https://api.example.com/data
```

### XP Tasks - curl Basics

- [ ] Download a webpage using basic curl command
- [ ] Save a file with `-O` flag from a public API
- [ ] Use `-L` to follow a redirect URL
- [ ] Download a file showing progress with `-#`
- [ ] Get only headers from a website using `-I`
- [ ] Download data from an API requiring authentication

---

## Module 2: wget Basics

### What is wget?

`wget` (World Wide Web get) is a non-interactive command-line utility for downloading files from the web. It's excellent for recursive downloads, resuming interrupted downloads, and batch operations.

### Basic wget Syntax

```bash
wget [options] [URL]
```

### Essential wget Commands

#### 1. Basic File Download

```bash
# Download a single file
wget https://example.com/data.csv

# Download with custom filename
wget -O mydata.csv https://example.com/data.csv
```

#### 2. Resume Downloads

```bash
# Resume interrupted download
wget -c https://example.com/largefile.zip
```

#### 3. Background Downloads

```bash
# Download in background
wget -b https://example.com/largefile.zip

# Check background job status
tail -f wget-log
```

#### 4. Limit Download Speed

```bash
# Limit to 200KB/s
wget --limit-rate=200k https://example.com/largefile.zip
```

#### 5. Retry and Timeout Settings

```bash
# Set retry attempts and timeout
wget --tries=3 --timeout=30 https://example.com/data.csv

# Wait between retries
wget --waitretry=5 --tries=3 https://example.com/data.csv
```

#### 6. User Agent and Headers

```bash
# Set custom user agent
wget --user-agent="Mozilla/5.0" https://example.com/data.csv

# Add custom headers
wget --header="Accept: application/json" https://api.example.com/data
```

### XP Tasks - wget Basics

- [ ] Download a file using basic wget command
- [ ] Resume an interrupted download with `-c`
- [ ] Download a file in background with `-b`
- [ ] Set download speed limit to 100KB/s
- [ ] Download with custom user agent string
- [ ] Set retry attempts and timeout values

---

## Module 3: Advanced wget Features

### Recursive Downloads

#### 1. Download Entire Websites

```bash
# Download entire website (be careful!)
wget -r -np -k -p https://example.com/

# Limit recursion depth
wget -r -l 2 https://example.com/
```

#### 2. Download Specific File Types

```bash
# Download only PDF files
wget -r -A "*.pdf" https://example.com/documents/

# Exclude certain file types
wget -r -R "*.jpg,*.png" https://example.com/
```

#### 3. Mirror Websites

```bash
# Mirror a website locally
wget -m -k -p -np https://example.com/

# With progress and verbose output
wget -m -k -p -np -v --progress=bar https://example.com/
```

### Advanced Options

#### 1. Parallel Downloads

```bash
# Download multiple files in parallel
echo -e "https://example.com/file1.csv\nhttps://example.com/file2.csv" | xargs -n 1 -P 4 wget
```

#### 2. Input from File

```bash
# Download URLs from a file
wget -i urls.txt

# Example urls.txt content:
# https://example.com/data1.csv
# https://example.com/data2.json
# https://example.com/data3.xml
```

#### 3. Directory Structure

```bash
# Preserve directory structure
wget -r -nH --cut-dirs=1 https://example.com/data/

# Create custom directory structure
wget -P /custom/path/ https://example.com/data.csv
```

#### 4. Conditional Downloads

```bash
# Download only if newer than local file
wget -N https://example.com/data.csv

# Check if file exists remotely before download
wget --spider https://example.com/data.csv
```

### Authentication and Cookies

#### 1. HTTP Authentication

```bash
# Basic authentication
wget --user=username --password=password https://secure.example.com/data.csv

# Prompt for password
wget --user=username --ask-password https://secure.example.com/data.csv
```

#### 2. Cookie Handling

```bash
# Save cookies to file
wget --save-cookies cookies.txt --keep-session-cookies https://example.com/login

# Use saved cookies
wget --load-cookies cookies.txt https://example.com/protected-data.csv
```

### XP Tasks - Advanced wget

- [ ] Download all PDFs from a website using `-A "*.pdf"`
- [ ] Mirror a small website section with depth limit of 2
- [ ] Download files listed in a text file using `-i`
- [ ] Use conditional download with `-N` flag
- [ ] Download with custom directory structure using `-P`
- [ ] Test file existence with `--spider` before downloading

---

## Module 4: Comparison and Best Practices

### curl vs wget Quick Reference

|Feature|curl|wget|
|---|---|---|
|**Best for**|API calls, testing|File downloads, mirroring|
|**Protocols**|Many (HTTP, FTP, SFTP, etc.)|HTTP, HTTPS, FTP|
|**Recursive downloads**|No|Yes|
|**Resume downloads**|Manual|Built-in (-c)|
|**Output to stdout**|Default|With -O -|
|**POST data**|Easy (-d flag)|More complex|
|**JSON APIs**|Excellent|Good|

### When to Use curl

- **API interactions** and testing endpoints
- **Sending POST/PUT requests** with data
- **Quick data retrieval** to stdout
- **Protocol testing** (FTP, SFTP, etc.)
- **Integration in scripts** requiring output parsing

### When to Use wget

- **Large file downloads** with resume capability
- **Recursive downloads** and website mirroring
- **Batch downloads** from file lists
- **Unattended downloads** in background
- **Preserving directory structure**

### Best Practices

#### 1. Error Handling in Scripts

```bash
#!/bin/bash
# curl with error handling
if curl -f -s -o data.json "https://api.example.com/data"; then
    echo "Download successful"
else
    echo "Download failed with code $?"
    exit 1
fi

# wget with error handling
if wget -q -O data.csv "https://example.com/data.csv"; then
    echo "Download successful"
else
    echo "Download failed"
    exit 1
fi
```

#### 2. Rate Limiting and Politeness

```bash
# Be respectful to servers
wget --wait=1 --random-wait --limit-rate=200k -r https://example.com/

# Add delays between curl requests in loops
for url in "${urls[@]}"; do
    curl -o "data_$(basename "$url")" "$url"
    sleep 2  # Wait 2 seconds between requests
done
```

#### 3. Logging and Monitoring

```bash
# curl with verbose logging
curl -v -o data.json https://api.example.com/data 2> curl.log

# wget with detailed logging
wget --progress=bar --verbose -o wget.log https://example.com/data.csv
```

---

## Module 5: Capstone Project

### Project: Automated Data Collection Pipeline

Create a comprehensive data collection script that combines curl and wget to gather data from multiple sources.

#### Project Requirements

1. **API Data Collection**: Use curl to fetch JSON data from a REST API
2. **File Downloads**: Use wget to download CSV files from web sources
3. **Error Handling**: Implement proper error checking and logging
4. **Data Organization**: Structure downloaded data in organized directories
5. **Automation**: Make the script configurable and reusable

#### Implementation Script

```bash
#!/bin/bash
# data_collection_pipeline.sh
# Comprehensive data collection using curl and wget

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Configuration
DATA_DIR="./collected_data"
LOG_FILE="$DATA_DIR/collection.log"
API_BASE="https://jsonplaceholder.typicode.com"
FILE_SOURCES=(
    "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
    "https://raw.githubusercontent.com/datasets/population/master/data/population.csv"
)

# Create directory structure
setup_directories() {
    mkdir -p "$DATA_DIR"/{api_data,files,logs}
    touch "$LOG_FILE"
}

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Collect API data using curl
collect_api_data() {
    log "Starting API data collection..."
    
    # Fetch posts
    if curl -f -s -o "$DATA_DIR/api_data/posts.json" "$API_BASE/posts"; then
        log "✓ Posts data collected successfully"
    else
        log "✗ Failed to collect posts data"
        return 1
    fi
    
    # Fetch users
    if curl -f -s -o "$DATA_DIR/api_data/users.json" "$API_BASE/users"; then
        log "✓ Users data collected successfully"
    else
        log "✗ Failed to collect users data"
        return 1
    fi
    
    # Fetch comments
    if curl -f -s -o "$DATA_DIR/api_data/comments.json" "$API_BASE/comments"; then
        log "✓ Comments data collected successfully"
    else
        log "✗ Failed to collect comments data"
        return 1
    fi
}

# Download files using wget
download_files() {
    log "Starting file downloads..."
    
    for url in "${FILE_SOURCES[@]}"; do
        filename=$(basename "$url")
        log "Downloading $filename..."
        
        if wget -q -P "$DATA_DIR/files/" "$url"; then
            log "✓ Downloaded $filename successfully"
        else
            log "✗ Failed to download $filename"
        fi
        
        # Be polite - wait between downloads
        sleep 2
    done
}

# Verify downloaded data
verify_data() {
    log "Verifying downloaded data..."
    
    # Check API data files
    for file in posts.json users.json comments.json; do
        filepath="$DATA_DIR/api_data/$file"
        if [[ -f "$filepath" ]] && [[ -s "$filepath" ]]; then
            log "✓ $file is present and not empty"
        else
            log "✗ $file is missing or empty"
        fi
    done
    
    # Check downloaded files
    for url in "${FILE_SOURCES[@]}"; do
        filename=$(basename "$url")
        filepath="$DATA_DIR/files/$filename"
        if [[ -f "$filepath" ]] && [[ -s "$filepath" ]]; then
            log "✓ $filename is present and not empty"
        else
            log "✗ $filename is missing or empty"
        fi
    done
}

# Generate summary report
generate_report() {
    log "Generating collection report..."
    
    report_file="$DATA_DIR/collection_report.txt"
    {
        echo "Data Collection Report"
        echo "======================"
        echo "Generated: $(date)"
        echo
        echo "API Data Files:"
        find "$DATA_DIR/api_data" -name "*.json" -exec basename {} \; | sort
        echo
        echo "Downloaded Files:"
        find "$DATA_DIR/files" -name "*.*" -exec basename {} \; | sort
        echo
        echo "File Sizes:"
        find "$DATA_DIR" -type f -name "*.*" -exec du -h {} \; | sort
    } > "$report_file"
    
    log "✓ Report generated: $report_file"
}

# Main execution
main() {
    log "Starting data collection pipeline..."
    
    setup_directories
    collect_api_data
    download_files
    verify_data
    generate_report
    
    log "Data collection pipeline completed!"
    echo "Check $DATA_DIR for collected data and logs."
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

### Capstone XP Tasks

- [ ] Set up the directory structure for the project
- [ ] Implement API data collection using curl with error handling
- [ ] Add file download functionality using wget
- [ ] Create logging mechanism for monitoring progress
- [ ] Test the complete pipeline script
- [ ] Modify script to add your own data sources
- [ ] Add data validation checks
- [ ] Create a scheduling mechanism (cron job) for automated runs

### Advanced Extensions

#### 1. Enhanced Error Handling

```bash
# Add retry logic
retry_download() {
    local url=$1
    local output=$2
    local max_attempts=3
    
    for attempt in $(seq 1 $max_attempts); do
        if curl -f -s -o "$output" "$url"; then
            return 0
        else
            log "Attempt $attempt failed, retrying in 5 seconds..."
            sleep 5
        fi
    done
    return 1
}
```

#### 2. Configuration File Support

```bash
# config.json
{
    "data_dir": "./collected_data",
    "api_sources": [
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/users"
    ],
    "file_sources": [
        "https://example.com/data1.csv",
        "https://example.com/data2.json"
    ],
    "settings": {
        "max_retries": 3,
        "delay_between_requests": 2,
        "timeout": 30
    }
}
```

#### 3. Data Processing Integration

```bash
# Add data processing after collection
process_collected_data() {
    log "Processing collected data..."
    
    # Convert JSON to CSV using jq
    if command -v jq &> /dev/null; then
        jq -r '.[] | [.id, .title, .userId] | @csv' \
            "$DATA_DIR/api_data/posts.json" > "$DATA_DIR/processed/posts.csv"
        log "✓ Processed posts.json to CSV"
    fi
}
```

---

## Quick Reference Cheat Sheet

### curl Quick Commands

```bash
# Basic download
curl -O https://example.com/file.csv

# With authentication
curl -H "Authorization: Bearer TOKEN" https://api.example.com/data

# POST with JSON data
curl -X POST -H "Content-Type: application/json" \
     -d '{"key":"value"}' https://api.example.com/endpoint

# Follow redirects and show progress
curl -L -# -O https://example.com/file.zip
```

### wget Quick Commands

```bash
# Basic download with resume support
wget -c https://example.com/largefile.zip

# Download in background
wget -b https://example.com/file.csv

# Recursive with file type filter
wget -r -A "*.pdf" https://example.com/documents/

# Download from URL list
wget -i urls.txt
```

### Common Use Cases

|Task|Command|
|---|---|
|**Download single file**|`curl -O URL` or `wget URL`|
|**Resume download**|`wget -c URL`|
|**API call with auth**|`curl -H "Authorization: Bearer TOKEN" URL`|
|**Download all PDFs**|`wget -r -A "*.pdf" URL`|
|**Background download**|`wget -b URL`|
|**Download with progress**|`curl -# -O URL`|

---

## Related Topics

- [[HTTP Status Codes]] - Understanding response codes
- [[JSON Processing]] - Working with API responses
- [[CSV Data Handling]] - Processing downloaded CSV files
- [[Bash Scripting]] - Automating download workflows
- [[Data Engineering Tools]] - Integration with ETL pipelines
- [[Network Security]] - Secure data transfer practices

---

**Tags:** #Linux #DataProcessing #curl #wget #CLI #DataEngineering #Automation #NetworkTools