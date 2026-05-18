# Complete Shell Usage Guide - Linux/Unix

## Table of Contents

- [[#Basics of Shell]]
- [[#File System Navigation]]
- [[#File Permissions & Ownership]]
- [[#Process Management]]
- [[#Networking with Shell]]
- [[#Compression and Archiving]]
- [[#Search and Filters]]
- [[#Scripting Basics]]
- [[#Advanced Shell Tricks]]
- [[#Secure Shell Usage (SSH)]]
- [[#Best Practices for Security]]
- [[#Troubleshooting and Debugging]]

## Basics of Shell

### Shell Types and Selection

```bash
# Check current shell
echo $SHELL

# List available shells
cat /etc/shells

# Change shell temporarily
bash
zsh
fish

# Change default shell
chsh -s /bin/bash
chsh -s /bin/zsh
```

### Essential Commands

```bash
# System information
whoami          # Current user
id              # User and group IDs
uname -a        # System information
date            # Current date and time
uptime          # System uptime
hostname        # Machine name

# Help and documentation
man command     # Manual pages
info command    # Info documents  
command --help  # Built-in help
which command   # Command location
type command    # Command type
```

> [!tip] Command Structure Most commands follow: `command [options] [arguments]`
> 
> - Options: `-h` (short) or `--help` (long)
> - Multiple options: `-la` or `-l -a`

### Command History

```bash
# History commands
history         # Show command history
!!              # Execute last command
!n              # Execute command number n
!string         # Execute last command starting with string
^old^new        # Replace 'old' with 'new' in last command

# History search
Ctrl+R          # Reverse search
Ctrl+G          # Cancel search
Ctrl+P          # Previous command
Ctrl+N          # Next command
```

## File System Navigation

### Directory Operations

```bash
# Navigation
pwd             # Print working directory
cd /path/to/dir # Change directory
cd ~            # Home directory
cd -            # Previous directory
cd ..           # Parent directory
cd ../..        # Two levels up

# Directory listing
ls              # Basic listing
ls -l           # Long format
ls -la          # Include hidden files
ls -lh          # Human-readable sizes
ls -lt          # Sort by time
ls -lR          # Recursive listing

# Directory management
mkdir directory           # Create directory
mkdir -p path/to/nested  # Create nested directories
rmdir directory          # Remove empty directory
rm -rf directory         # Remove directory recursively
```

### File Operations

```bash
# File creation and editing
touch filename          # Create empty file or update timestamp
nano filename          # Simple text editor
vim filename           # Advanced text editor
emacs filename         # Emacs editor

# File copying and moving
cp source destination           # Copy file
cp -r source_dir dest_dir      # Copy directory recursively
cp -p file1 file2              # Preserve permissions
mv oldname newname             # Rename/move file
mv file directory/             # Move to directory

# File deletion
rm filename            # Remove file
rm -i filename         # Interactive removal
rm -f filename         # Force removal
rm -rf directory       # Remove directory and contents

# File viewing
cat filename           # Display entire file
less filename          # Page through file
more filename          # Page through file (limited)
head filename          # First 10 lines
head -n 20 filename    # First 20 lines
tail filename          # Last 10 lines
tail -f filename       # Follow file changes
```

### File Information

```bash
# File details
file filename          # File type information
stat filename          # Detailed file statistics
du -h filename         # File size
du -sh directory       # Directory size
df -h                  # Disk usage
wc filename            # Word, line, character count
wc -l filename         # Line count only
```

## File Permissions & Ownership

### Understanding Permissions

```bash
# Permission display
ls -l filename
# Output: -rw-r--r-- 1 user group 1024 Jan 1 12:00 filename
#         |        |   |    |     |    |           |
#         type     |   user group size date       name
#                  permissions
```

> [!note] Permission Types
> 
> - **r** (read): 4
> - **w** (write): 2
> - **x** (execute): 1
> - **-** (no permission): 0

### Changing Permissions

```bash
# Chmod with octal notation
chmod 755 filename     # rwxr-xr-x
chmod 644 filename     # rw-r--r--
chmod 600 filename     # rw-------
chmod 777 filename     # rwxrwxrwx (avoid this)

# Chmod with symbolic notation
chmod u+x filename     # Add execute for user
chmod g-w filename     # Remove write for group
chmod o=r filename     # Set read-only for others
chmod a+x filename     # Add execute for all
chmod u+rwx,g+rx,o+r filename  # Complex permissions

# Recursive permissions
chmod -R 755 directory/
```

### Ownership Management

```bash
# Change ownership
sudo chown user filename           # Change user
sudo chown user:group filename     # Change user and group
sudo chown :group filename         # Change group only
sudo chgrp group filename          # Change group

# Recursive ownership
sudo chown -R user:group directory/

# Special permissions
chmod u+s filename     # Set SUID bit
chmod g+s filename     # Set SGID bit
chmod +t directory     # Set sticky bit
```

> [!warning] Security Warning Be extremely careful with `chmod 777` and SUID permissions as they can create security vulnerabilities.

## Process Management

### Viewing Processes

```bash
# Process listing
ps                     # Current user processes
ps aux                 # All processes (detailed)
ps -ef                 # All processes (alternative format)
pstree                 # Process tree
top                    # Dynamic process view
htop                   # Enhanced process viewer
jobs                   # Current shell jobs

# Process filtering
ps aux | grep process_name
pgrep process_name
pidof process_name
```

### Process Control

```bash
# Running processes
command &              # Run in background
nohup command &         # Run immune to hangups
screen command          # Run in screen session
tmux                   # Terminal multiplexer

# Job control
Ctrl+C                 # Interrupt (SIGTERM)
Ctrl+Z                 # Suspend (SIGTSTP)
bg                     # Resume in background
fg                     # Resume in foreground
fg %1                  # Resume job 1 in foreground

# Process termination
kill PID               # Send SIGTERM
kill -9 PID            # Send SIGKILL (force)
kill -15 PID           # Send SIGTERM (graceful)
killall process_name   # Kill by name
pkill pattern          # Kill by pattern
```

### System Monitoring

```bash
# System resources
free -h                # Memory usage
df -h                  # Disk usage
iostat                 # I/O statistics
vmstat                 # Virtual memory statistics
lsof                   # List open files
netstat -tulpn         # Network connections

# Process monitoring
watch "ps aux | grep process"
watch -n 2 "free -h"
```

## Networking with Shell

### Network Information

```bash
# Network configuration
ip addr show           # IP addresses (modern)
ifconfig              # IP addresses (legacy)
ip route show         # Routing table
route -n              # Routing table (legacy)
hostname -I           # Local IP addresses

# Network connectivity
ping hostname         # Test connectivity
ping -c 4 hostname    # Ping 4 times
traceroute hostname   # Trace network path
mtr hostname          # Dynamic traceroute
nslookup hostname     # DNS lookup
dig hostname          # DNS lookup (detailed)
```

### Network Services

```bash
# Port scanning and services
nmap hostname         # Port scan
netstat -tulpn        # Listening services
ss -tulpn            # Socket statistics (modern)
lsof -i :port        # Process using port

# Network file transfer
wget URL             # Download file
curl URL             # Transfer data
curl -O URL          # Download with original filename
rsync source dest    # Synchronize files
```

### Firewall Management

```bash
# UFW (Ubuntu/Debian)
sudo ufw status              # Check status
sudo ufw enable              # Enable firewall
sudo ufw allow 22            # Allow SSH
sudo ufw allow ssh           # Allow SSH by name
sudo ufw deny 80             # Deny HTTP

# iptables (Advanced)
sudo iptables -L             # List rules
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

## Compression and Archiving

### Tar Archives

```bash
# Creating archives
tar -czf archive.tar.gz directory/    # Create gzip compressed
tar -cjf archive.tar.bz2 directory/   # Create bzip2 compressed
tar -cJf archive.tar.xz directory/    # Create xz compressed
tar -cf archive.tar directory/        # Create uncompressed

# Extracting archives
tar -xzf archive.tar.gz               # Extract gzip
tar -xjf archive.tar.bz2              # Extract bzip2
tar -xJf archive.tar.xz               # Extract xz
tar -xf archive.tar                   # Extract uncompressed

# Listing archive contents
tar -tzf archive.tar.gz               # List gzip contents
tar -tf archive.tar                   # List contents

# Advanced tar options
tar -czf backup.tar.gz --exclude='*.log' directory/
tar -xzf archive.tar.gz -C /destination/path/
```

### Compression Utilities

```bash
# Gzip compression
gzip filename          # Compress file
gunzip filename.gz     # Decompress file
zcat filename.gz       # View compressed file

# Other compression formats
zip archive.zip files/         # Create ZIP archive
unzip archive.zip             # Extract ZIP archive
unzip -l archive.zip          # List ZIP contents

# 7zip (if available)
7z a archive.7z directory/    # Create 7z archive
7z x archive.7z               # Extract 7z archive
```

## Search and Filters

### File Search with Find

```bash
# Basic find syntax
find /path -name "filename"           # Find by name
find . -name "*.txt"                  # Find by pattern
find /home -user username             # Find by owner
find . -type f                        # Find files only
find . -type d                        # Find directories only
find . -size +100M                    # Find files > 100MB
find . -mtime -7                      # Modified in last 7 days
find . -perm 755                      # Find by permissions

# Advanced find operations
find . -name "*.log" -delete          # Find and delete
find . -name "*.txt" -exec ls -l {} \;    # Find and execute command
find . -empty                         # Find empty files/directories
find . -name "*.tmp" -o -name "*.bak" # OR condition
```

### Text Search with Grep

```bash
# Basic grep usage
grep "pattern" filename               # Search in file
grep -r "pattern" directory/          # Recursive search
grep -i "pattern" filename            # Case insensitive
grep -v "pattern" filename            # Invert match (exclude)
grep -n "pattern" filename            # Show line numbers
grep -c "pattern" filename            # Count matches
grep -l "pattern" *.txt               # List matching files only

# Advanced grep patterns
grep "^start" filename                # Lines starting with "start"
grep "end$" filename                  # Lines ending with "end"
grep -E "pattern1|pattern2" filename  # Extended regex (OR)
grep -w "word" filename               # Match whole words
grep -A 3 -B 3 "pattern" filename     # Show 3 lines before/after
```

### Regular Expressions

```bash
# Basic regex patterns
.           # Any single character
*           # Zero or more of preceding
+           # One or more of preceding  
?           # Zero or one of preceding
^           # Start of line
$           # End of line
[abc]       # Character class
[a-z]       # Character range
[^abc]      # Negated character class
\d          # Digit
\w          # Word character
\s          # Whitespace

# Examples
grep -E "^[0-9]{3}-[0-9]{3}-[0-9]{4}$" file    # Phone numbers
grep -E "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" file  # Email
```

### Stream Processing

```bash
# Cut - extract columns
cut -d',' -f1,3 file.csv             # Extract columns 1 and 3
cut -c1-10 filename                   # Extract characters 1-10

# Sort and unique
sort filename                         # Sort lines
sort -n filename                      # Numeric sort
sort -r filename                      # Reverse sort
uniq filename                         # Remove duplicates
sort filename | uniq -c               # Count occurrences

# Awk - pattern processing
awk '{print $1}' filename             # Print first column
awk -F',' '{print $2}' file.csv       # CSV processing
awk '/pattern/ {print}' filename      # Print matching lines
awk '{sum+=$1} END {print sum}' file  # Sum first column

# Sed - stream editor
sed 's/old/new/g' filename            # Replace all occurrences
sed '1d' filename                     # Delete first line
sed -n '10,20p' filename              # Print lines 10-20
sed -i 's/old/new/g' filename         # In-place editing
```

## Scripting Basics

### Shell Script Structure

```bash
#!/bin/bash
# Script header and comments

# Variables
NAME="John"
AGE=30
readonly CONSTANT="unchangeable"

# User input
read -p "Enter your name: " USERNAME
read -s -p "Enter password: " PASSWORD  # Silent input

# Command line arguments
echo "Script name: $0"
echo "First argument: $1"
echo "All arguments: $@"
echo "Number of arguments: $#"

# Exit codes
exit 0  # Success
exit 1  # General error
```

### Conditional Statements

```bash
# If statements
if [ "$AGE" -gt 18 ]; then
    echo "Adult"
elif [ "$AGE" -eq 18 ]; then
    echo "Just turned adult"
else
    echo "Minor"
fi

# File tests
if [ -f "$filename" ]; then
    echo "File exists"
fi

if [ -d "$directory" ]; then
    echo "Directory exists"
fi

# String comparisons
if [ "$string1" = "$string2" ]; then
    echo "Strings are equal"
fi

# Numeric comparisons
if [ "$num1" -eq "$num2" ]; then    # Equal
if [ "$num1" -ne "$num2" ]; then    # Not equal
if [ "$num1" -gt "$num2" ]; then    # Greater than
if [ "$num1" -lt "$num2" ]; then    # Less than
```

### Loops

```bash
# For loops
for i in {1..10}; do
    echo "Number: $i"
done

for file in *.txt; do
    echo "Processing $file"
done

for arg in "$@"; do
    echo "Argument: $arg"
done

# While loops
counter=1
while [ $counter -le 10 ]; do
    echo "Count: $counter"
    counter=$((counter + 1))
done

# Until loops
until [ $counter -gt 10 ]; do
    echo "Count: $counter"
    counter=$((counter + 1))
done
```

### Functions

```bash
# Function definition
function greet() {
    echo "Hello, $1!"
    return 0
}

# Alternative syntax
backup_file() {
    local source="$1"
    local destination="$2"
    
    if [ -f "$source" ]; then
        cp "$source" "$destination"
        echo "Backup completed: $destination"
        return 0
    else
        echo "Source file not found: $source"
        return 1
    fi
}

# Function calls
greet "Alice"
backup_file "/etc/hosts" "/backup/hosts.bak"
```

### Error Handling

```bash
# Set error handling options
set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Exit on pipe failure

# Error handling in functions
safe_command() {
    command_that_might_fail || {
        echo "Command failed"
        exit 1
    }
}

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> /var/log/script.log
}
```

## Advanced Shell Tricks

### Input/Output Redirection

```bash
# Output redirection
command > file              # Redirect stdout to file (overwrite)
command >> file             # Redirect stdout to file (append)
command 2> file             # Redirect stderr to file
command 2>&1               # Redirect stderr to stdout
command > file 2>&1        # Redirect both stdout and stderr
command &> file            # Redirect both (bash shortcut)

# Input redirection
command < file             # Use file as input
command << EOF             # Here document
This is input
EOF

# Null device
command > /dev/null        # Discard output
command 2> /dev/null       # Discard errors
```

### Pipes and Filters

```bash
# Basic piping
ps aux | grep nginx                    # Process list to grep
cat file | sort | uniq                 # Chain multiple commands
ls -l | awk '{print $1, $9}'          # Extract permissions and names

# Tee - split output
command | tee file.txt                 # Output to both terminal and file
command | tee -a file.txt              # Append to file

# Named pipes (FIFOs)
mkfifo mypipe
command1 > mypipe &
command2 < mypipe
```

### Environment Variables

```bash
# Setting variables
export PATH="$PATH:/new/path"
export EDITOR=vim
export BROWSER=firefox

# Viewing variables
env                        # All environment variables
printenv                   # All environment variables
echo $PATH                 # Specific variable
set                       # All variables (including local)

# Special variables
$HOME                     # Home directory
$USER                     # Username
$PWD                      # Current directory
$OLDPWD                   # Previous directory
$RANDOM                   # Random number
$$                        # Process ID
$?                        # Exit status of last command
```

### Aliases and Functions

```bash
# Creating aliases
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'

# Persistent aliases (add to ~/.bashrc or ~/.bash_profile)
echo "alias ll='ls -la'" >> ~/.bashrc

# Viewing aliases
alias                     # List all aliases
type alias_name          # Show alias definition

# Removing aliases
unalias alias_name
```

### Command Substitution

```bash
# Using backticks (old style)
current_date=`date`

# Using $() (preferred)
current_date=$(date)
file_count=$(ls | wc -l)
kernel_version=$(uname -r)

# Usage in commands
echo "Today is $(date)"
cp file.txt file.txt.$(date +%Y%m%d)
```

### Job Control

```bash
# Background processes
command &                 # Run in background
nohup command &           # Run immune to hangups

# Job management
jobs                      # List active jobs
bg %1                     # Resume job 1 in background
fg %1                     # Bring job 1 to foreground
kill %1                   # Kill job 1
disown %1                 # Remove job from shell's job table

# Process substitution
diff <(command1) <(command2)    # Compare outputs
command < <(other_command)      # Use command output as input
```

## Secure Shell Usage (SSH)

### Basic SSH Connection

```bash
# Basic SSH login
ssh username@hostname
ssh username@ip_address
ssh -p 2222 username@hostname     # Custom port

# SSH with specific options
ssh -v username@hostname          # Verbose output
ssh -X username@hostname          # X11 forwarding
ssh -L local_port:remote_host:remote_port username@hostname  # Local forwarding
```

### SSH Key Authentication

> [!tip] Key-based authentication is much more secure than password authentication

```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
ssh-keygen -t ed25519 -C "your_email@example.com"     # Preferred modern algorithm

# Key generation with passphrase
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_work -C "work_email@company.com"

# Copy public key to remote server
ssh-copy-id username@hostname
ssh-copy-id -i ~/.ssh/id_ed25519.pub username@hostname

# Manual key copy
cat ~/.ssh/id_ed25519.pub | ssh username@hostname "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### SSH Key Permissions

> [!warning] Critical Security SSH keys must have correct permissions or SSH will refuse to use them.

```bash
# Set correct permissions
chmod 700 ~/.ssh                    # SSH directory
chmod 600 ~/.ssh/id_ed25519         # Private key
chmod 644 ~/.ssh/id_ed25519.pub     # Public key
chmod 644 ~/.ssh/authorized_keys    # Authorized keys
chmod 600 ~/.ssh/config             # SSH config

# Verify permissions
ls -la ~/.ssh/
```

### SSH Config File

Create `~/.ssh/config` for connection shortcuts:

```bash
# ~/.ssh/config
Host myserver
    HostName server.example.com
    User myusername
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_work
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host jumpbox
    HostName jump.example.com
    User admin
    IdentityFile ~/.ssh/id_rsa

Host internal
    HostName internal.company.com
    User developer
    ProxyJump jumpbox
    IdentityFile ~/.ssh/id_ed25519

# Wildcards and defaults
Host *.company.com
    User myusername
    IdentityFile ~/.ssh/id_company

Host *
    AddKeysToAgent yes
    UseKeychain yes
    IdentitiesOnly yes
```

Usage with config:

```bash
ssh myserver                # Uses configuration from ~/.ssh/config
ssh internal               # Connects through jumpbox automatically
```

### File Transfer with SSH

```bash
# SCP (Secure Copy)
scp file.txt username@hostname:/remote/path/
scp -r directory/ username@hostname:/remote/path/
scp username@hostname:/remote/file.txt ./local/path/
scp -P 2222 file.txt username@hostname:/path/    # Custom port

# SFTP (SSH File Transfer Protocol)
sftp username@hostname
# SFTP commands:
# put localfile remotefile    - Upload file
# get remotefile localfile    - Download file
# ls                          - List remote directory
# lls                         - List local directory
# cd                          - Change remote directory
# lcd                         - Change local directory
# mkdir                       - Create remote directory
# rmdir                       - Remove remote directory
# exit                        - Exit SFTP

# RSYNC over SSH (efficient synchronization)
rsync -avz -e ssh local_directory/ username@hostname:/remote/path/
rsync -avz -e ssh username@hostname:/remote/path/ ./local_directory/
rsync -avz --delete -e ssh source/ destination/    # Delete files not in source
```

### SSH Tunneling and Port Forwarding

```bash
# Local port forwarding (access remote service locally)
ssh -L local_port:target_host:target_port username@ssh_server
ssh -L 8080:localhost:80 username@webserver       # Access remote web server locally
ssh -L 3306:database.internal:3306 username@jumpbox  # Access internal database

# Remote port forwarding (expose local service remotely)
ssh -R remote_port:localhost:local_port username@ssh_server
ssh -R 8080:localhost:3000 username@remote_server  # Expose local app on remote server

# Dynamic port forwarding (SOCKS proxy)
ssh -D local_port username@ssh_server
ssh -D 1080 username@proxy_server                  # Create SOCKS proxy on port 1080

# Persistent tunnels
autossh -M 20000 -L 8080:localhost:80 username@hostname  # Auto-restart tunnel
```

### SSH Agent and Key Management

```bash
# SSH Agent
ssh-agent bash            # Start SSH agent
eval $(ssh-agent)         # Start SSH agent in current shell
ssh-add                   # Add default keys to agent
ssh-add ~/.ssh/id_ed25519 # Add specific key to agent
ssh-add -l                # List keys in agent
ssh-add -d ~/.ssh/id_ed25519  # Remove key from agent
ssh-add -D                # Remove all keys from agent

# Key forwarding
ssh -A username@hostname  # Forward SSH agent
```

### Advanced SSH Security

```bash
# SSH hardening options
ssh -o StrictHostKeyChecking=yes username@hostname
ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no username@hostname  # Skip host key checking (insecure)
ssh -o ConnectTimeout=10 username@hostname
ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 username@hostname

# SSH escape sequences (during active SSH session)
~.              # Disconnect
~^Z             # Background SSH
~#              # List forwarded connections
~?              # Help
```

## Best Practices for Security

### User Account Security

> [!warning] Root Access Avoid using root account for daily tasks. Use sudo instead.

```bash
# Sudo usage
sudo command              # Run single command as root
sudo -u username command  # Run command as specific user
sudo -i                   # Interactive root shell
sudo su - username        # Switch to user account

# Sudo configuration
sudo visudo              # Edit sudoers file safely
```

### File System Security

```bash
# Secure file permissions
chmod 600 ~/.ssh/id_*         # SSH private keys
chmod 644 ~/.ssh/id_*.pub     # SSH public keys  
chmod 700 ~/.ssh              # SSH directory
chmod 600 ~/.bashrc           # Shell configuration
chmod 600 ~/.bash_history     # Command history

# Find security issues
find / -perm -4000 2>/dev/null    # Find SUID files
find / -perm -2000 2>/dev/null    # Find SGID files
find / -perm -1000 2>/dev/null    # Find sticky bit files
find /home -perm 777 2>/dev/null  # Find world-writable files
```

### Network Security

```bash
# Secure SSH configuration (server-side /etc/ssh/sshd_config)
# Port 2222                          # Change default port
# PermitRootLogin no                  # Disable root login
# PasswordAuthentication no           # Disable password auth
# PubkeyAuthentication yes            # Enable key auth
# AllowUsers user1 user2              # Limit users
# MaxAuthTries 3                      # Limit login attempts

# Client-side security
ssh -o StrictHostKeyChecking=yes username@hostname
ssh -o UserKnownHostsFile=~/.ssh/known_hosts username@hostname
```

### System Monitoring

```bash
# Security monitoring
sudo tail -f /var/log/auth.log        # Authentication logs
sudo tail -f /var/log/secure          # Security logs (RHEL/CentOS)
who                                   # Currently logged in users
last                                  # Login history
lastb                                 # Failed login attempts
w                                     # Detailed user activity

# Process monitoring
ps aux | grep suspicious_process
lsof -i                              # Network connections
netstat -tulpn                       # Listening services
```

### Backup and Recovery

```bash
# System backup
tar -czf backup-$(date +%Y%m%d).tar.gz /etc /home
rsync -avz /important/data/ /backup/location/

# Database backup (if applicable)
mysqldump -u root -p database_name > backup.sql
pg_dump database_name > backup.sql

# Automated backup script
#!/bin/bash
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "$BACKUP_DIR/system_backup_$DATE.tar.gz" /etc /home --exclude=/home/*/tmp
find "$BACKUP_DIR" -name "system_backup_*.tar.gz" -mtime +7 -delete
```

## Troubleshooting and Debugging

### Common Issues and Solutions

```bash
# Permission denied errors
ls -la filename                      # Check permissions
sudo chmod +x filename               # Make executable
sudo chown $USER:$USER filename      # Change ownership

# Command not found
which command_name                   # Check if command exists
echo $PATH                          # Check PATH variable
sudo apt update && sudo apt install package  # Install missing package (Debian/Ubuntu)
sudo yum install package            # Install package (RHEL/CentOS)

# SSH connection issues
ssh -v username@hostname             # Verbose SSH output
ssh-keygen -R hostname               # Remove host from known_hosts
ping hostname                        # Test connectivity
telnet hostname 22                   # Test SSH port
```

### System Information Commands

```bash
# Hardware information
lscpu                   # CPU information
lsmem                   # Memory information
lsblk                   # Block devices
lspci                   # PCI devices
lsusb                   # USB devices
dmidecode               # Hardware details (requires root)

# System status
systemctl status service_name        # Service status (systemd)
service service_name status          # Service status (SysV)
journalctl -u service_name           # Service logs (systemd)
dmesg                               # Kernel messages
uptime                              # System uptime and load
```

### Log Analysis

```bash
# Common log locations
/var/log/messages       # General system messages
/var/log/syslog         # System log (Debian/Ubuntu)
/var/log/auth.log       # Authentication log
/var/log/kern.log       # Kernel log
/var/log/cron.log       # Cron job log

# Log analysis commands
tail -f /var/log/syslog             # Follow log in real-time
grep "ERROR" /var/log/messages      # Search for errors
awk '/error/ {print}' /var/log/app.log  # Extract error lines
journalctl --since "1 hour ago"     # Recent systemd logs
```

> [!note] Learning Path
> 
> 1. Master basic commands and file operations
> 2. Learn text processing and search tools
> 3. Practice scripting and automation
> 4. Study SSH and security practices
> 5. Explore advanced topics like system administration

---

**Related Notes:** [[File System]], [[Regex]], [[Bash Scripting]], [[Networking Basics]], [[SSH]], [[Security Best Practices]], [[System Administration]], [[Linux Commands Reference]]

#shell #bash #linux #commands #obsidian #scripting #ssh #security #unix #terminal #cli #sysadmin