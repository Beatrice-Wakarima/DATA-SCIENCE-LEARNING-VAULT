# Command Line Interface (CLI)

#CLI #Terminal #CommandLine #Shell #Bash #PowerShell #Windows #Linux #macOS

**Related:** [[Linux Basics]] | [[Shell Scripting]] | [[Terminal Emulators]] | [[System Administration]] | [[Development Tools]]

---

## Overview

The Command Line Interface (CLI) is a text-based interface for interacting with computer systems. Unlike graphical user interfaces (GUIs), CLIs allow users to execute commands by typing text instructions, providing powerful automation capabilities and direct system control.

**Benefits of CLI:**

- **Speed**: Faster than GUI for many operations
- **Automation**: Easy to script and automate tasks
- **Precision**: Exact control over system operations
- **Remote Access**: Works over network connections
- **Resource Efficient**: Lower system resource usage
- **Consistency**: Same interface across different systems

---

## Module 1: CLI Fundamentals

### What is a Command Line Interface?

A CLI is a text-based user interface that allows users to interact with the operating system or applications by typing commands. It consists of:

- **Terminal**: The application that provides the CLI environment
- **Shell**: The command interpreter that processes commands
- **Prompt**: The text that indicates the system is ready for input
- **Commands**: Instructions given to the system
- **Arguments**: Parameters passed to commands
- **Options/Flags**: Modifiers that change command behavior

### Anatomy of a Command

```bash
command [options] [arguments]
```

**Examples:**

```bash
ls -la /home/user          # command: ls, option: -la, argument: /home/user
cp -r source/ destination/ # command: cp, option: -r, arguments: source/, destination/
grep -i "text" file.txt    # command: grep, option: -i, arguments: "text", file.txt
```

### CLI vs GUI Comparison

|Aspect|CLI|GUI|
|---|---|---|
|**Learning Curve**|Steeper initially|More intuitive|
|**Speed (Expert)**|Very fast|Moderate|
|**Automation**|Excellent|Limited|
|**Precision**|Exact control|Point-and-click approximation|
|**Resource Usage**|Minimal|Higher|
|**Remote Access**|Perfect|Requires special tools|
|**Discoverability**|Requires knowledge|Visual exploration|

### XP Tasks - Fundamentals

- [ ] Open a terminal/command prompt on your system
- [ ] Identify your current shell (echo $SHELL on Unix, echo $0 on Windows)
- [ ] Practice typing basic commands without executing them
- [ ] Understand the difference between terminal, shell, and CLI
- [ ] Explore your system's command prompt appearance

---

## Module 2: Cross-Platform CLI Basics

### Windows Command Line

#### Command Prompt (cmd)

```cmd
# Basic navigation
dir                        # List directory contents
cd directory_name          # Change directory
cd ..                      # Go to parent directory
cd \                       # Go to root directory
mkdir new_folder           # Create directory
rmdir folder_name          # Remove empty directory

# File operations
copy file1.txt file2.txt   # Copy file
move file1.txt newname.txt # Move/rename file
del filename.txt           # Delete file
type filename.txt          # Display file contents

# System information
systeminfo                 # System information
tasklist                   # Running processes
ipconfig                   # Network configuration
```

#### PowerShell

```powershell
# Navigation (similar to Unix)
Get-ChildItem              # List directory (alias: ls, dir)
Set-Location directory     # Change directory (alias: cd)
New-Item -ItemType Directory -Name "folder"  # Create directory (alias: mkdir)

# File operations
Copy-Item file1.txt file2.txt              # Copy file (alias: cp)
Move-Item file1.txt newname.txt            # Move file (alias: mv)
Remove-Item filename.txt                   # Delete file (alias: rm)
Get-Content filename.txt                   # Display file contents (alias: cat)

# System information
Get-ComputerInfo           # System information
Get-Process                # Running processes (alias: ps)
Get-NetIPConfiguration     # Network configuration
```

### Unix-like Systems (Linux/macOS)

#### Bash Shell

```bash
# Basic navigation
ls                         # List directory contents
cd directory_name          # Change directory
cd ..                      # Go to parent directory
cd ~                       # Go to home directory
mkdir new_folder           # Create directory
rmdir folder_name          # Remove empty directory

# File operations
cp file1.txt file2.txt     # Copy file
mv file1.txt newname.txt   # Move/rename file
rm filename.txt            # Delete file
cat filename.txt           # Display file contents

# System information
uname -a                   # System information
ps aux                     # Running processes
ifconfig                   # Network configuration (or ip addr)
```

### XP Tasks - Cross-Platform

- [ ] List files in current directory on your system
- [ ] Create a new directory using CLI
- [ ] Copy a file using command line
- [ ] Display system information using appropriate command
- [ ] Navigate between directories using relative and absolute paths

---

## Module 3: Command Structure and Syntax

### Command Components

#### 1. Command Name

The primary instruction to execute:

```bash
ls          # List command
grep        # Search command  
find        # File search command
```

#### 2. Options/Flags

Modify command behavior:

```bash
# Short options (single dash, single character)
ls -l       # Long listing format
ls -a       # Show all files (including hidden)
ls -h       # Human readable sizes

# Long options (double dash, full words)
ls --all    # Same as -a
ls --human-readable  # Same as -h

# Combined short options
ls -la      # Combine -l and -a
ls -lah     # Combine -l, -a, and -h
```

#### 3. Arguments

Data passed to commands:

```bash
ls /home            # Directory argument
cp file1.txt file2.txt  # Source and destination arguments
grep "text" file.txt    # Pattern and file arguments
```

#### 4. Special Characters

##### Wildcards

```bash
*           # Matches any characters
?           # Matches single character
[abc]       # Matches any character in brackets
[a-z]       # Matches any character in range

# Examples
ls *.txt           # All .txt files
ls file?.txt       # file1.txt, fileA.txt, etc.
ls [Dd]ocument*    # Documents, documents, Document1, etc.
```

##### Redirection and Pipes

```bash
>           # Redirect output to file (overwrite)
>>          # Redirect output to file (append)
<           # Redirect input from file
|           # Pipe output to next command
&&          # Execute next command if previous succeeds
||          # Execute next command if previous fails
;           # Execute commands sequentially
```

##### Quoting

```bash
'single'    # Literal string (no variable expansion)
"double"    # Allow variable expansion
`backtick`  # Command substitution (deprecated)
$(command)  # Command substitution (modern)
\           # Escape character

# Examples
echo 'Hello $USER'      # Outputs: Hello $USER
echo "Hello $USER"      # Outputs: Hello john
echo "Today is $(date)" # Outputs: Today is Mon Jan 15 10:30:00
```

### Command Types

#### 1. Built-in Commands

Commands integrated into the shell:

```bash
# Common built-ins
cd          # Change directory
echo        # Display text
pwd         # Print working directory
history     # Command history
alias       # Create command aliases
export      # Set environment variables
```

#### 2. External Commands

Separate programs called by the shell:

```bash
# Examples
ls          # List files
grep        # Search text
find        # Find files
wget        # Download files
git         # Version control
```

#### 3. Aliases

Custom shortcuts for commands:

```bash
# Create aliases
alias ll='ls -la'
alias la='ls -la'
alias ..='cd ..'
alias grep='grep --color=auto'

# View aliases
alias

# Remove alias
unalias ll
```

#### 4. Functions

Custom command-like procedures:

```bash
# Define function
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Use function
mkcd new_project
```

### XP Tasks - Command Structure

- [ ] Practice using short and long options with `ls` command
- [ ] Use wildcards to list specific file types
- [ ] Create and use a simple alias
- [ ] Practice command substitution with `$(date)`
- [ ] Combine commands using `&&` and `||`
- [ ] Use pipes to combine two commands

---

## Module 4: Navigation and File Operations

### Directory Navigation

#### Basic Navigation Commands

```bash
# Universal commands (work in most shells)
pwd                 # Print current directory
ls / dir           # List directory contents  
cd path            # Change directory

# Relative vs Absolute Paths
cd /home/user/Documents     # Absolute path
cd Documents               # Relative path from current location
cd ../Downloads            # Relative path using parent directory
cd ~                       # Home directory (Unix)
cd %USERPROFILE%          # Home directory (Windows cmd)
```

#### Navigation Shortcuts

```bash
# Unix/Linux/macOS
cd ~               # Home directory
cd -               # Previous directory
cd ..              # Parent directory
cd ../..           # Two levels up
cd /               # Root directory

# Windows
cd %USERPROFILE%   # User home directory
cd \               # Root of current drive
cd /d D:\          # Change to D: drive
```

#### Advanced Navigation

```bash
# Directory stack (pushd/popd)
pushd /path/to/dir     # Save current dir and change to new
popd                   # Return to saved directory
dirs                   # Show directory stack

# Recent directories (in some shells)
cd -               # Toggle between two most recent directories
```

### File and Directory Operations

#### Creating Files and Directories

```bash
# Create files
touch filename.txt         # Create empty file (Unix)
echo. > filename.txt       # Create empty file (Windows cmd)
New-Item -Type File name.txt  # Create file (PowerShell)

# Create directories
mkdir dirname              # Create directory
mkdir -p path/to/dir       # Create nested directories (Unix)
mkdir path\to\dir          # Create nested directories (Windows)
```

#### Copying Operations

```bash
# Copy files
cp source.txt dest.txt     # Copy file (Unix)
copy source.txt dest.txt   # Copy file (Windows cmd)
Copy-Item source.txt dest.txt  # Copy file (PowerShell)

# Copy directories
cp -r sourcedir/ destdir/  # Copy directory recursively (Unix)
xcopy sourcedir destdir /E # Copy directory (Windows cmd)
Copy-Item -Recurse source dest  # Copy directory (PowerShell)
```

#### Moving and Renaming

```bash
# Move/rename files
mv old.txt new.txt         # Rename/move (Unix)
move old.txt new.txt       # Rename/move (Windows cmd)
Move-Item old.txt new.txt  # Rename/move (PowerShell)

# Move to directory
mv file.txt /path/to/dir/  # Move to directory (Unix)
move file.txt C:\path\     # Move to directory (Windows)
```

#### Deleting Files and Directories

```bash
# Delete files
rm filename.txt            # Delete file (Unix)
del filename.txt           # Delete file (Windows cmd)
Remove-Item filename.txt   # Delete file (PowerShell)

# Delete directories
rmdir dirname              # Delete empty directory
rm -rf dirname             # Delete directory and contents (Unix)
rmdir /S dirname           # Delete directory and contents (Windows)
Remove-Item -Recurse dirname  # Delete directory (PowerShell)
```

### File Content Operations

#### Viewing File Contents

```bash
# Display entire file
cat filename.txt           # Unix
type filename.txt          # Windows cmd
Get-Content filename.txt   # PowerShell

# Page through file
less filename.txt          # Unix (q to quit)
more filename.txt          # Universal (space for next page)

# First/last lines
head -n 10 filename.txt    # First 10 lines (Unix)
tail -n 10 filename.txt    # Last 10 lines (Unix)
Get-Content file.txt -Head 10   # First 10 lines (PowerShell)
Get-Content file.txt -Tail 10   # Last 10 lines (PowerShell)
```

#### Searching in Files

```bash
# Search for text
grep "pattern" filename.txt    # Search in file (Unix)
findstr "pattern" filename.txt # Search in file (Windows)
Select-String "pattern" file.txt  # Search in file (PowerShell)

# Search with options
grep -i "pattern" file.txt     # Case insensitive
grep -n "pattern" file.txt     # Show line numbers
grep -r "pattern" directory/   # Recursive search
```

### XP Tasks - Navigation & Files

- [ ] Navigate to your home directory using appropriate command
- [ ] Create a nested directory structure (3 levels deep)
- [ ] Create a file and copy it to a different location
- [ ] Use wildcards to copy multiple files at once
- [ ] Search for a specific word in a text file
- [ ] Practice using both absolute and relative paths
- [ ] Delete a file and an empty directory

---

## Module 5: Input/Output and Redirection

### Standard Streams

Every process has three standard streams:

- **stdin (0)**: Standard input (keyboard)
- **stdout (1)**: Standard output (screen)
- **stderr (2)**: Standard error (screen)

### Output Redirection

#### Basic Redirection

```bash
# Redirect stdout to file
command > file.txt          # Overwrite file
command >> file.txt         # Append to file

# Examples
ls > directory_list.txt     # Save directory listing
date >> log.txt            # Append date to log
echo "Hello" > greeting.txt # Write text to file
```

#### Error Redirection

```bash
# Unix/Linux/macOS
command 2> error.log        # Redirect stderr to file
command 2>> error.log       # Append stderr to file
command > output.txt 2> error.log    # Separate stdout and stderr
command > output.txt 2>&1   # Redirect both to same file
command &> all_output.txt   # Redirect both (bash shorthand)

# Windows cmd
command > output.txt 2> error.log    # Separate streams
command > output.txt 2>&1   # Combine streams
```

#### Suppressing Output

```bash
# Discard output
command > /dev/null         # Discard stdout (Unix)
command 2> /dev/null        # Discard stderr (Unix)
command > /dev/null 2>&1    # Discard both (Unix)

command > nul               # Discard stdout (Windows)
command 2> nul              # Discard stderr (Windows)
```

### Input Redirection

#### Redirect Input from Files

```bash
# Use file as input
command < input.txt
sort < names.txt > sorted_names.txt

# Here documents (Unix)
command << EOF
Line 1
Line 2
EOF

# Here strings (Unix)
command <<< "input string"
```

### Pipes

#### Basic Piping

```bash
# Send output of one command to input of another
command1 | command2

# Examples
ls -la | grep ".txt"        # List files and filter for .txt
ps aux | grep "firefox"     # Show processes and filter
cat file.txt | wc -l        # Count lines in file
```

#### Complex Pipe Chains

```bash
# Multiple pipes
ls -la | grep ".txt" | wc -l    # Count .txt files
cat /etc/passwd | cut -d: -f1 | sort | uniq  # Get unique users

# Tee - output to both file and stdout
ls -la | tee listing.txt | grep ".txt"  # Save listing and filter
```

#### Platform-Specific Piping

```bash
# PowerShell object piping
Get-Process | Where-Object {$_.CPU -gt 100} | Sort-Object CPU

# Windows cmd piping
dir | findstr ".txt" | more
```

### Command Chaining

#### Sequential Execution

```bash
# Always execute next command
command1; command2; command3

# Execute if previous succeeds
command1 && command2 && command3

# Execute if previous fails
command1 || command2

# Mixed chaining
command1 && command2 || command3
```

#### Background Execution

```bash
# Run in background (Unix)
command &

# Multiple background commands
command1 & command2 & command3 &

# Background with output redirection
long_running_command > output.log 2>&1 &
```

### XP Tasks - I/O Redirection

- [ ] Redirect command output to a file
- [ ] Append command output to an existing file
- [ ] Use pipes to combine two commands
- [ ] Create a pipe chain with three commands
- [ ] Redirect both stdout and stderr to different files
- [ ] Use command chaining with && and ||
- [ ] Practice using input redirection with a file

---

## Module 6: Environment and Variables

### Environment Variables

#### Viewing Variables

```bash
# Unix/Linux/macOS
env                         # All environment variables
printenv                    # All environment variables
echo $VARIABLE_NAME         # Specific variable
echo $HOME                  # Home directory
echo $PATH                  # Command search path
echo $USER                  # Current user

# Windows cmd
set                         # All environment variables
echo %VARIABLE_NAME%        # Specific variable
echo %USERPROFILE%          # User profile directory
echo %PATH%                 # Command search path
echo %USERNAME%             # Current user

# PowerShell
Get-ChildItem Env:          # All environment variables
$env:VARIABLE_NAME          # Specific variable
$env:USERPROFILE            # User profile directory
$env:PATH                   # Command search path
$env:USERNAME               # Current user
```

#### Setting Variables

##### Temporary Variables (Session Only)

```bash
# Unix/Linux/macOS
VARIABLE_NAME="value"       # Local variable
export VARIABLE_NAME="value"  # Environment variable

# Windows cmd
set VARIABLE_NAME=value

# PowerShell
$env:VARIABLE_NAME="value"
```

##### Permanent Variables

```bash
# Unix/Linux - Add to shell configuration files
echo 'export MY_VAR="my_value"' >> ~/.bashrc
echo 'export MY_VAR="my_value"' >> ~/.bash_profile
echo 'export MY_VAR="my_value"' >> ~/.profile

# Windows - System Properties or registry
setx VARIABLE_NAME "value"  # User variable
setx VARIABLE_NAME "value" /M  # System variable (requires admin)

# PowerShell - Profile or system
Add-Content $PROFILE '$env:MY_VAR="my_value"'
```

### Important Environment Variables

#### Universal Variables

```bash
PATH            # Directories searched for commands
HOME / USERPROFILE  # User's home directory
USER / USERNAME     # Current username
TEMP / TMP          # Temporary directory
```

#### Unix-Specific Variables

```bash
SHELL           # Current shell program
PWD             # Present working directory
OLDPWD          # Previous working directory
LANG            # Locale/language settings
EDITOR          # Default text editor
BROWSER         # Default web browser
```

#### Windows-Specific Variables

```cmd
COMPUTERNAME    # Computer name
PROCESSOR_ARCHITECTURE  # CPU architecture
PROGRAMFILES    # Program Files directory
SYSTEMROOT      # Windows directory
WINDIR          # Windows directory
```

### PATH Variable

#### Understanding PATH

The PATH variable tells the system where to look for executable files:

```bash
# View current PATH
echo $PATH          # Unix
echo %PATH%         # Windows cmd
$env:PATH           # PowerShell
```

#### Modifying PATH

##### Temporary PATH Changes

```bash
# Unix/Linux/macOS
export PATH=$PATH:/new/directory
export PATH=/new/directory:$PATH    # Prepend

# Windows cmd
set PATH=%PATH%;C:\new\directory

# PowerShell
$env:PATH += ";C:\new\directory"
$env:PATH = "C:\new\directory;" + $env:PATH  # Prepend
```

##### Permanent PATH Changes

```bash
# Unix - Add to shell config
echo 'export PATH=$PATH:/new/directory' >> ~/.bashrc

# Windows - Use setx
setx PATH "%PATH%;C:\new\directory"

# Or use GUI: System Properties > Environment Variables
```

### Command History

#### Viewing History

```bash
# Unix/Linux/macOS
history                     # Show command history
history 10                  # Show last 10 commands
!number                     # Execute command by number
!!                         # Repeat last command
!string                    # Last command starting with string

# Windows cmd
doskey /history            # Show command history
F7                         # History popup (interactive)

# PowerShell
Get-History                # Show command history
Invoke-History 5           # Execute command by ID
r string                   # Last command starting with string
```

#### History Configuration

```bash
# Unix - Configure in ~/.bashrc
HISTSIZE=1000              # Commands in memory
HISTFILESIZE=2000          # Commands in history file
HISTCONTROL=ignoredups     # Ignore duplicate commands

# PowerShell - Configure in profile
Set-PSReadlineOption -MaximumHistoryCount 4000
```

### Aliases and Functions

#### Creating Aliases

```bash
# Unix/Linux/macOS
alias ll='ls -la'
alias la='ls -la'
alias ..='cd ..'
alias grep='grep --color=auto'

# Windows cmd (using doskey)
doskey ll=dir
doskey ..=cd ..

# PowerShell
Set-Alias ll Get-ChildItem
New-Alias grep Select-String
```

#### Creating Functions

```bash
# Bash function
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# PowerShell function
function mkcd($dir) {
    New-Item -ItemType Directory -Path $dir -Force
    Set-Location $dir
}
```

### XP Tasks - Environment

- [ ] View all environment variables on your system
- [ ] Check your current PATH variable
- [ ] Create a temporary environment variable
- [ ] Add a directory to your PATH temporarily
- [ ] View your command history
- [ ] Create and use a simple alias
- [ ] Write a basic function and use it

---

## Module 7: Process Management and Job Control

### Understanding Processes

#### What are Processes?

- **Process**: Running instance of a program
- **PID**: Process ID (unique identifier)
- **PPID**: Parent Process ID
- **Thread**: Lightweight process within a process
- **Daemon/Service**: Background process

#### Viewing Processes

##### Unix/Linux/macOS

```bash
# Basic process listing
ps                          # Current user's processes
ps aux                      # All processes with details
ps -ef                      # All processes, different format

# Real-time process monitoring
top                         # Interactive process viewer
htop                        # Enhanced version (if installed)

# Process tree
pstree                      # Show process hierarchy
ps auxf                     # Process tree format
```

##### Windows

```cmd
# Command Prompt
tasklist                    # List all processes
tasklist /svc              # Processes with services
tasklist /fi "imagename eq notepad.exe"  # Filter processes

# PowerShell
Get-Process                 # List all processes
Get-Process | Sort-Object CPU -Descending  # Sort by CPU usage
Get-Process notepad         # Specific process
```

### Starting and Managing Processes

#### Foreground vs Background

##### Foreground Processes

```bash
# Normal execution (blocks terminal)
command
long_running_script.sh
```

##### Background Processes

```bash
# Unix/Linux/macOS
command &                   # Start in background
nohup command &            # Background, immune to hangups
screen command             # Detachable session
tmux new-session -d command  # Terminal multiplexer

# Windows
start command              # Start in new window
start /B command           # Start in background (cmd)
Start-Process command      # PowerShell
```

### Job Control

#### Job Management (Unix/Linux/macOS)

```bash
# View jobs
jobs                        # List active jobs
jobs -l                     # List with PIDs

# Control jobs
Ctrl+Z                      # Suspend current job
bg                          # Send job to background
bg %1                       # Send job 1 to background
fg                          # Bring job to foreground
fg %1                       # Bring job 1 to foreground

# Job references
%1                          # Job number 1
%+                          # Current job
%-                          # Previous job
%%                          # Current job (same as %+)
```

#### Process Control

```bash
# Suspend and resume
kill -STOP PID             # Suspend process
kill -CONT PID             # Resume process

# Terminate processes
kill PID                   # Terminate gracefully (SIGTERM)
kill -9 PID                # Force terminate (SIGKILL)
kill -HUP PID              # Hangup signal (reload config)

# Kill by name
killall process_name       # Kill all processes by name
pkill -f pattern          # Kill processes matching pattern
```

### System Resources and Monitoring

#### Resource Usage

```bash
# Memory usage
free -h                    # Memory usage (Linux)
vm_stat                    # Memory statistics (macOS)

# Disk usage
df -h                      # Disk space usage
du -h directory/           # Directory space usage
du -sh *                   # Size of each item

# CPU and load
uptime                     # System uptime and load average
w                          # Who is logged in and system load
```

#### Process Monitoring

```bash
# Detailed process info
ps -p PID -o pid,ppid,cmd,%cpu,%mem  # Custom format
pgrep process_name         # Find PID by name
pidof process_name         # Find PID by name (Linux)

# Resource monitoring
top -p PID                 # Monitor specific process
iostat                     # I/O statistics
vmstat                     # Virtual memory statistics
```

#### Windows Resource Monitoring

```cmd
# Task Manager equivalents
tasklist /fi "memusage gt 100000"  # High memory processes
wmic process get name,processid,percentprocessortime

# PowerShell
Get-Process | Sort-Object WorkingSet -Descending
Get-Counter "\Processor(_Total)\% Processor Time"
```

### Service Management

#### Unix/Linux Services (systemd)

```bash
# Service status
systemctl status service_name
systemctl is-active service_name
systemctl is-enabled service_name

# Start/stop services
sudo systemctl start service_name
sudo systemctl stop service_name
sudo systemctl restart service_name
sudo systemctl reload service_name

# Enable/disable auto-start
sudo systemctl enable service_name
sudo systemctl disable service_name

# List services
systemctl list-units --type=service
systemctl list-units --type=service --state=running
```

#### Windows Services

```cmd
# Command Prompt
sc query                   # List services
sc query service_name      # Service status
net start service_name     # Start service
net stop service_name      # Stop service

# PowerShell
Get-Service                # List all services
Get-Service service_name   # Specific service
Start-Service service_name # Start service
Stop-Service service_name  # Stop service
Restart-Service service_name # Restart service
```

### XP Tasks - Process Management

- [ ] List all running processes on your system
- [ ] Start a long-running command in the background
- [ ] Use job control to suspend and resume a process
- [ ] Monitor system resource usage (CPU, memory)
- [ ] Find and kill a specific process by name
- [ ] Check the status of a system service
- [ ] Practice using process monitoring tools

---

## Module 8: Text Processing and Pattern Matching

### Basic Text Operations

#### Viewing and Manipulating Text

##### Universal Commands

```bash
# Display file contents
cat filename.txt           # Unix
type filename.txt          # Windows cmd
Get-Content filename.txt   # PowerShell

# Count lines, words, characters
wc filename.txt            # Unix (lines, words, chars)
wc -l filename.txt         # Lines only
Get-Content file.txt | Measure-Object -Line -Word -Character  # PowerShell
```

##### Sorting and Uniqueness

```bash
# Sort lines
sort filename.txt          # Unix
sort -n numbers.txt        # Numerical sort
sort -r filename.txt       # Reverse sort
Get-Content file.txt | Sort-Object  # PowerShell

# Remove duplicates
uniq filename.txt          # Unix (consecutive duplicates only)
sort filename.txt | uniq   # All duplicates
Get-Content file.txt | Sort-Object | Get-Unique  # PowerShell
```

##### Extracting Columns/Fields

```bash
# Cut specific columns
cut -d',' -f1,3 data.csv   # Extract columns 1 and 3 (comma delimiter)
cut -c1-10 filename.txt    # Extract characters 1-10
awk -F',' '{print $1,$3}' data.csv  # Using awk

# PowerShell
Import-Csv data.csv | Select-Object Column1,Column3
```

### Pattern Matching and Searching

#### grep (Unix/Linux/macOS)

```bash
# Basic searching
grep "pattern" filename.txt
grep -i "pattern" filename.txt     # Case insensitive
grep -n "pattern" filename.txt     # Show line numbers
grep -v "pattern" filename.txt     # Invert match (exclude pattern)

# Multiple files and directories
grep "pattern" *.txt               # Search in all .txt files
grep -r "pattern" directory/       # Recursive search
grep -l "pattern" *.txt            # Show only filenames with matches

# Regular expressions
grep "^start" filename.txt         # Lines starting with "start"
grep "end$" filename.txt           # Lines ending with "end"
grep "[0-9]" filename.txt          # Lines containing digits
grep "colou?r" filename.txt        # Color or colour
```

#### Windows Text Searching

```cmd
# Command Prompt
findstr "pattern" filename.txt
findstr /i "pattern" filename.txt  # Case insensitive
findstr /n "pattern" filename.txt  # Show line numbers
findstr /r "^start" filename.txt   # Regular expressions

# PowerShell
Select-String "pattern" filename.txt
Select-String -Pattern "pattern" -Path *.txt
Select-String -Pattern "pattern" -Path filename.txt -CaseSensitive
```

### Advanced Text Processing

#### sed (Stream Editor) - Unix

```bash
# Substitution
sed 's/old/new/' filename.txt          # Replace first occurrence per line
sed 's/old/new/g' filename.txt         # Replace all occurrences
sed 's/old/new/2' filename.txt         # Replace second occurrence per line

# Line operations
sed '1d' filename.txt                  # Delete first line
sed '1,5d' filename.txt                # Delete lines 1-5
sed -n '10,20p' filename.txt           # Print only lines 10-20

# Multiple operations
sed -e 's/old/new/g' -e 's/foo/bar/g' filename.txt
```

#### awk (Pattern Processing) - Unix

```bash
# Field processing
awk '{print $1}' filename.txt          # Print first field
awk '{print $1,$3}' filename.txt       # Print first and third fields
awk -F':' '{print $1}' /etc/passwd     # Custom delimiter

# Conditional processing
awk '$3 > 100 {print $1}' data.txt     # Print first field if third > 100
awk '/pattern/ {print $2}' filename.txt # Print second field of matching lines

# Calculations
awk '{sum += $1} END {print sum}' numbers.txt  # Sum first column
awk '{print NR, $0}' filename.txt      # Add line numbers
```

#### PowerShell Text Processing

```powershell
# String operations
"text".Replace("old", "new")
"text" -replace "old", "new"
"text" -match "pattern"

# File processing
Get-Content file.txt | ForEach-Object { $_ -replace "old", "new" }
Get-Content file.txt | Where-Object { $_ -like "*pattern*" }
Get-Content file.txt | Select-String "pattern"

# Advanced processing
Import-Csv data.csv | Where-Object {$_.Column1 -gt 100}
Get-Content file.txt | ForEach-Object { ($_ -split '\s+')[0] }  # First word
```

### Regular Expressions

#### Basic Regex Patterns

```bash
# Character classes
.           # Any single character
[abc]       # Any character in set
[a-z]       # Any lowercase letter
[A-Z]       # Any uppercase letter
[0-9]       # Any digit
\d          # Any digit (same as [0-9])
\w          # Word character (letters, digits, underscore)
\s          # Whitespace character

# Quantifiers
*           # Zero or more
+           # One or more
?           # Zero or one
{n}         # Exactly n times
{n,}        # n or more times
{n,m}       # Between n and m times

# Anchors
^           # Start of line
$           # End of line
\b          # Word boundary
```

#### Practical Regex Examples

```bash
# Email validation (basic)
grep -E "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# Phone number patterns
grep -E "\([0-9]{3}\) [0-9]{3}-[0-9]{4}"  # (123) 456-7890
grep -E "[0-9]{3}-[0-9]{3}-[0-9]{4}"      # 123-456-7890

# IP address
grep -E "([0-9]{1,3}\.){3}[0-9]{1,3}"

# Date patterns
grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}"      # YYYY-MM-DD
grep -E "[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}"  # MM/DD/YYYY
```

### XP Tasks - Text Processing

- [ ] Search for a pattern in a file using grep/findstr
- [ ] Use regular expressions to find email addresses in text
- [ ] Sort a file and remove duplicate lines
- [ ] Extract specific columns from a CSV file
- [ ] Replace all occurrences of a word in a file
- [ ] Count the number of lines containing a specific pattern
- [ ] Use awk or PowerShell to process structured data

---

## Module 9: Automation and Scripting

### Introduction to Shell Scripting

#### Why Automate with CLI?

- **Repetitive Tasks**: Automate routine operations
- **Consistency**: Same steps every time
- **Error Reduction**: Eliminate manual mistakes
- **Time Saving**: Execute complex workflows instantly
- **Scheduling**: Run tasks at specific times
- **Remote Execution**: Automate across multiple systems

### Basic Scripting Concepts

#### Script Structure

##### Bash Script (Unix/Linux/macOS)

```bash
#!/bin/bash
# This is a comment
# Script: my_script.sh

# Variables
name="John"
count=5

# Commands
echo "Hello, $name"
echo "Count is: $count"

# Make executable: chmod +x my_script.sh
# Run: ./my_script.sh
```

##### Batch Script (Windows cmd)

```batch
@echo off
REM This is a comment
REM Script: my_script.bat

REM Variables
set name=John
set count=5

REM Commands
echo Hello, %name%
echo Count is: %count%

REM Run: my_script.bat
```

##### PowerShell Script

```powershell
# This is a comment
# Script: my_script.ps1

# Variables
$name = "John"
$count = 5

# Commands
Write-Host "Hello, $name"
Write-Host "Count is: $count"

# Run: .\my_script.ps1
# May need: Set-ExecutionPolicy RemoteSigned
```

#### Variables and Data Types

##### Bash Variables

```bash
# String variables
name="John Doe"
path="/home/user"

# Numeric variables
count=10
price=19.99

# Arrays
fruits=("apple" "banana" "orange")
echo ${fruits[0]}      # First element
echo ${fruits[@]}      # All elements
echo ${#fruits[@]}     # Array length

# Command substitution
current_date=$(date)
file_count=$(ls | wc -l)

# User input
read -p "Enter your name: " username
echo "Hello, $username"
```

##### PowerShell Variables

```powershell
# String variables
$name = "John Doe"
$path = "C:\Users\John"

# Numeric variables
$count = 10
$price = 19.99

# Arrays
$fruits = @("apple", "banana", "orange")
$fruits[0]             # First element
$fruits                # All elements
$fruits.Length         # Array length

# Hash tables (dictionaries)
$person = @{
    Name = "John"
    Age = 30
    City = "New York"
}
$person.Name

# User input
$username = Read-Host "Enter your name"
Write-Host "Hello, $username"
```

### Control Structures

#### Conditional Statements

##### Bash Conditionals

```bash
# If statement
if [ $count -gt 5 ]; then
    echo "Count is greater than 5"
elif [ $count -eq 5 ]; then
    echo "Count equals 5"
else
    echo "Count is less than 5"
fi

# String comparisons
if [ "$name" = "John" ]; then
    echo "Hello John!"
fi

# File tests
if [ -f "file.txt" ]; then
    echo "File exists"
fi

if [ -d "directory" ]; then
    echo "Directory exists"
fi

# Case statement
case $1 in
    start)
        echo "Starting service"
        ;;
    stop)
        echo "Stopping service"
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        ;;
esac
```

##### PowerShell Conditionals

```powershell
# If statement
if ($count -gt 5) {
    Write-Host "Count is greater than 5"
}
elseif ($count -eq 5) {
    Write-Host "Count equals 5"
}
else {
    Write-Host "Count is less than 5"
}

# String comparisons
if ($name -eq "John") {
    Write-Host "Hello John!"
}

# File tests
if (Test-Path "file.txt") {
    Write-Host "File exists"
}

# Switch statement
switch ($action) {
    "start" { Write-Host "Starting service" }
    "stop" { Write-Host "Stopping service" }
    default { Write-Host "Usage: start or stop" }
}
```

#### Loops

##### Bash Loops

```bash
# For loop - range
for i in {1..5}; do
    echo "Number: $i"
done

# For loop - array
fruits=("apple" "banana" "orange")
for fruit in "${fruits[@]}"; do
    echo "Fruit: $fruit"
done

# For loop - files
for file in *.txt; do
    echo "Processing: $file"
done

# While loop
count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done

# Until loop
count=1
until [ $count -gt 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done
```

##### PowerShell Loops

```powershell
# For loop
for ($i = 1; $i -le 5; $i++) {
    Write-Host "Number: $i"
}

# ForEach loop - array
$fruits = @("apple", "banana", "orange")
foreach ($fruit in $fruits) {
    Write-Host "Fruit: $fruit"
}

# ForEach loop - files
foreach ($file in Get-ChildItem *.txt) {
    Write-Host "Processing: $($file.Name)"
}

# While loop
$count = 1
while ($count -le 5) {
    Write-Host "Count: $count"
    $count++
}

# Do-While loop
$count = 1
do {
    Write-Host "Count: $count"
    $count++
} while ($count -le 5)
```

### Functions and Error Handling

#### Functions

##### Bash Functions

```bash
# Define function
greet() {
    local name=$1
    echo "Hello, $name!"
}

# Function with return value
add_numbers() {
    local a=$1
    local b=$2
    echo $((a + b))
}

# Use functions
greet "Alice"
result=$(add_numbers 5 3)
echo "Result: $result"

# Function with error checking
backup_file() {
    local source=$1
    local backup_dir=$2
    
    if [ ! -f "$source" ]; then
        echo "Error: Source file does not exist"
        return 1
    fi
    
    if [ ! -d "$backup_dir" ]; then
        mkdir -p "$backup_dir"
    fi
    
    cp "$source" "$backup_dir/"
    echo "Backup completed: $source -> $backup_dir/"
}
```

##### PowerShell Functions

```powershell
# Define function
function Greet {
    param([string]$Name)
    Write-Host "Hello, $Name!"
}

# Advanced function
function Add-Numbers {
    param(
        [int]$a,
        [int]$b
    )
    return $a + $b
}

# Use functions
Greet -Name "Alice"
$result = Add-Numbers -a 5 -b 3
Write-Host "Result: $result"

# Function with error handling
function Backup-File {
    param(
        [string]$Source,
        [string]$BackupDir
    )
    
    try {
        if (-not (Test-Path $Source)) {
            throw "Source file does not exist: $Source"
        }
        
        if (-not (Test-Path $BackupDir)) {
            New-Item -ItemType Directory -Path $BackupDir -Force
        }
        
        Copy-Item $Source $BackupDir
        Write-Host "Backup completed: $Source -> $BackupDir"
    }
    catch {
        Write-Error "Backup failed: $($_.Exception.Message)"
    }
}
```

#### Error Handling

##### Bash Error Handling

```bash
# Exit on error
set -e                     # Exit if any command fails
set -u                     # Exit if undefined variable used
set -o pipefail            # Exit if any pipe command fails

# Manual error checking
if ! command_that_might_fail; then
    echo "Command failed"
    exit 1
fi

# Trap errors
trap 'echo "Error on line $LINENO"' ERR

# Check command success
if grep "pattern" file.txt > /dev/null 2>&1; then
    echo "Pattern found"
else
    echo "Pattern not found"
fi
```

##### PowerShell Error Handling

```powershell
# Error action preference
$ErrorActionPreference = "Stop"  # Stop on errors

# Try-Catch blocks
try {
    Get-Content "nonexistent.txt"
    Write-Host "This won't execute"
}
catch {
    Write-Error "File not found: $($_.Exception.Message)"
}
finally {
    Write-Host "Cleanup code here"
}

# Test commands before execution
if (Test-Path "file.txt") {
    Get-Content "file.txt"
}
else {
    Write-Warning "File not found"
}
```

### Practical Automation Examples

#### System Maintenance Script (Bash)

```bash
#!/bin/bash
# System maintenance script

set -e  # Exit on error

LOG_FILE="/tmp/maintenance.log"
EMAIL="admin@company.com"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cleanup_temp() {
    log "Cleaning temporary files..."
    find /tmp -type f -mtime +7 -delete
    find /var/log -name "*.log.old" -mtime +30 -delete
}

check_disk_space() {
    log "Checking disk space..."
    
    while read output; do
        usage=$(echo $output | awk '{print $5}' | sed 's/%//g')
        partition=$(echo $output | awk '{print $6}')
        
        if [ $usage -gt 85 ]; then
            log "WARNING: $partition is ${usage}% full"
            echo "Disk space warning: $partition is ${usage}% full" | mail -s "Disk Space Alert" "$EMAIL"
        fi
    done <<< "$(df -h | grep -vE '^Filesystem|tmpfs|cdrom')"
}

update_system() {
    log "Updating package lists..."
    if command -v apt > /dev/null; then
        apt update && apt upgrade -y
    elif command -v yum > /dev/null; then
        yum update -y
    fi
}

main() {
    log "Starting system maintenance"
    cleanup_temp
    check_disk_space
    update_system
    log "System maintenance completed"
}

main "$@"
```

#### Log Analysis Script (PowerShell)

```powershell
# Log analysis script
param(
    [string]$LogPath = "C:\Logs",
    [int]$DaysBack = 7,
    [string]$OutputPath = "C:\Reports\log_analysis.html"
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message"
}

function Get-ErrorSummary {
    param([string]$LogDirectory)
    
    $startDate = (Get-Date).AddDays(-$DaysBack)
    $errors = @()
    
    Get-ChildItem -Path $LogDirectory -Filter "*.log" | ForEach-Object {
        Write-Log "Processing $($_.Name)"
        
        Get-Content $_.FullName | Where-Object {
            $_ -match "ERROR|FATAL|CRITICAL" 
        } | ForEach-Object {
            if ($_ -match "(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})") {
                try {
                    $logDate = [DateTime]::Parse($matches[1])
                    if ($logDate -ge $startDate) {
                        $errors += [PSCustomObject]@{
                            File = $_.Name
                            Date = $logDate
                            Message = $_
                        }
                    }
                }
                catch {
                    # Skip lines with invalid dates
                }
            }
        }
    }
    
    return $errors
}

function New-HtmlReport {
    param(
        [array]$Errors,
        [string]$OutputFile
    )
    
    $html = @"
    <!DOCTYPE html>
    <html>
    <head>
        <title>Log Analysis Report</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <h1>Log Analysis Report</h1>
        <p>Generated: $(Get-Date)</p>
        <p>Period: Last $DaysBack days</p>
        <p>Total Errors: $($Errors.Count)</p>
        
        <table>
            <tr>
                <th>Date</th>
                <th>File</th>
                <th>Message</th>
            </tr>
"@
    
    foreach ($error in ($Errors | Sort-Object Date -Descending)) {
        $html += @"
            <tr>
                <td>$($error.Date.ToString("yyyy-MM-dd HH:mm:ss"))</td>
                <td>$($error.File)</td>
                <td class="error">$([System.Web.HttpUtility]::HtmlEncode($error.Message))</td>
            </tr>
"@
    }
    
    $html += @"
        </table>
    </body>
    </html>
"@
    
    $html | Out-File -FilePath $OutputFile -Encoding UTF8
    Write-Log "Report saved to: $OutputFile"
}

try {
    Write-Log "Starting log analysis"
    Write-Log "Log directory: $LogPath"
    Write-Log "Days back: $DaysBack"
    
    if (-not (Test-Path $LogPath)) {
        throw "Log directory not found: $LogPath"
    }
    
    $errors = Get-ErrorSummary -LogDirectory $LogPath
    Write-Log "Found $($errors.Count) errors"
    
    $reportDir = Split-Path $OutputPath -Parent
    if (-not (Test-Path $reportDir)) {
        New-Item -ItemType Directory -Path $reportDir -Force
    }
    
    New-HtmlReport -Errors $errors -OutputFile $OutputPath
    Write-Log "Analysis completed successfully"
}
catch {
    Write-Log "ERROR: $($_.Exception.Message)"
    exit 1
}
```

### Task Scheduling

#### Cron Jobs (Unix/Linux/macOS)

```bash
# Edit crontab
crontab -e

# Example entries
# Run backup script daily at 2 AM
0 2 * * * /home/user/scripts/backup.sh

# Clean temp files every hour
0 * * * * /home/user/scripts/cleanup.sh

# Generate reports on weekdays at 6 PM
0 18 * * 1-5 /home/user/scripts/report.sh

# System maintenance on Sundays at midnight
0 0 * * 0 /home/user/scripts/maintenance.sh
```

#### Windows Task Scheduler

```cmd
# Create scheduled task
schtasks /create /tn "Daily Backup" /tr "C:\Scripts\backup.bat" /sc daily /st 02:00

# Create task with PowerShell script
schtasks /create /tn "Log Analysis" /tr "powershell.exe -File C:\Scripts\log_analysis.ps1" /sc weekly /d sun /st 18:00
```

### XP Tasks - Automation

- [ ] Write a simple script that displays system information
- [ ] Create a script with variables and user input
- [ ] Implement error handling in a script
- [ ] Write a function that performs a specific task
- [ ] Create a script that processes multiple files
- [ ] Set up a scheduled task to run a script automatically
- [ ] Build a maintenance script that cleans up temporary files
- [ ] Develop a monitoring script that checks system resources

---

## Module 10: Advanced CLI Techniques

### Command Line Productivity

#### Keyboard Shortcuts

##### Universal Shortcuts

```bash
Ctrl+C          # Interrupt/cancel current command
Ctrl+D          # EOF (end of file) / logout
Ctrl+Z          # Suspend current process (Unix)
Ctrl+L          # Clear screen
Ctrl+A          # Move cursor to beginning of line
Ctrl+E          # Move cursor to end of line
Ctrl+U          # Delete from cursor to beginning of line
Ctrl+K          # Delete from cursor to end of line
Ctrl+R          # Search command history
Tab             # Auto-complete commands/files
```

##### Bash-Specific Shortcuts

```bash
Alt+B           # Move cursor back one word
Alt+F           # Move cursor forward one word
Alt+D           # Delete word after cursor
Ctrl+W          # Delete word before cursor
Ctrl+Y          # Paste last deleted text
Ctrl+T          # Swap characters
Alt+T           # Swap words
```

##### PowerShell-Specific Shortcuts

```powershell
Ctrl+Space      # Show available parameters
Ctrl+J          # Show available snippets
F7              # Show command history popup
Shift+F7        # Reverse search in history
Tab/Shift+Tab   # Cycle through completions
```

#### Command Completion and History

##### Advanced History Usage

```bash
# History expansion (Bash)
!!              # Last command
!n              # Command number n from history
!string         # Last command starting with string
!?string        # Last command containing string
^old^new        # Replace 'old' with 'new' in last command

# History modifiers
!!:h            # Head (directory) of last command
!!:t            # Tail (filename) of last command
!!:r            # Remove extension from last command
!!:e            # Extension of last command
```

##### Smart Completion

```bash
# Bash completion (install bash-completion package)
command [Tab][Tab]      # Show available options
ssh [Tab][Tab]          # Show known hosts
git [Tab][Tab]          # Show git commands
systemctl start [Tab]   # Show available services

# PowerShell IntelliSense
Get-Process [Tab]       # Cycle through process names
Get-Service -Name [Tab] # Cycle through service names
```

### Performance and Monitoring

#### System Performance Commands

```bash
# CPU and process monitoring
top -n 1                # Single snapshot
htop                    # Interactive process viewer (if available)
ps aux --sort=-%cpu     # Processes sorted by CPU usage
ps aux --sort=-%mem     # Processes sorted by memory usage

# Memory analysis
free -h                 # Human-readable memory info
vmstat 1 5              # Virtual memory stats (1 sec intervals, 5 times)
cat /proc/meminfo       # Detailed memory information

# Disk I/O monitoring
iostat -x 1             # Extended I/O stats
iotop                   # Top-like I/O monitor (if available)
lsof +D /path           # List open files in directory

# Network monitoring
netstat -tuln           # Network connections and listening ports
ss -tuln                # Modern alternative to netstat
iftop                   # Network bandwidth monitor (if available)
nload                   # Network load monitor (if available)
```

#### Windows Performance Monitoring

```cmd
# Task Manager equivalents
tasklist /fo table      # Formatted process list
wmic process get name,processid,percentprocessortime

# System information
systeminfo              # Comprehensive system info
wmic computersystem get TotalPhysicalMemory
wmic logicaldisk get size,freespace,caption

# Network information
netstat -an             # Network connections
ipconfig /all           # Network configuration
```

```powershell
# PowerShell performance cmdlets
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10
Get-Counter "\Processor(_Total)\% Processor Time" -SampleInterval 1 -MaxSamples 5
Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID,Size,FreeSpace
```

### Security and Best Practices

#### Secure Command Line Practices

```bash
# Avoid putting passwords in command line (visible in history)
# Bad:
mysql -u user -ppassword database

# Good:
mysql -u user -p database  # Will prompt for password
# Or use configuration files with proper permissions

# Secure file permissions
chmod 600 ~/.ssh/id_rsa     # Private key permissions
chmod 644 ~/.ssh/id_rsa.pub # Public key permissions
chmod 700 ~/.ssh            # SSH directory permissions

# Clear sensitive history
history -c              # Clear current session history
> ~/.bash_history       # Clear history file
export HISTIGNORE="*password*:*secret*"  # Don't save sensitive commands
```

#### Input Validation and Sanitization

```bash
# Always validate user input
read -p "Enter filename: " filename
if [[ "$filename" =~ ^[a-zA-Z0-9._-]+$ ]]; then
    echo "Valid filename: $filename"
else
    echo "Invalid filename format"
    exit 1
fi

# Use quotes to prevent word splitting
cp "$filename" "$destination"  # Good
cp $filename $destination      # Dangerous if names contain spaces
```

#### Logging and Auditing

```bash
# Enable command logging
export PROMPT_COMMAND='echo "$(date "+%Y-%m-%d.%H:%M:%S") $(pwd) $(history 1)" >> ~/.logs/bash_history.log'

# Log script execution
exec > >(tee -a /var/log/myscript.log)
exec 2>&1
echo "Script started at $(date)"
```

### Advanced Networking

#### Remote Command Execution

```bash
# SSH command execution
ssh user@server 'command'
ssh user@server 'ls -la && df -h'

# SSH with key authentication
ssh -i ~/.ssh/private_key user@server

# SSH tunneling
ssh -L 8080:localhost:80 user@server    # Local port forwarding
ssh -R 8080:localhost:80 user@server    # Remote port forwarding
ssh -D 1080 user@server                 # SOCKS proxy
```

#### File Transfer Commands

```bash
# Secure copy (scp)
scp file.txt user@server:/path/
scp user@server:/path/file.txt ./
scp -r directory/ user@server:/path/

# rsync (synchronization)
rsync -avz --progress local/ user@server:remote/
rsync -avz --delete local/ remote/      # Delete files not in source
rsync -avz --exclude='*.log' local/ remote/  # Exclude patterns

# SFTP (interactive)
sftp user@server
# sftp> put local_file
# sftp> get remote_file
# sftp> exit
```

#### Network Troubleshooting

```bash
# Connectivity testing
ping -c 4 google.com        # Ping 4 times
traceroute google.com       # Show route to destination
mtr google.com              # Continuous traceroute (if available)

# DNS resolution
nslookup google.com         # Basic DNS lookup
dig google.com              # Detailed DNS information
dig @8.8.8.8 google.com     # Query specific DNS server

# Port testing
telnet server.com 80        # Test port connectivity
nc -zv server.com 80        # Netcat port scan
nmap -p 80,443 server.com   # Nmap port scan
```

### Customization and Configuration

#### Shell Customization

```bash
# Bash configuration (~/.bashrc)
# Custom prompt
export PS1='\u@\h:\w\$ '
export PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

# Useful aliases
alias ll='ls -la'
alias la='ls -la'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias less='less -R'

# Useful functions
extract() {
    if [ -f $1 ] ; then
        case $1 in
            *.tar.bz2)   tar xjf $1     ;;
            *.tar.gz)    tar xzf $1     ;;
            *.bz2)       bunzip2 $1     ;;
            *.rar)       unrar e $1     ;;
            *.gz)        gunzip $1      ;;
            *.tar)       tar xf $1      ;;
            *.tbz2)      tar xjf $1     ;;
            *.tgz)       tar xzf $1     ;;
            *.zip)       unzip $1       ;;
            *.Z)         uncompress $1  ;;
            *.7z)        7z x $1        ;;
            *)           echo "'$1' cannot be extracted via extract()" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}
```

#### PowerShell Profile Customization

```powershell
# PowerShell profile ($PROFILE)
# Custom prompt
function prompt {
    $currentPath = Get-Location
    Write-Host "PS " -NoNewline -ForegroundColor Green
    Write-Host "$currentPath" -NoNewline -ForegroundColor Blue
    Write-Host ">" -NoNewline
    return " "
}

# Useful aliases
Set-Alias ll Get-ChildItem
Set-Alias which Get-Command
New-Alias grep Select-String

# Custom functions
function Get-DirectorySize {
    param([string]$Path = ".")
    Get-ChildItem -Path $Path -Recurse | 
    Measure-Object -Property Length -Sum |
    Select-Object @{Name="Size(MB)";Expression={[math]::Round($_.Sum/1MB,2)}}
}

function Test-Port {
    param(
        [string]$Computer,
        [int]$Port
    )
    $tcpClient = New-Object System.Net.Sockets.TcpClient
    try {
        $tcpClient.Connect($Computer, $Port)
        return $true
    }
    catch {
        return $false
    }
    finally {
        $tcpClient.Close()
    }
}
```

### XP Tasks - Advanced Techniques

- [ ] Master 10 keyboard shortcuts for your shell
- [ ] Set up command history with search functionality
- [ ] Create custom aliases for frequently used commands
- [ ] Write a function that combines multiple commands
- [ ] Monitor system performance using CLI tools
- [ ] Practice secure remote command execution with SSH
- [ ] Customize your shell prompt with colors and information
- [ ] Set up command logging for audit purposes
- [ ] Create a personal CLI toolkit with useful functions

---

## Module 11: Capstone Project

### Project: Multi-Platform System Administration Toolkit

Build a comprehensive command-line toolkit that demonstrates mastery of CLI concepts across different platforms.

#### Project Requirements

**Core Features:**

1. **System Information Gathering**
2. **Log Analysis and Monitoring**
3. **File Management and Backup**
4. **Network Diagnostics**
5. **Process Management**
6. **Security Auditing**
7. **Automated Reporting**
8. **Cross-platform Compatibility**

#### Implementation Structure

##### Main Script (Bash Version)

```bash
#!/bin/bash
# system_toolkit.sh - Comprehensive system administration toolkit

set -euo pipefail

# Configuration
TOOLKIT_VERSION="1.0.0"
LOG_DIR="/var/log/system_toolkit"
REPORT_DIR="/tmp/system_reports"
CONFIG_FILE="$HOME/.system_toolkit.conf"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        ERROR)   echo -e "${RED}[$timestamp] ERROR: $message${NC}" ;;
        WARN)
```