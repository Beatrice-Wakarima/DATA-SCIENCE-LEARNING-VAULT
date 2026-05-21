# SSH (Secure Shell) 

## Table of Contents

- [[#SSH Fundamentals]]
- [[#SSH Key Authentication]]
- [[#SSH Configuration]]
- [[#SSH Connection Management]]
- [[#File Transfer with SSH]]
- [[#SSH Tunneling and Port Forwarding]]
- [[#SSH Agent and Key Management]]
- [[#Advanced SSH Features]]
- [[#SSH Server Configuration]]
- [[#SSH Security Best Practices]]
- [[#Troubleshooting SSH]]
- [[#SSH Automation and Scripting]]

## SSH Fundamentals

### What is SSH?

SSH (Secure Shell) is a cryptographic network protocol for operating network services securely over an unsecured network. It provides secure remote access, file transfers, and tunneling capabilities.

> [!note] SSH Components
> 
> - **SSH Client**: Initiates connections (ssh, scp, sftp)
> - **SSH Server**: Accepts connections (sshd daemon)
> - **SSH Protocol**: Encrypted communication standard

### Basic SSH Syntax

```bash
# Basic connection syntax
ssh [options] [user@]hostname [command]

# Examples
ssh user@example.com                    # Connect to server
ssh -p 2222 user@example.com           # Connect on custom port
ssh user@192.168.1.100                 # Connect using IP address
ssh user@example.com "ls -la"          # Execute command remotely
ssh -t user@example.com "top"          # Force pseudo-terminal allocation
```

### SSH Connection Process

```bash
# Verbose connection for debugging
ssh -v user@hostname                    # Basic verbose
ssh -vv user@hostname                   # More verbose
ssh -vvv user@hostname                  # Maximum verbosity

# Connection timeout
ssh -o ConnectTimeout=10 user@hostname

# Connection without host key checking (insecure - testing only)
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null user@hostname
```

## SSH Key Authentication

### Understanding SSH Keys

> [!tip] Key Types Comparison
> 
> - **RSA**: Traditional, widely supported (minimum 2048 bits)
> - **Ed25519**: Modern, fast, secure (recommended)
> - **ECDSA**: Elliptic curve, good performance
> - **DSA**: Deprecated, avoid using

### Generating SSH Keys

```bash
# Generate Ed25519 key (recommended)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Generate RSA key (legacy compatibility)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Generate key with custom filename and location
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_work -C "work@company.com"

# Generate key without passphrase (automation - less secure)
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_auto -N "" -C "automation@example.com"

# Generate key with specific number of rounds (Ed25519)
ssh-keygen -t ed25519 -a 100 -C "your_email@example.com"
```

### Key Management

```bash
# View public key
cat ~/.ssh/id_ed25519.pub
ssh-keygen -y -f ~/.ssh/id_ed25519      # Extract public key from private

# View key fingerprint
ssh-keygen -lf ~/.ssh/id_ed25519.pub    # Public key fingerprint
ssh-keygen -lf ~/.ssh/id_ed25519        # Private key fingerprint

# Change key passphrase
ssh-keygen -p -f ~/.ssh/id_ed25519

# Convert key formats
ssh-keygen -e -f ~/.ssh/id_rsa.pub -m RFC4716     # Convert to RFC4716
ssh-keygen -i -f public_key.rfc4716 -m PKCS8      # Convert from RFC4716
```

### Deploying Public Keys

```bash
# Copy public key to remote server
ssh-copy-id user@hostname
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@hostname

# Copy to custom SSH port
ssh-copy-id -p 2222 user@hostname

# Manual key deployment
cat ~/.ssh/id_ed25519.pub | ssh user@hostname "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# Deploy multiple keys
for key in ~/.ssh/id_*.pub; do
    ssh-copy-id -i "$key" user@hostname
done
```

### SSH Key Permissions

> [!warning] Critical Security Incorrect permissions will cause SSH to reject key authentication.

```bash
# Set correct permissions
chmod 700 ~/.ssh                       # SSH directory
chmod 600 ~/.ssh/id_*                  # Private keys
chmod 644 ~/.ssh/id_*.pub               # Public keys
chmod 600 ~/.ssh/authorized_keys        # Authorized keys file
chmod 600 ~/.ssh/config                 # SSH config file
chmod 644 ~/.ssh/known_hosts            # Known hosts file

# Fix permissions script
#!/bin/bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_* 2>/dev/null
chmod 644 ~/.ssh/id_*.pub 2>/dev/null
chmod 600 ~/.ssh/authorized_keys 2>/dev/null
chmod 600 ~/.ssh/config 2>/dev/null
chmod 644 ~/.ssh/known_hosts 2>/dev/null
echo "SSH permissions fixed"
```

## SSH Configuration

### Client Configuration File

Create `~/.ssh/config` for connection shortcuts and settings:

```bash
# ~/.ssh/config

# Basic host configuration
Host myserver
    HostName server.example.com
    User myusername
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_work

# Jump host configuration
Host jumpbox
    HostName jump.example.com
    User admin
    Port 22
    IdentityFile ~/.ssh/id_rsa

# Internal server through jump host
Host internal
    HostName 192.168.1.100
    User developer
    ProxyJump jumpbox
    IdentityFile ~/.ssh/id_ed25519

# Multiple jump hosts
Host deep-internal
    HostName 10.0.0.50
    User admin
    ProxyJump jumpbox,internal

# Wildcard configurations
Host *.company.com
    User myusername
    IdentityFile ~/.ssh/id_company
    Port 2222

Host dev-*
    User developer
    IdentityFile ~/.ssh/id_dev
    StrictHostKeyChecking no

# Global defaults
Host *
    AddKeysToAgent yes
    UseKeychain yes                    # macOS only
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes
    Compression yes
```

### Advanced SSH Options

```bash
# Connection options
Host production
    HostName prod.example.com
    User produser
    Port 22
    IdentityFile ~/.ssh/id_production
    
    # Connection settings
    ConnectTimeout 10
    ServerAliveInterval 30
    ServerAliveCountMax 3
    TCPKeepAlive yes
    
    # Security settings
    StrictHostKeyChecking yes
    UserKnownHostsFile ~/.ssh/known_hosts
    IdentitiesOnly yes
    PubkeyAuthentication yes
    PasswordAuthentication no
    
    # Forwarding settings
    ForwardAgent no
    ForwardX11 no
    ForwardX11Trusted no
    
    # Compression and performance
    Compression yes
    CompressionLevel 6
    Cipher aes256-gcm@openssh.com
```

### SSH Config File Examples

```bash
# Development environment
Host dev
    HostName dev.company.com
    User developer
    IdentityFile ~/.ssh/id_dev
    LocalForward 3000 localhost:3000
    LocalForward 5432 db.internal:5432
    DynamicForward 1080

# Backup server with specific settings
Host backup
    HostName backup.example.com
    User backup
    IdentityFile ~/.ssh/id_backup
    Compression yes
    ServerAliveInterval 120
    ServerAliveCountMax 720
    BatchMode yes                      # Non-interactive mode

# Git server configuration
Host git.company.com
    User git
    IdentityFile ~/.ssh/id_git
    IdentitiesOnly yes
    StrictHostKeyChecking yes

# Emergency access server
Host emergency
    HostName emergency.example.com
    User root
    IdentityFile ~/.ssh/id_emergency
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel QUIET
```

## SSH Connection Management

### Basic Connection Commands

```bash
# Standard connections
ssh user@hostname                      # Basic connection
ssh -l username hostname               # Alternative user specification
ssh -p 2222 user@hostname             # Custom port
ssh -4 user@hostname                  # Force IPv4
ssh -6 user@hostname                  # Force IPv6

# Connection with specific key
ssh -i ~/.ssh/id_specific user@hostname

# Execute remote commands
ssh user@hostname 'ls -la /var/log'
ssh user@hostname 'ps aux | grep nginx'
ssh user@hostname 'sudo systemctl status apache2'
```

### Interactive Features

```bash
# X11 forwarding (GUI applications)
ssh -X user@hostname                   # Basic X11 forwarding
ssh -Y user@hostname                   # Trusted X11 forwarding
ssh -X user@hostname firefox           # Run GUI application

# Terminal multiplexing
ssh -t user@hostname screen -R session_name
ssh -t user@hostname tmux attach -t session_name

# Force pseudo-terminal
ssh -t user@hostname                   # Allocate pseudo-terminal
ssh -T user@hostname                   # Disable pseudo-terminal
```

### SSH Escape Sequences

> [!tip] SSH Escape Sequences Use these during an active SSH session by pressing Enter, then the escape sequence.

```bash
~.              # Disconnect session
~^Z             # Background SSH process
~#              # List forwarded connections
~&              # Background SSH at logout
~?              # Display help for escape sequences
~C              # Open command line (for port forwarding)
~R              # Request rekeying
```

## File Transfer with SSH

### SCP (Secure Copy Protocol)

```bash
# Basic SCP syntax
scp [options] source destination

# Upload files
scp file.txt user@hostname:/remote/path/
scp -r directory/ user@hostname:/remote/path/
scp file1.txt file2.txt user@hostname:/remote/path/

# Download files
scp user@hostname:/remote/file.txt ./local/path/
scp -r user@hostname:/remote/directory/ ./local/path/

# Copy between remote hosts
scp user1@host1:/path/file user2@host2:/path/destination

# SCP with specific options
scp -P 2222 file.txt user@hostname:/path/        # Custom port
scp -i ~/.ssh/id_rsa file.txt user@hostname:/path/  # Specific key
scp -C file.txt user@hostname:/path/              # Enable compression
scp -v file.txt user@hostname:/path/              # Verbose output
scp -p file.txt user@hostname:/path/              # Preserve timestamps
scp -q file.txt user@hostname:/path/              # Quiet mode
```

### SFTP (SSH File Transfer Protocol)

```bash
# Start SFTP session
sftp user@hostname
sftp -P 2222 user@hostname                # Custom port
sftp -i ~/.ssh/id_rsa user@hostname       # Specific key

# SFTP interactive commands
put localfile remotefile                  # Upload file
get remotefile localfile                  # Download file
put -r local_directory remote_directory   # Upload directory
get -r remote_directory local_directory   # Download directory

# Navigation commands
ls                                        # List remote directory
lls                                       # List local directory
cd remote_directory                       # Change remote directory
lcd local_directory                       # Change local directory
pwd                                       # Show remote working directory
lpwd                                      # Show local working directory

# File operations
mkdir remote_directory                    # Create remote directory
lmkdir local_directory                    # Create local directory
rmdir remote_directory                    # Remove remote directory
rm remote_file                            # Delete remote file
rename old_name new_name                  # Rename remote file

# SFTP batch mode
sftp -b commands.txt user@hostname
# commands.txt content:
# cd /var/log
# get *.log
# quit
```

### RSYNC over SSH

```bash
# Basic rsync over SSH
rsync -avz -e ssh source/ user@hostname:/destination/
rsync -avz -e ssh user@hostname:/source/ ./destination/

# Advanced rsync options
rsync -avz --delete -e ssh source/ user@hostname:/destination/     # Delete extra files
rsync -avz --exclude='*.log' -e ssh source/ user@hostname:/dest/   # Exclude patterns
rsync -avz --include='*.txt' --exclude='*' -e ssh source/ user@hostname:/dest/

# Rsync with custom SSH options
rsync -avz -e "ssh -p 2222 -i ~/.ssh/id_rsa" source/ user@hostname:/dest/

# Bandwidth limiting
rsync -avz --bwlimit=1000 -e ssh source/ user@hostname:/dest/      # Limit to 1MB/s

# Progress and statistics
rsync -avz --progress -e ssh source/ user@hostname:/dest/
rsync -avz --stats -e ssh source/ user@hostname:/dest/

# Dry run (test without making changes)
rsync -avz --dry-run -e ssh source/ user@hostname:/dest/
```

## SSH Tunneling and Port Forwarding

### Local Port Forwarding

```bash
# Basic local forwarding
ssh -L local_port:target_host:target_port user@ssh_server

# Examples
ssh -L 8080:localhost:80 user@webserver              # Access remote web server locally
ssh -L 3306:database.internal:3306 user@jumpbox     # Access internal database
ssh -L 5432:postgres.internal:5432 user@gateway     # PostgreSQL tunnel
ssh -L 443:secure.internal:443 user@proxy           # HTTPS tunnel

# Multiple port forwards
ssh -L 8080:web.internal:80 -L 3306:db.internal:3306 user@gateway

# Background tunneling
ssh -f -N -L 8080:localhost:80 user@webserver        # Run in background
nohup ssh -N -L 8080:localhost:80 user@webserver &   # Immune to hangups

# Auto-restart tunnel
autossh -M 20000 -f -N -L 8080:localhost:80 user@webserver
```

### Remote Port Forwarding

```bash
# Basic remote forwarding
ssh -R remote_port:localhost:local_port user@ssh_server

# Examples
ssh -R 8080:localhost:3000 user@remote_server        # Expose local app remotely
ssh -R 80:localhost:8000 user@public_server          # Expose local web server
ssh -R 2222:localhost:22 user@remote_server          # Reverse SSH access

# Remote forwarding with specific bind address
ssh -R 192.168.1.100:8080:localhost:3000 user@server

# Persistent remote forwarding
autossh -M 20000 -f -N -R 8080:localhost:3000 user@server
```

### Dynamic Port Forwarding (SOCKS Proxy)

```bash
# Create SOCKS proxy
ssh -D local_port user@ssh_server

# Examples
ssh -D 1080 user@proxy_server                        # SOCKS5 proxy on port 1080
ssh -D 8080 user@gateway                             # Alternative port

# Background SOCKS proxy
ssh -f -N -D 1080 user@proxy_server

# Configure applications to use SOCKS proxy:
# - Browser: Set SOCKS5 proxy to localhost:1080
# - curl: curl --socks5 localhost:1080 http://example.com
# - wget: Add to ~/.wgetrc: use_proxy=on, https_proxy=socks5://localhost:1080/
```

### Advanced Tunneling

```bash
# Jump host with port forwarding
ssh -J jumphost -L 8080:target:80 user@destination

# Multiple hops with forwarding
ssh -L 8080:final_destination:80 user@hop1 ssh -L 8080:localhost:80 user@hop2

# VPN-like tunneling (requires root)
sudo ssh -w 0:0 root@server                          # Layer 3 tunneling

# Tunnel through multiple servers
ssh -L 9999:localhost:8888 user@server1 ssh -L 8888:target:80 user@server2
```

## SSH Agent and Key Management

### SSH Agent Basics

```bash
# Start SSH agent
ssh-agent bash                        # Start agent in new shell
eval $(ssh-agent)                     # Start agent in current shell
eval `ssh-agent -s`                   # Alternative syntax

# Add keys to agent
ssh-add                               # Add default keys (~/.ssh/id_*)
ssh-add ~/.ssh/id_ed25519             # Add specific key
ssh-add ~/.ssh/id_*                   # Add all private keys

# List keys in agent
ssh-add -l                            # List key fingerprints
ssh-add -L                            # List public keys

# Remove keys from agent
ssh-add -d ~/.ssh/id_ed25519          # Remove specific key
ssh-add -D                            # Remove all keys

# Key timeouts
ssh-add -t 3600 ~/.ssh/id_ed25519     # Add key with 1-hour timeout
ssh-add -t 0 ~/.ssh/id_ed25519        # Add key without timeout
```

### Persistent SSH Agent

```bash
# Add to ~/.bashrc or ~/.bash_profile
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval $(ssh-agent -s)
    ssh-add
fi

# Kill agent on logout (add to ~/.bash_logout)
if [ -n "$SSH_AGENT_PID" ]; then
    ssh-agent -k
fi

# systemd user service for SSH agent (Linux)
# Create ~/.config/systemd/user/ssh-agent.service
[Unit]
Description=SSH key agent

[Service]
Type=simple
Environment=SSH_AUTH_SOCK=%t/ssh-agent.socket
ExecStart=/usr/bin/ssh-agent -D -a $SSH_AUTH_SOCK

[Install]
WantedBy=default.target
```

### SSH Agent Forwarding

```bash
# Enable agent forwarding
ssh -A user@hostname                  # Command line option
ssh -o ForwardAgent=yes user@hostname # Explicit option

# SSH config for agent forwarding
Host trusted_server
    HostName server.example.com
    User myuser
    ForwardAgent yes

Host *
    ForwardAgent no                   # Disable by default for security
```

> [!warning] Agent Forwarding Security Only enable agent forwarding for trusted servers. Compromised servers can use your forwarded keys.

## Advanced SSH Features

### SSH Multiplexing

```bash
# Enable connection multiplexing
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

# Create socket directory
mkdir -p ~/.ssh/sockets

# Manual multiplexing
ssh -M -S ~/.ssh/socket_name user@hostname           # Master connection
ssh -S ~/.ssh/socket_name user@hostname              # Shared connection

# Check multiplexed connections
ssh -S ~/.ssh/socket_name -O check user@hostname     # Check connection
ssh -S ~/.ssh/socket_name -O exit user@hostname      # Close connection
```

### SSH with Jump Hosts

```bash
# ProxyJump (modern method)
ssh -J jumphost user@destination
ssh -J user1@jump1,user2@jump2 user@destination     # Multiple jumps

# SSH config with jump hosts
Host destination
    HostName dest.internal.com
    User destuser
    ProxyJump jumphost

Host jumphost
    HostName jump.example.com
    User jumpuser

# ProxyCommand (legacy method)
Host destination
    HostName dest.internal.com
    User destuser
    ProxyCommand ssh jumphost nc %h %p
```

### SSH Certificates

```bash
# Generate Certificate Authority (CA)
ssh-keygen -t ed25519 -f ssh_ca -C "SSH Certificate Authority"

# Sign user certificate
ssh-keygen -s ssh_ca -I user_cert -n user1,user2 -V +52w ~/.ssh/id_ed25519.pub

# Sign host certificate
ssh-keygen -s ssh_ca -I host_cert -h -n hostname,hostname.domain.com -V +52w /etc/ssh/ssh_host_ed25519_key.pub

# View certificate
ssh-keygen -L -f ~/.ssh/id_ed25519-cert.pub
```

## SSH Server Configuration

### Basic Server Configuration

Edit `/etc/ssh/sshd_config`:

```bash
# Basic security settings
Port 2222                             # Change default port
Protocol 2                            # Use SSH protocol version 2
PermitRootLogin no                     # Disable root login
MaxAuthTries 3                         # Limit authentication attempts
MaxSessions 2                          # Limit concurrent sessions
LoginGraceTime 60                      # Authentication timeout

# User restrictions  
AllowUsers user1 user2                 # Allow specific users
AllowGroups sshusers                   # Allow specific groups
DenyUsers baduser                      # Deny specific users
DenyGroups wheel                       # Deny specific groups

# Authentication settings
PubkeyAuthentication yes               # Enable public key auth
AuthorizedKeysFile .ssh/authorized_keys # Key location
PasswordAuthentication no              # Disable password auth
PermitEmptyPasswords no                # No empty passwords
ChallengeResponseAuthentication no     # Disable challenge-response

# Host key configuration
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key
```

### Advanced Server Security

```bash
# Network and connection settings
ClientAliveInterval 300                # Send keepalive every 5 minutes
ClientAliveCountMax 2                  # Disconnect after 2 failed keepalives
TCPKeepAlive yes                       # Enable TCP keepalive
Compression yes                        # Enable compression

# Forwarding restrictions
AllowTcpForwarding no                  # Disable port forwarding
AllowStreamLocalForwarding no          # Disable Unix socket forwarding
GatewayPorts no                        # Disable gateway ports
PermitTunnel no                        # Disable tunneling
X11Forwarding no                       # Disable X11 forwarding

# Logging
SyslogFacility AUTHPRIV               # Log facility
LogLevel VERBOSE                       # Detailed logging

# Cryptographic settings
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group16-sha512
```

### SSH Server Management

```bash
# Test configuration
sudo sshd -t                          # Test config syntax
sudo sshd -T                          # Show effective configuration

# Restart SSH service
sudo systemctl restart sshd           # systemd
sudo service ssh restart              # SysV init

# Check SSH service status
sudo systemctl status sshd
sudo journalctl -u sshd -f            # Follow SSH logs

# Generate new host keys
sudo ssh-keygen -A                    # Generate all missing host keys
sudo ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ""
```

## SSH Security Best Practices

### Client Security

> [!tip] Security Checklist Follow these practices for maximum SSH security.

```bash
# Secure key generation
ssh-keygen -t ed25519 -a 100 -f ~/.ssh/id_ed25519_secure

# Strong passphrases
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_with_passphrase

# Verify host fingerprints
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub    # Server-side
ssh-keygen -H -F hostname                           # Client-side lookup

# Use specific keys
ssh -o IdentitiesOnly=yes -i ~/.ssh/id_specific user@hostname
```

### Server Hardening

```bash
# Fail2ban configuration for SSH protection
# /etc/fail2ban/jail.local
[sshd]
enabled = true
port = 2222
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600

# SSH key-only authentication
PasswordAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey

# IP restrictions
# Use iptables or configure AllowUsers with @IP
AllowUsers user@192.168.1.0/24
```

### Network Security

```bash
# SSH over VPN only
# Configure firewall to only allow SSH from VPN networks
sudo iptables -A INPUT -p tcp --dport 2222 -s 10.0.0.0/8 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 2222 -j DROP

# SSH through port knocking
# Configure port knocking to open SSH port temporarily
```

### Monitoring and Auditing

```bash
# SSH connection logging
sudo tail -f /var/log/auth.log | grep sshd

# Monitor failed attempts
sudo grep "Failed password" /var/log/auth.log
sudo grep "Invalid user" /var/log/auth.log

# Active SSH sessions
who                                   # Current users
w                                     # Detailed session info
ss -tnlp | grep :22                  # SSH connections

# SSH key audit script
#!/bin/bash
for key in ~/.ssh/id_*.pub; do
    echo "=== $key ==="
    ssh-keygen -lf "$key"
    echo
done
```

## Troubleshooting SSH

### Common Connection Issues

```bash
# Debug connection problems
ssh -vvv user@hostname                # Maximum verbosity
ssh -F /dev/null user@hostname        # Ignore config files

# Test network connectivity
ping hostname                         # Basic connectivity
telnet hostname 22                    # Test SSH port
nmap hostname -p 22                   # Port scan

# DNS resolution issues
nslookup hostname                     # Check DNS
dig hostname                          # Detailed DNS info
ssh -o PreferredAuthentications=publickey user@ip_address  # Bypass DNS
```

### Permission Problems

```bash
# Check SSH key permissions
ls -la ~/.ssh/
stat ~/.ssh/id_ed25519

# Fix common permission issues
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_*
chmod 644 ~/.ssh/id_*.pub
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/authorized_keys

# Debug permission errors on server
sudo tail -f /var/log/auth.log        # Watch authentication logs
```

### Authentication Failures

```bash
# Test key authentication
ssh -o PasswordAuthentication=no -o PubkeyAuthentication=yes user@hostname

# Verify key is loaded
ssh-add -l                            # List loaded keys
ssh-add ~/.ssh/id_ed25519             # Load specific key

# Check authorized_keys on server
ssh user@hostname "ls -la ~/.ssh/authorized_keys"
ssh user@hostname "cat ~/.ssh/authorized_keys" | grep "$(cat ~/.ssh/id_ed25519.pub)"
```

### Configuration Issues

```bash
# Test SSH config
ssh -F ~/.ssh/config -T git@github.com     # Test specific config
ssh -o UserKnownHostsFile=/dev/null user@hostname  # Ignore known_hosts

# Validate server configuration
sudo sshd -t                          # Test server config
sudo sshd -T | grep -i setting        # Show effective settings
```

## SSH Automation and Scripting

### SSH in Scripts

```bash
#!/bin/bash
# SSH automation script

HOST="user@example.com"
KEY="~/.ssh/id_ed25519"

# Non-interactive SSH
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -i "$KEY" "$HOST" "command"

# SSH with timeout
timeout 30 ssh "$HOST" "long_running_command"

# SSH with retry logic
for i in {1..3}; do
    if ssh "$HOST" "test_command"; then
        echo "Command successful"
        break
    else
        echo "Attempt $i failed, retrying..."
        sleep 5
    fi
done
```

### Parallel SSH Execution

```bash
#!/bin/bash
# Parallel SSH execution

HOSTS=("server1.com" "server2.com" "server3.com")
COMMAND="uptime"

# Execute command on all hosts in parallel
for host in "${HOSTS[@]}"; do
    (
        echo "=== $host ==="
        ssh user@"$host" "$COMMAND"
    ) &
done
wait  # Wait for all background jobs to complete

# Using xargs for parallel execution
echo -e "server1.com\nserver2.com\nserver3.com" | \
xargs -I {} -P 3 ssh user@{} "uptime"
```

### SSH Key Distribution Script

```bash
#!/bin/bash
# Distribute SSH keys to multiple servers

KEY_FILE="~/.ssh/id_ed25519.pub"
SERVERS=("server1.com" "server2.com" "server3.com")
USERNAME="deploy"

for server in "${SERVERS[@]}"; do
    echo "Deploying key to $server..."
    if ssh-copy-id -i "$KEY_FILE" "$USERNAME@$server"; then
        echo "✓ Key deployed to $server successfully"
    else
        echo "✗ Failed to deploy key to $server"
    fi
done
```

### SSH Health Check Script

```bash
#!/bin/bash
# SSH connectivity health check

check_ssh_connectivity() {
    local host=$1
    local user=$2
    local timeout=${3:-10}
    
    if timeout "$timeout" ssh -o BatchMode=yes -o ConnectTimeout=5 "$user@$host" exit 2>/dev/null; then
        echo "✓ $host - SSH connectivity OK"
        return 0
    else
        echo "✗ $host - SSH connectivity FAILED"
        return 1
    fi
}

# Check multiple servers
SERVERS=(
    "web1.example.com:deploy"
    "web2.example.com:deploy"
    "db.example.com:admin"
)

for server_info in "${SERVERS[@]}"; do
    host=$(echo "$server_info" | cut -d':' -f1)
    user=$(echo "$server_info" | cut -d':' -f2)
    check_ssh_connectivity "$host" "$user"
done
```

---

**Related Notes:** [[Linux Commands]], [[Shell Usage]], [[Network Security]], [[System Administration]], [[Encryption]], [[Remote Access]], [[Bash Scripting]], [[Server Management]]

#ssh #security #networking #remote-access #authentication #tunneling #linux #sysadmin #encryption #shell