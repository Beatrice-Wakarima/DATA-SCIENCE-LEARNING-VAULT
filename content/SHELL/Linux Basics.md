# Linux Basics

#Linux #CommandLine #Terminal #SystemAdministration #Unix #CLI

**Related:** [[Command Line Interface]] | [[File System]] | [[Shell Scripting]] | [[System Administration]] | [[Network Tools]]

---

## Overview

Linux is a powerful, open-source operating system kernel that forms the foundation of many distributions (distros). Understanding Linux basics is essential for developers, system administrators, and data professionals working with servers, cloud platforms, and development environments.

**Common Distributions:** Ubuntu, CentOS, Red Hat, Debian, Arch Linux, Fedora

---

## Module 1: Getting Started with Linux

### What is Linux?

Linux is a Unix-like operating system kernel originally created by Linus Torvalds in 1991. It's:

- **Open Source**: Free to use, modify, and distribute
- **Multi-user**: Multiple users can work simultaneously
- **Multi-tasking**: Can run multiple processes concurrently
- **Portable**: Runs on various hardware architectures
- **Secure**: Built-in security features and permissions

### Linux File System Hierarchy

```
/                    # Root directory
├── bin/            # Essential user binaries
├── boot/           # Boot loader files
├── dev/            # Device files
├── etc/            # System configuration files
├── home/           # User home directories
├── lib/            # Essential shared libraries
├── media/          # Removable media mount points
├── mnt/            # Temporary mount points
├── opt/            # Optional software packages
├── proc/           # Process information
├── root/           # Root user's home directory
├── sbin/           # System binaries
├── tmp/            # Temporary files
├── usr/            # User programs and data
└── var/            # Variable data files
```

### Basic Concepts

#### 1. Everything is a File

In Linux, everything is treated as a file:

- Regular files (documents, images, etc.)
- Directories (folders)
- Device files (hardware devices)
- Process files (running programs)

#### 2. Case Sensitivity

Linux is case-sensitive:

- `file.txt` and `File.txt` are different files
- `ls` and `LS` are different commands

#### 3. No File Extensions Required

File types are determined by content, not extensions:

- Extensions are for human convenience
- Use `file` command to check actual file type

### XP Tasks - Getting Started

- [ ] Identify your current Linux distribution with `cat /etc/os-release`
- [ ] Explore the root directory with `ls /`
- [ ] Check your current directory with `pwd`
- [ ] Navigate to your home directory with `cd ~`
- [ ] List hidden files with `ls -la`

---

## Module 2: Essential Commands

### Navigation Commands

#### Directory Operations

```bash
# Print working directory
pwd

# List directory contents
ls                    # Basic listing
ls -l                 # Long format with details
ls -la                # Include hidden files
ls -lh                # Human readable file sizes
ls -lt                # Sort by modification time

# Change directory
cd /path/to/directory # Go to specific directory
cd ~                  # Go to home directory
cd ..                 # Go to parent directory
cd -                  # Go to previous directory
cd                    # Go to home directory (same as cd ~)
```

#### Path Types

```bash
# Absolute paths (start from root)
cd /home/username/Documents

# Relative paths (from current location)
cd Documents/projects
cd ../Downloads
```

### File and Directory Operations

#### Creating Files and Directories

```bash
# Create empty file
touch filename.txt
touch file1.txt file2.txt file3.txt  # Multiple files

# Create directories
mkdir dirname
mkdir -p path/to/nested/directory    # Create parent directories
mkdir dir1 dir2 dir3                 # Multiple directories
```

#### Copying and Moving

```bash
# Copy files
cp source.txt destination.txt
cp file.txt /path/to/directory/
cp -r directory/ /path/to/destination/  # Copy directory recursively

# Move/rename files
mv oldname.txt newname.txt
mv file.txt /path/to/directory/
mv directory/ /new/location/
```

#### Removing Files and Directories

```bash
# Remove files
rm filename.txt
rm file1.txt file2.txt              # Multiple files
rm -i filename.txt                  # Interactive (ask for confirmation)

# Remove directories
rmdir empty_directory               # Remove empty directory
rm -r directory/                    # Remove directory and contents
rm -rf directory/                   # Force remove (be careful!)
```

### File Content Operations

#### Viewing File Contents

```bash
# Display entire file
cat filename.txt

# Display file with line numbers
cat -n filename.txt

# View file page by page
less filename.txt                   # Navigate with arrow keys, q to quit
more filename.txt                   # Similar to less

# Display first/last lines
head filename.txt                   # First 10 lines
head -n 5 filename.txt             # First 5 lines
tail filename.txt                   # Last 10 lines
tail -n 20 filename.txt            # Last 20 lines
tail -f filename.txt               # Follow file changes (useful for logs)
```

#### Searching in Files

```bash
# Search for text in files
grep "search_term" filename.txt
grep -i "search_term" filename.txt     # Case insensitive
grep -r "search_term" directory/       # Recursive search in directory
grep -n "search_term" filename.txt     # Show line numbers
grep -v "search_term" filename.txt     # Show lines NOT containing term
```

### XP Tasks - Essential Commands

- [ ] Create a directory called `linux_practice`
- [ ] Create three empty files: `file1.txt`, `file2.txt`, `file3.txt`
- [ ] Copy `file1.txt` to `backup.txt`
- [ ] Move `file2.txt` to a subdirectory
- [ ] Use `grep` to search for a word in a text file
- [ ] View the last 5 lines of `/etc/passwd`
- [ ] List all files in `/usr/bin` with details

---

## Module 3: File Permissions and Ownership

### Understanding File Permissions

#### Permission Types

- **r (read)**: View file contents or list directory contents
- **w (write)**: Modify file contents or create/delete files in directory
- **x (execute)**: Run file as program or enter directory

#### Permission Groups

- **Owner**: The user who owns the file
- **Group**: Users who belong to the file's group
- **Other**: All other users

#### Reading Permission Display

```bash
ls -l filename.txt
# Output: -rw-r--r-- 1 user group 1234 Jan 15 10:30 filename.txt
#         |  |  |
#         |  |  └── Other permissions (r--)
#         |  └───── Group permissions (r--)
#         └──────── Owner permissions (rw-)
```

#### Permission Values

```bash
# Symbolic notation
r = 4, w = 2, x = 1

# Common combinations
7 = rwx (4+2+1)     # Read, write, execute
6 = rw- (4+2+0)     # Read, write
5 = r-x (4+0+1)     # Read, execute
4 = r-- (4+0+0)     # Read only
0 = --- (0+0+0)     # No permissions
```

### Changing Permissions

#### Using chmod (Change Mode)

```bash
# Numeric method
chmod 755 filename.txt              # rwxr-xr-x
chmod 644 filename.txt              # rw-r--r--
chmod 600 filename.txt              # rw-------

# Symbolic method
chmod u+x filename.txt              # Add execute for owner
chmod g-w filename.txt              # Remove write for group
chmod o+r filename.txt              # Add read for others
chmod a+x filename.txt              # Add execute for all

# Multiple changes
chmod u+x,g-w,o-r filename.txt
```

#### Using chown (Change Owner)

```bash
# Change owner
sudo chown newowner filename.txt

# Change owner and group
sudo chown newowner:newgroup filename.txt

# Change group only
sudo chgrp newgroup filename.txt

# Recursive change
sudo chown -R user:group directory/
```

### Special Permissions

#### Sticky Bit, SUID, SGID

```bash
# Sticky bit (typically on directories like /tmp)
chmod +t directory/                 # Only owner can delete files

# SUID (Set User ID)
chmod u+s program                   # Run with owner's privileges

# SGID (Set Group ID)
chmod g+s directory/                # New files inherit group
```

### XP Tasks - Permissions

- [ ] Check permissions of files in your home directory
- [ ] Create a file and make it executable with `chmod +x`
- [ ] Change a file's permissions to 644
- [ ] Create a script file and make it executable
- [ ] Use `ls -la` to see hidden file permissions
- [ ] Check the owner and group of `/etc/passwd`

---

## Module 4: Text Processing and I/O Redirection

### Input/Output Redirection

#### Standard Streams

- **stdin (0)**: Standard input (keyboard)
- **stdout (1)**: Standard output (screen)
- **stderr (2)**: Standard error (screen)

#### Redirection Operators

```bash
# Output redirection
command > file.txt                  # Redirect stdout to file (overwrite)
command >> file.txt                 # Append stdout to file
command 2> error.log               # Redirect stderr to file
command &> all.log                  # Redirect both stdout and stderr

# Input redirection
command < input.txt                 # Use file as input

# Pipes
command1 | command2                 # Send output of command1 to command2
command1 | command2 | command3      # Chain multiple commands
```

#### Practical Examples

```bash
# Save directory listing to file
ls -la > directory_contents.txt

# Append date to log file
date >> activity.log

# Search and save results
grep "error" /var/log/messages > errors.txt

# Count lines in multiple files
cat file1.txt file2.txt | wc -l

# Sort and remove duplicates
sort names.txt | uniq > unique_names.txt
```

### Text Processing Commands

#### Basic Text Tools

```bash
# Word, line, character count
wc filename.txt                     # Lines, words, characters
wc -l filename.txt                  # Lines only
wc -w filename.txt                  # Words only

# Sort lines
sort filename.txt                   # Alphabetical sort
sort -n numbers.txt                 # Numerical sort
sort -r filename.txt                # Reverse sort

# Remove duplicates
uniq filename.txt                   # Remove consecutive duplicates
sort filename.txt | uniq            # Remove all duplicates

# Cut columns
cut -d: -f1 /etc/passwd            # Extract first field (delimiter :)
cut -c1-5 filename.txt             # Extract characters 1-5
```

#### Advanced Text Processing

```bash
# Stream editor (sed)
sed 's/old/new/' filename.txt          # Replace first occurrence per line
sed 's/old/new/g' filename.txt         # Replace all occurrences
sed '1,5d' filename.txt                # Delete lines 1-5
sed -n '10,20p' filename.txt           # Print lines 10-20 only

# Text processing (awk)
awk '{print $1}' filename.txt          # Print first column
awk -F: '{print $1}' /etc/passwd       # Print first field (delimiter :)
awk 'NR>1{print $2}' data.txt          # Skip first line, print second column
```

#### Find and Locate

```bash
# Find files and directories
find /path -name "*.txt"               # Find all .txt files
find . -type f -size +1M                # Find files larger than 1MB
find /home -user username               # Find files owned by user
find . -mtime -7                        # Find files modified in last 7 days

# Quick file location
locate filename                         # Find file by name (uses database)
which command                           # Find location of command
whereis command                         # Find binary, source, manual
```

### XP Tasks - Text Processing

- [ ] Create a text file and redirect command output to it
- [ ] Use pipes to combine `ls`, `grep`, and `wc` commands
- [ ] Sort a file and save the result to a new file
- [ ] Use `cut` to extract specific columns from `/etc/passwd`
- [ ] Find all `.txt` files in your home directory
- [ ] Count the number of lines in a file using `wc -l`
- [ ] Use `sed` to replace a word in a file

---

## Module 5: Process Management

### Understanding Processes

#### Process Concepts

- **Process**: Running instance of a program
- **PID**: Process ID (unique identifier)
- **PPID**: Parent Process ID
- **Daemon**: Background process (system services)

#### Viewing Processes

```bash
# Display running processes
ps                                  # Processes for current user
ps aux                             # All processes with details
ps -ef                             # All processes, full format

# Real-time process monitor
top                                # Interactive process viewer
htop                               # Enhanced version (if installed)

# Process tree
pstree                             # Show process hierarchy
pstree username                    # Processes for specific user
```

#### Process Information

```bash
# Detailed process info
ps aux | head -1; ps aux | grep processname

# Process resource usage
top -p PID                         # Monitor specific process
pidstat -p PID 1                   # CPU usage statistics (if available)
```

### Managing Processes

#### Starting and Stopping Processes

```bash
# Run in background
command &                          # Start process in background
nohup command &                    # Run immune to hangups

# Job control
jobs                               # List current jobs
fg %1                              # Bring job 1 to foreground
bg %1                              # Send job 1 to background
Ctrl+Z                             # Suspend current process
Ctrl+C                             # Terminate current process
```

#### Killing Processes

```bash
# Terminate processes
kill PID                           # Send TERM signal
kill -9 PID                        # Force kill (KILL signal)
kill -STOP PID                     # Stop process
kill -CONT PID                     # Continue stopped process

# Kill by name
killall processname                # Kill all processes by name
pkill -f "pattern"                 # Kill processes matching pattern
```

#### System Resource Monitoring

```bash
# Memory usage
free -h                            # Display memory usage
cat /proc/meminfo                  # Detailed memory info

# Disk usage
df -h                              # Disk space usage
du -h directory/                   # Directory space usage
du -sh *                           # Size of each item in current directory

# CPU information
cat /proc/cpuinfo                  # CPU details
lscpu                              # CPU architecture info
uptime                             # System uptime and load
```

### XP Tasks - Process Management

- [ ] View all running processes with `ps aux`
- [ ] Start a process in background using `&`
- [ ] Use `top` to monitor system processes
- [ ] Find and kill a specific process by PID
- [ ] Check system memory usage with `free -h`
- [ ] Monitor disk usage with `df -h`
- [ ] Use `jobs` to see background processes

---

## Module 6: Environment and Variables

### Environment Variables

#### Common Environment Variables

```bash
# Display environment variables
env                                # All environment variables
printenv                           # Same as env
echo $VARIABLE_NAME               # Display specific variable

# Important variables
echo $HOME                         # User's home directory
echo $PATH                         # Command search path
echo $USER                         # Current username
echo $SHELL                        # Current shell
echo $PWD                          # Present working directory
echo $LANG                         # Language/locale setting
```

#### Setting Variables

```bash
# Local variables (current session only)
VARIABLE_NAME="value"
export VARIABLE_NAME="value"       # Make it available to child processes

# Permanent variables (add to ~/.bashrc or ~/.profile)
echo 'export MY_VAR="my_value"' >> ~/.bashrc
source ~/.bashrc                   # Reload configuration

# System-wide variables (add to /etc/environment)
sudo echo 'MY_VAR="my_value"' >> /etc/environment
```

#### PATH Variable

```bash
# View current PATH
echo $PATH

# Add directory to PATH temporarily
export PATH=$PATH:/new/directory

# Add to PATH permanently (in ~/.bashrc)
echo 'export PATH=$PATH:/new/directory' >> ~/.bashrc
```

### Shell Configuration

#### Configuration Files

```bash
# User-specific files
~/.bashrc                          # Non-login shell settings
~/.bash_profile                    # Login shell settings
~/.profile                         # General profile (works with any shell)

# System-wide files
/etc/bashrc                        # System-wide bashrc
/etc/profile                       # System-wide profile
/etc/environment                   # Environment variables
```

#### Customizing Your Shell

```bash
# Aliases (shortcuts)
alias ll='ls -la'
alias la='ls -la'
alias ..='cd ..'
alias grep='grep --color=auto'

# Add aliases permanently
echo "alias ll='ls -la'" >> ~/.bashrc

# Functions
myfunc() {
    echo "Hello $1"
}

# Command history
history                            # Show command history
!number                            # Run command by history number
!!                                 # Repeat last command
!string                            # Run last command starting with string
```

### XP Tasks - Environment

- [ ] Display all environment variables with `env`
- [ ] Check your current PATH variable
- [ ] Create a temporary variable and export it
- [ ] Add a permanent alias to your `.bashrc`
- [ ] View your command history
- [ ] Create a simple shell function
- [ ] Add a directory to your PATH

---

## Module 7: Network and System Information

### Network Commands

#### Basic Network Information

```bash
# Network interface information
ip addr show                       # Show all network interfaces
ip route show                      # Show routing table
ifconfig                           # Network interface configuration (deprecated)

# Network connectivity
ping hostname                      # Test connectivity
ping -c 4 google.com              # Ping 4 times
traceroute hostname                # Show route to destination
nslookup hostname                  # DNS lookup
dig hostname                       # DNS lookup (more detailed)
```

#### Network Services

```bash
# Port and connection information
netstat -tuln                      # Show listening ports
ss -tuln                          # Modern alternative to netstat
lsof -i :80                       # Show what's using port 80

# Download files
wget URL                          # Download file from URL
curl URL                          # Transfer data from/to server
```

### System Information

#### Hardware and System Details

```bash
# System information
uname -a                          # System information
hostname                          # System hostname
whoami                            # Current username
id                                # User and group IDs
w                                 # Who is logged in
last                              # Last login information

# Hardware information
lscpu                             # CPU information
lsmem                             # Memory information
lsblk                             # Block devices (disks)
lsusb                             # USB devices
lspci                             # PCI devices
dmidecode                         # Hardware details (requires root)
```

#### System Resources

```bash
# Resource usage
uptime                            # System uptime and load
vmstat                            # Virtual memory statistics
iostat                            # I/O statistics
sar                               # System activity reporter

# Log files
tail -f /var/log/messages         # System messages
tail -f /var/log/syslog          # System log (Ubuntu/Debian)
journalctl -f                     # Systemd journal (modern systems)
```

### Package Management

#### Debian/Ubuntu (APT)

```bash
# Update package list
sudo apt update

# Upgrade packages
sudo apt upgrade

# Install packages
sudo apt install package_name

# Remove packages
sudo apt remove package_name
sudo apt autoremove               # Remove unused dependencies

# Search packages
apt search keyword
apt list --installed              # List installed packages
```

#### Red Hat/CentOS (YUM/DNF)

```bash
# Update system
sudo yum update                   # CentOS 7 and earlier
sudo dnf update                   # CentOS 8+ and Fedora

# Install packages
sudo yum install package_name
sudo dnf install package_name

# Remove packages
sudo yum remove package_name
sudo dnf remove package_name

# Search packages
yum search keyword
dnf search keyword
```

### XP Tasks - Network & System

- [ ] Check your network interfaces with `ip addr show`
- [ ] Test connectivity to google.com with `ping`
- [ ] Check system information with `uname -a`
- [ ] View system uptime and load
- [ ] Update package list (using appropriate package manager)
- [ ] Check who is currently logged in with `w`
- [ ] View system logs with `tail -f /var/log/messages`

---

## Module 8: Archives and Compression

### Working with Archives

#### tar (Tape Archive)

```bash
# Create archives
tar -cvf archive.tar files/        # Create tar archive
tar -czvf archive.tar.gz files/    # Create compressed tar.gz
tar -cjvf archive.tar.bz2 files/   # Create compressed tar.bz2

# Extract archives
tar -xvf archive.tar               # Extract tar archive
tar -xzvf archive.tar.gz           # Extract tar.gz
tar -xjvf archive.tar.bz2          # Extract tar.bz2

# List archive contents
tar -tvf archive.tar               # List contents without extracting

# Common tar options:
# c = create, x = extract, t = list
# v = verbose, f = file, z = gzip, j = bzip2
```

#### zip/unzip

```bash
# Create zip archives
zip archive.zip file1 file2        # Create zip with specific files
zip -r archive.zip directory/      # Create zip recursively

# Extract zip archives
unzip archive.zip                  # Extract all files
unzip archive.zip -d /path/        # Extract to specific directory
unzip -l archive.zip               # List contents without extracting
```

#### Other Compression Tools

```bash
# gzip/gunzip
gzip file.txt                      # Compress file (creates file.txt.gz)
gunzip file.txt.gz                 # Decompress file

# bzip2/bunzip2
bzip2 file.txt                     # Compress with bzip2
bunzip2 file.txt.bz2               # Decompress bzip2

# xz
xz file.txt                        # Compress with xz
unxz file.txt.xz                   # Decompress xz
```

### File Transfer

#### Secure Copy (scp)

```bash
# Copy files to remote server
scp file.txt user@server:/path/

# Copy files from remote server
scp user@server:/path/file.txt ./

# Copy directories recursively
scp -r directory/ user@server:/path/
```

#### rsync (Synchronization)

```bash
# Synchronize directories
rsync -av source/ destination/     # Archive mode, verbose
rsync -av --delete source/ dest/   # Delete files not in source
rsync -av source/ user@server:dest/ # Remote sync
```

### XP Tasks - Archives

- [ ] Create a tar.gz archive of a directory
- [ ] Extract a tar archive and list its contents first
- [ ] Create a zip file with multiple files
- [ ] Compress a file with gzip and decompress it
- [ ] Use rsync to synchronize two directories
- [ ] Practice creating different types of compressed archives

---

## Module 9: System Services and Scheduling

### Service Management

#### systemd (Modern Linux Systems)

```bash
# Service status
sudo systemctl status service_name

# Start/stop/restart services
sudo systemctl start service_name
sudo systemctl stop service_name
sudo systemctl restart service_name
sudo systemctl reload service_name

# Enable/disable services (auto-start)
sudo systemctl enable service_name
sudo systemctl disable service_name

# List services
systemctl list-units --type=service
systemctl list-units --type=service --state=active
```

#### Traditional SysV (Older Systems)

```bash
# Service control
sudo service service_name start
sudo service service_name stop
sudo service service_name restart
sudo service service_name status

# Run levels
sudo chkconfig service_name on     # Enable service
sudo chkconfig service_name off    # Disable service
```

### Task Scheduling

#### cron (Scheduled Tasks)

```bash
# Edit user's crontab
crontab -e

# List current crontab
crontab -l

# Remove crontab
crontab -r

# System-wide cron
sudo vim /etc/crontab
```

#### Cron Syntax

```bash
# Cron format: minute hour day month day_of_week command
# Examples:
0 2 * * *       /path/to/script.sh     # Daily at 2 AM
30 14 * * 1     /path/to/script.sh     # Every Monday at 2:30 PM
0 0 1 * *       /path/to/script.sh     # First day of every month
*/15 * * * *    /path/to/script.sh     # Every 15 minutes
0 9-17 * * 1-5  /path/to/script.sh     # Every hour 9-5, Mon-Fri
```

#### at (One-time Tasks)

```bash
# Schedule one-time task
at 15:30                           # Run at 3:30 PM today
at 2pm tomorrow                    # Run at 2 PM tomorrow
at now + 5 minutes                 # Run in 5 minutes

# List scheduled tasks
atq

# Remove scheduled task
atrm job_number
```

### XP Tasks - Services & Scheduling

- [ ] Check the status of ssh service
- [ ] Create a simple cron job to run every 5 minutes
- [ ] List all active services on your system
- [ ] Schedule a one-time task with `at`
- [ ] Enable/disable a service for automatic startup
- [ ] View system logs for a specific service

---

## Module 10: Security Basics

### User and Group Management

#### User Operations

```bash
# Add user
sudo useradd username
sudo useradd -m username           # Create home directory
sudo useradd -s /bin/bash username # Specify shell

# Set password
sudo passwd username

# Modify user
sudo usermod -aG groupname username # Add user to group
sudo usermod -s /bin/zsh username  # Change shell

# Delete user
sudo userdel username              # Keep home directory
sudo userdel -r username           # Remove home directory
```

#### Group Operations

```bash
# Add group
sudo groupadd groupname

# Add user to group
sudo usermod -aG groupname username
sudo gpasswd -a username groupname

# Remove user from group
sudo gpasswd -d username groupname

# Delete group
sudo groupdel groupname

# View user's groups
groups username
id username
```

### File Security

#### Access Control Lists (ACLs)

```bash
# View ACLs
getfacl filename

# Set ACLs
setfacl -m u:username:rw filename  # Give user read/write
setfacl -m g:groupname:r filename  # Give group read access
setfacl -x u:username filename     # Remove user's ACL

# Default ACLs for directories
setfacl -d -m u:username:rw directory/
```

#### File Attributes

```bash
# View file attributes
lsattr filename

# Set file attributes
chattr +i filename                 # Make file immutable
chattr -i filename                 # Remove immutable attribute
chattr +a filename                 # Append only
```

### System Security

#### sudo Configuration

```bash
# Edit sudo configuration
sudo visudo

# Grant sudo access to user
username ALL=(ALL:ALL) ALL

# Allow user to run specific commands
username ALL=(ALL) /bin/systemctl restart apache2
```

#### SSH Security

```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096

# Copy public key to server
ssh-copy-id user@server

# SSH with key authentication
ssh -i ~/.ssh/private_key user@server

# SSH configuration
vim ~/.ssh/config
```

#### Firewall (ufw - Ubuntu)

```bash
# Enable firewall
sudo ufw enable

# Allow ports
sudo ufw allow 22                  # SSH
sudo ufw allow 80                  # HTTP
sudo ufw allow 443                 # HTTPS

# Deny access
sudo ufw deny 23                   # Telnet

# List rules
sudo ufw status
sudo ufw status verbose
```

### XP Tasks - Security

- [ ] Create a new user with home directory
- [ ] Add user to a specific group
- [ ] Set up SSH key authentication
- [ ] Configure sudo access for a user
- [ ] Use ACLs to grant specific file permissions
- [ ] Enable and configure basic firewall rules
- [ ] Practice changing file ownership and permissions

---

## Quick Reference Cheat Sheet

### Essential Commands

```bash
# Navigation
pwd, ls, cd, mkdir, rmdir

# File Operations
cp, mv, rm, touch, find, locate

# File Content
cat, less, head, tail, grep, wc

# Permissions
chmod, chown, chgrp

# Processes
ps, top, kill, jobs, bg, fg

# Archives
tar, zip, unzip, gzip

# Network
ping, wget, curl, ssh, scp

# System Info
df, free, uptime, uname
```

### File Permission Quick Reference

```bash
# Numeric permissions
755 = rwxr-xr-x    # Directories, executables
644 = rw-r--r--    # Regular files
600 = rw-------    # Private files
```

### Common File Locations

```bash
/etc/passwd        # User accounts
/etc/group         # Groups
/etc/hosts         # Host name resolution
/var/log/          # Log files
/tmp/              # Temporary files
~/.bashrc          # User shell configuration
```

---

## Troubleshooting Common Issues

### Permission Denied

```bash
# Check file permissions
ls -la filename

# Fix common permission issues
chmod +x script.sh             # Make script executable
sudo chown user:group file     # Fix ownership
```

### Command Not Found

```bash
# Check if command exists
which command_name
whereis command_name

# Check PATH variable
echo $PATH

# Install missing package (Ubuntu)
sudo apt search command_name
sudo apt install package_name
```

### Disk Space Issues

```bash
# Check disk usage
df -h
du -sh /*

# Find large files
find / -size +100M -type f 2>/dev/null

# Clean up
sudo apt autoremove
sudo apt autoclean
```

### Process Issues

```bash
# Find resource-heavy processes
top
ps aux --sort=-%cpu | head
ps aux --sort=-%mem | head

# Kill unresponsive processes
kill -9 PID
killall process_name
```

---

## Advanced Topics to Explore

- [[Shell Scripting]] - Automating tasks with bash scripts
- [[System Administration]] - Advanced system management
- [[Network Configuration]] - Network setup and troubleshooting
- [[Log Analysis]] - System and application log management
- [[Performance Monitoring]] - System performance tuning
- [[Container Technology]] - Docker and container management
- [[Security Hardening]] - Advanced security configurations

---

## Final XP Challenge

### Linux Mastery Project

Create a comprehensive system monitoring and maintenance script that demonstrates your Linux skills:

**Requirements:**

- [ ] System information gathering
- [ ] Automated log rotation and cleanup
- [ ] User account management functions
- [ ] Disk space monitoring and alerting
- [ ] Service status checking
- [ ] Security audit features
- [ ] Scheduled execution via cron
- [ ] Error handling and logging

This project should integrate multiple Linux concepts and serve as a practical tool for system administration.

---

**Tags:** #Linux #CommandLine #Terminal #SystemAdministration #Unix #CLI #FileSystem #Permissions #ProcessManagement