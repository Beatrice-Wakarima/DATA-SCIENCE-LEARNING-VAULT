# System Administration

#SystemAdministration #Linux #Windows #DevOps #Infrastructure #Security #Monitoring #Automation

**Related:** [[Linux Basics]] | [[Command Line Interface]] | [[Network Administration]] | [[Security Management]] | [[Performance Monitoring]] | [[Backup and Recovery]]

---

## Overview

System Administration involves managing, configuring, and maintaining computer systems and networks. System administrators ensure systems run efficiently, securely, and reliably while supporting users and business operations.

**Core Responsibilities:**

- **System Installation & Configuration**
- **User and Access Management**
- **Security Implementation & Monitoring**
- **Performance Optimization**
- **Backup and Disaster Recovery**
- **Network Administration**
- **Automation and Scripting**
- **Troubleshooting and Support**

---

## Module 1: System Administration Fundamentals

### What is System Administration?

System Administration is the discipline of managing computer systems, networks, and IT infrastructure. It encompasses:

- **Server Management**: Installing, configuring, and maintaining servers
- **User Management**: Creating accounts, managing permissions, access control
- **Security**: Implementing security policies, monitoring threats
- **Monitoring**: Tracking system performance, availability, and health
- **Automation**: Scripting routine tasks and processes
- **Documentation**: Maintaining system documentation and procedures

### Core Principles

#### 1. Reliability and Availability

```bash
# System uptime monitoring
uptime                          # Check system uptime
systemctl status critical-service
journalctl -u service-name -f   # Monitor service logs

# High availability concepts
# - Redundancy
# - Load balancing  
# - Failover mechanisms
# - Disaster recovery planning
```

#### 2. Security First

```bash
# Security hardening basics
sudo ufw enable                 # Enable firewall
sudo fail2ban-client status     # Check intrusion prevention
sudo lynis audit system         # Security audit tool

# Regular security tasks
sudo apt update && sudo apt upgrade    # Keep systems updated
sudo chkrootkit                        # Check for rootkits
```

#### 3. Automation and Efficiency

```bash
# Automate routine tasks
crontab -e                      # Schedule automated tasks
ansible-playbook deploy.yml     # Configuration management
bash /scripts/maintenance.sh    # Automated maintenance
```

#### 4. Monitoring and Alerting

```bash
# System monitoring
htop                           # Process monitoring
iotop                          # I/O monitoring
netstat -tuln                  # Network connections
df -h && free -h              # Disk and memory usage
```

### System Architecture Understanding

#### Hardware Components

- **CPU**: Processing power, cores, architecture
- **Memory (RAM)**: System and application memory
- **Storage**: HDDs, SSDs, RAID configurations
- **Network**: NICs, bandwidth, connectivity
- **Power**: UPS, redundant power supplies

#### Software Layers

```
Applications
├── Application Software (Web servers, databases)
├── Middleware (Application servers, message queues)  
├── Operating System (Linux, Windows, Unix)
├── Drivers (Hardware abstraction)
└── Firmware/BIOS (Hardware initialization)
```

### XP Tasks - Fundamentals

- [ ] Check system information (CPU, memory, disk) on your system
- [ ] Review system logs for the past 24 hours
- [ ] Identify running services and their status
- [ ] Check network configuration and connectivity
- [ ] Document current system configuration
- [ ] Create a basic system monitoring script

---

## Module 2: User and Access Management

### User Account Management

#### Linux User Management

```bash
# Create users
sudo useradd -m -s /bin/bash username     # Create user with home directory
sudo useradd -m -G sudo username          # Create user with sudo access
sudo passwd username                      # Set password

# Modify users  
sudo usermod -aG groupname username       # Add user to group
sudo usermod -s /bin/zsh username         # Change shell
sudo usermod -l newname oldname           # Rename user
sudo usermod -L username                  # Lock account
sudo usermod -U username                  # Unlock account

# Delete users
sudo userdel username                     # Delete user (keep home)
sudo userdel -r username                  # Delete user and home directory

# User information
id username                               # User ID and groups
finger username                           # User information
last username                             # Login history
w                                         # Currently logged in users
```

#### Windows User Management

```powershell
# PowerShell user management
New-LocalUser -Name "username" -Description "User description"
Set-LocalUser -Name "username" -Password (ConvertTo-SecureString "password" -AsPlainText -Force)
Add-LocalGroupMember -Group "Administrators" -Member "username"
Get-LocalUser                             # List users
Remove-LocalUser -Name "username"         # Delete user

# Command Prompt
net user username password /add          # Create user
net user username /active:no             # Disable user
net localgroup administrators username /add  # Add to admin group
```

### Group Management

#### Linux Groups

```bash
# Group operations
sudo groupadd groupname                   # Create group
sudo groupdel groupname                   # Delete group
sudo gpasswd -a username groupname        # Add user to group
sudo gpasswd -d username groupname        # Remove user from group

# View groups
groups username                           # User's groups
getent group                              # All groups
grep "^groupname:" /etc/group            # Group information
```

#### Common Linux Groups

```bash
# Important system groups
sudo        # Sudo access
wheel       # Administrative access (some distros)
www-data    # Web server group
mysql       # Database group
docker      # Docker access
audio       # Audio device access
video       # Video device access
```

### Permission Management

#### File Permissions (Linux)

```bash
# Basic permissions
chmod 755 /path/to/file                   # rwxr-xr-x
chmod 644 /path/to/file                   # rw-r--r--
chmod 600 /path/to/file                   # rw-------

# Recursive permissions
chmod -R 755 /path/to/directory

# Symbolic permissions
chmod u+x filename                        # Add execute for owner
chmod g-w filename                        # Remove write for group
chmod o=r filename                        # Set others to read only
chmod a+r filename                        # Add read for all

# Special permissions
chmod +t /tmp                             # Sticky bit
chmod u+s /usr/bin/passwd                 # SUID
chmod g+s /shared/directory               # SGID
```

#### Access Control Lists (ACLs)

```bash
# Set ACLs
setfacl -m u:username:rwx filename        # Give user full access
setfacl -m g:groupname:r-x filename       # Give group read/execute
setfacl -m d:u:username:rwx directory/    # Default ACL for directory

# View ACLs
getfacl filename                          # Show file ACLs
ls -la filename                           # Shows '+' if ACLs present

# Remove ACLs
setfacl -x u:username filename            # Remove user ACL
setfacl -b filename                       # Remove all ACLs
```

### SSH Key Management

#### SSH Key Generation and Management

```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -C "user@email.com"
ssh-keygen -t ed25519 -C "user@email.com"    # More secure option

# Copy public key to server
ssh-copy-id user@server
cat ~/.ssh/id_rsa.pub | ssh user@server 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'

# SSH agent for key management
eval "$(ssh-agent -s)"                    # Start SSH agent
ssh-add ~/.ssh/id_rsa                     # Add key to agent
ssh-add -l                                # List loaded keys
```

#### SSH Configuration

```bash
# Client configuration (~/.ssh/config)
Host myserver
    HostName server.example.com
    User myuser
    Port 2222
    IdentityFile ~/.ssh/myserver_key
    
Host jumpbox
    HostName jump.example.com
    User admin
    ProxyJump bastion.example.com

# Server configuration (/etc/ssh/sshd_config)
Port 22
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers myuser
```

### Privilege Escalation and Sudo

#### Sudo Configuration

```bash
# Edit sudoers file (always use visudo)
sudo visudo

# Sudoers examples
username ALL=(ALL:ALL) ALL               # Full sudo access
username ALL=(ALL) NOPASSWD: ALL         # No password required
username ALL=(ALL) /bin/systemctl        # Specific command only
%admin ALL=(ALL) ALL                     # Group access

# Sudo aliases
Cmnd_Alias NETWORKING = /sbin/route, /sbin/ifconfig, /bin/ping
User_Alias WEBADMINS = alice, bob, charlie
WEBADMINS ALL = NETWORKING

# Test sudo configuration
sudo -l                                   # List user's sudo privileges
sudo -u otheruser command                 # Run as different user
```

### XP Tasks - User & Access Management

- [ ] Create a new user with appropriate groups
- [ ] Set up SSH key authentication for a user
- [ ] Configure sudo access for specific commands
- [ ] Create a shared directory with group permissions
- [ ] Set up ACLs for fine-grained access control
- [ ] Audit user accounts and permissions
- [ ] Configure SSH server security settings

---

## Module 3: Service and Process Management

### Understanding Services

#### Service Types

- **System Services**: Core OS functionality (networking, logging)
- **Application Services**: User applications (web servers, databases)
- **User Services**: Per-user services
- **Socket Services**: On-demand services triggered by connections

### Systemd Service Management (Modern Linux)

#### Basic Service Operations

```bash
# Service status
systemctl status service-name
systemctl is-active service-name
systemctl is-enabled service-name
systemctl is-failed service-name

# Start/stop/restart services
sudo systemctl start service-name
sudo systemctl stop service-name
sudo systemctl restart service-name
sudo systemctl reload service-name        # Reload config without restart

# Enable/disable auto-start
sudo systemctl enable service-name        # Start at boot
sudo systemctl disable service-name       # Don't start at boot
sudo systemctl mask service-name          # Prevent service from starting
sudo systemctl unmask service-name        # Remove mask
```

#### Service Discovery and Analysis

```bash
# List services
systemctl list-units --type=service
systemctl list-units --type=service --state=active
systemctl list-units --type=service --state=failed
systemctl list-unit-files --type=service

# Service dependencies
systemctl list-dependencies service-name
systemctl show service-name
```

#### Creating Custom Services

```bash
# Create service file (/etc/systemd/system/myapp.service)
sudo nano /etc/systemd/system/myapp.service

# Example service file
[Unit]
Description=My Application
After=network.target
Requires=network.target

[Service]
Type=simple
User=myuser
Group=mygroup
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/start.sh
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable myapp.service
sudo systemctl start myapp.service
```

### Process Management

#### Process Monitoring

```bash
# Real-time process monitoring
top                                       # Traditional process viewer
htop                                      # Enhanced process viewer
atop                                      # Advanced system monitor
iotop                                     # I/O monitoring
```

#### Process Control

```bash
# List processes
ps aux                                    # All processes
ps -ef                                    # Full format
ps -u username                            # User's processes
pgrep -u username                         # Process IDs by user

# Kill processes
kill PID                                  # Graceful termination
kill -9 PID                              # Force kill
kill -HUP PID                            # Reload signal
killall process-name                      # Kill by name
pkill -f pattern                         # Kill by pattern

# Process priority
nice -n 10 command                        # Start with lower priority
renice 10 -p PID                         # Change running process priority
```

#### Background Job Management

```bash
# Job control
command &                                 # Run in background
nohup command &                          # Run immune to hangups
jobs                                     # List jobs
fg %1                                    # Bring job 1 to foreground
bg %1                                    # Send job 1 to background

# Advanced background execution
screen -S session-name command           # Detachable session
tmux new-session -d -s mysession         # Terminal multiplexer
```

### Windows Service Management

#### Windows Services

```powershell
# PowerShell service management
Get-Service                              # List all services
Get-Service -Name "ServiceName"          # Specific service
Start-Service -Name "ServiceName"        # Start service
Stop-Service -Name "ServiceName"         # Stop service
Restart-Service -Name "ServiceName"      # Restart service
Set-Service -Name "ServiceName" -StartupType Automatic  # Auto-start

# Command prompt
sc query                                 # List services
sc query ServiceName                     # Service status
net start ServiceName                    # Start service
net stop ServiceName                     # Stop service
```

### Performance Monitoring and Tuning

#### Resource Monitoring

```bash
# CPU monitoring
top -n 1                                 # Single snapshot
sar -u 1 10                             # CPU utilization (10 samples)
mpstat 1 5                              # Multiprocessor stats

# Memory monitoring
free -h                                  # Memory usage
vmstat 1 5                              # Virtual memory stats
sar -r 1 10                             # Memory utilization

# Disk I/O monitoring
iostat -x 1                             # Extended I/O stats
sar -d 1 10                             # Disk activity
iotop                                   # Top-like I/O monitor

# Network monitoring
sar -n DEV 1 10                         # Network interface stats
netstat -i                              # Interface statistics
ss -tuln                                # Socket statistics
```

#### Performance Tuning

```bash
# System limits
ulimit -a                               # Show current limits
ulimit -n 4096                          # Set file descriptor limit

# Persistent limits (/etc/security/limits.conf)
* soft nofile 4096
* hard nofile 8192
* soft nproc 2048
* hard nproc 4096

# Kernel parameters (/etc/sysctl.conf)
vm.swappiness=10                        # Reduce swap usage
net.core.somaxconn=1024                 # Increase connection queue
fs.file-max=65536                       # Maximum open files

# Apply sysctl changes
sudo sysctl -p
```

### XP Tasks - Service & Process Management

- [ ] Check status of all system services
- [ ] Create a custom systemd service
- [ ] Monitor system processes and resource usage
- [ ] Set up process monitoring and alerting
- [ ] Configure service dependencies and startup order
- [ ] Optimize system performance parameters
- [ ] Practice process troubleshooting techniques

---

## Module 4: Storage and File System Management

### File System Types and Concepts

#### Common File Systems

```bash
# Linux file systems
ext4        # Default Linux filesystem
xfs         # High-performance filesystem
btrfs       # Advanced filesystem with snapshots
zfs         # Advanced filesystem with built-in RAID

# Other file systems
ntfs        # Windows filesystem
fat32       # Universal compatibility
exfat       # Large file support
```

#### File System Hierarchy

```bash
# Standard Linux directory structure
/           # Root directory
/bin        # Essential binaries
/boot       # Boot loader files
/dev        # Device files
/etc        # Configuration files
/home       # User home directories
/lib        # Essential libraries
/media      # Removable media
/mnt        # Mount points
/opt        # Optional packages
/proc       # Process information
/root       # Root user home
/run        # Runtime data
/sbin       # System binaries
/srv        # Service data
/sys        # System information
/tmp        # Temporary files
/usr        # User programs
/var        # Variable data
```

### Disk Management

#### Disk Information and Partitioning

```bash
# View disks and partitions
lsblk                                    # Block device tree
fdisk -l                                 # List all disks
parted -l                                # Parted disk info
df -h                                    # Mounted filesystem usage
du -sh /path                            # Directory usage

# Partition management
sudo fdisk /dev/sdb                      # Partition disk (MBR)
sudo parted /dev/sdb                     # Partition disk (GPT)
sudo gdisk /dev/sdb                      # GPT partitioning

# Create partitions with parted
sudo parted /dev/sdb mklabel gpt
sudo parted /dev/sdb mkpart primary ext4 0% 100%
```

#### File System Creation and Management

```bash
# Create file systems
sudo mkfs.ext4 /dev/sdb1                 # Create ext4 filesystem
sudo mkfs.xfs /dev/sdb1                  # Create XFS filesystem
sudo mkfs.btrfs /dev/sdb1                # Create Btrfs filesystem

# File system checks and repair
sudo fsck /dev/sdb1                      # Check filesystem
sudo fsck.ext4 /dev/sdb1                 # Check ext4 specifically
sudo xfs_repair /dev/sdb1                # Repair XFS filesystem

# File system information
sudo tune2fs -l /dev/sdb1                # Ext4 filesystem info
sudo xfs_info /dev/sdb1                  # XFS filesystem info
```

### Mount Management

#### Mounting File Systems

```bash
# Manual mounting
sudo mkdir /mnt/mydisk
sudo mount /dev/sdb1 /mnt/mydisk         # Mount filesystem
sudo mount -t ext4 /dev/sdb1 /mnt/mydisk # Specify filesystem type
sudo umount /mnt/mydisk                  # Unmount

# Mount with options
sudo mount -o rw,noatime /dev/sdb1 /mnt/mydisk      # Read-write, no access time
sudo mount -o ro /dev/sdb1 /mnt/mydisk              # Read-only
sudo mount -o bind /source /target                   # Bind mount
```

#### Automatic Mounting (/etc/fstab)

```bash
# Edit fstab for persistent mounts
sudo nano /etc/fstab

# fstab format: device mountpoint filesystem options dump pass
/dev/sdb1 /mnt/mydisk ext4 defaults 0 2
UUID=abc123 /home/user/data ext4 defaults,noatime 0 2
//server/share /mnt/network cifs username=user,password=pass 0 0

# Test fstab entries
sudo mount -a                           # Mount all fstab entries
sudo findmnt --verify                   # Verify fstab
```

### Logical Volume Management (LVM)

#### LVM Concepts

- **Physical Volume (PV)**: Physical disk or partition
- **Volume Group (VG)**: Collection of physical volumes
- **Logical Volume (LV)**: Virtual partition from volume group

#### LVM Operations

```bash
# Create physical volume
sudo pvcreate /dev/sdb1
sudo pvdisplay                           # Show physical volumes

# Create volume group
sudo vgcreate myvg /dev/sdb1
sudo vgdisplay                           # Show volume groups

# Create logical volume
sudo lvcreate -n mylv -L 10G myvg        # Create 10GB logical volume
sudo lvcreate -n mylv -l 100%FREE myvg   # Use all free space
sudo lvdisplay                           # Show logical volumes

# Extend logical volume
sudo lvextend -L +5G /dev/myvg/mylv      # Add 5GB
sudo resize2fs /dev/myvg/mylv            # Resize ext4 filesystem
```

### RAID Configuration

#### Software RAID with mdadm

```bash
# RAID levels
# RAID 0: Striping (performance, no redundancy)
# RAID 1: Mirroring (redundancy)
# RAID 5: Striping with parity (performance + redundancy)
# RAID 10: Striped mirrors (performance + redundancy)

# Create RAID arrays
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1  # RAID 1
sudo mdadm --create /dev/md1 --level=5 --raid-devices=3 /dev/sdb1 /dev/sdc1 /dev/sdd1  # RAID 5

# Monitor RAID
cat /proc/mdstat                         # RAID status
sudo mdadm --detail /dev/md0            # Detailed info

# RAID configuration file
sudo mdadm --detail --scan >> /etc/mdadm/mdadm.conf
```

### Storage Performance and Optimization

#### Monitoring Storage Performance

```bash
# I/O statistics
iostat -x 1                             # Extended I/O stats
sar -d 1 10                             # Disk activity
iotop                                   # Process I/O usage
lsof +D /path                           # Files open in directory

# Disk performance testing
sudo hdparm -tT /dev/sda                # Disk speed test
sudo dd if=/dev/zero of=/tmp/test bs=1G count=1 oflag=dsync  # Write test
```

#### Storage Optimization

```bash
# Mount options for performance
# noatime: Don't update access times
# data=writeback: Faster writes (less safe)
# barrier=0: Disable barriers (SSD optimization)

# SSD optimization
sudo fstrim -v /                        # Manual TRIM
sudo systemctl enable fstrim.timer      # Automatic TRIM

# File system tuning
sudo tune2fs -o journal_data_writeback /dev/sdb1  # Change journaling mode
```

### Backup and Recovery

#### File-level Backup Tools

```bash
# rsync backups
rsync -av --delete /source/ /backup/    # Mirror backup
rsync -av --backup --backup-dir=/backup/old /source/ /backup/  # Incremental

# tar archives
tar -czf backup-$(date +%Y%m%d).tar.gz /home/  # Compressed archive
tar -xzf backup.tar.gz                  # Extract archive

# System backup with excludes
rsync -av --exclude='/proc/*' --exclude='/tmp/*' --exclude='/sys/*' / /backup/
```

#### Block-level Backup Tools

```bash
# dd for disk imaging
sudo dd if=/dev/sda of=/backup/disk.img bs=4M status=progress  # Full disk image
sudo dd if=/dev/sda1 of=/backup/partition.img bs=4M            # Partition image

# Restore from image
sudo dd if=/backup/disk.img of=/dev/sdb bs=4M status=progress
```

### XP Tasks - Storage Management

- [ ] Create and format a new partition
- [ ] Set up automatic mounting in /etc/fstab
- [ ] Configure LVM with physical and logical volumes
- [ ] Monitor disk I/O performance
- [ ] Set up a simple RAID array (if multiple disks available)
- [ ] Create automated backup scripts
- [ ] Practice file system repair and recovery

---

## Module 5: Network Administration

### Network Fundamentals

#### OSI Model and TCP/IP Stack

```bash
# Layer understanding
Physical     # Cables, switches, NICs
Data Link    # MAC addresses, Ethernet
Network      # IP addresses, routing
Transport    # TCP, UDP ports
Session      # Connection management
Presentation # Encryption, compression
Application  # HTTP, SSH, FTP
```

#### IP Addressing and Subnetting

```bash
# IPv4 address classes
Class A: 1.0.0.0    - 126.255.255.255  (/8)
Class B: 128.0.0.0  - 191.255.255.255  (/16)
Class C: 192.0.0.0  - 223.255.255.255  (/24)

# Private IP ranges
10.0.0.0/8       # Class A private
172.16.0.0/12    # Class B private
192.168.0.0/16   # Class C private

# Subnet calculation examples
192.168.1.0/24   # 256 addresses (254 usable)
192.168.1.0/25   # 128 addresses (126 usable)
192.168.1.0/26   # 64 addresses (62 usable)
```

### Network Interface Configuration

#### Linux Network Configuration

```bash
# View network interfaces
ip addr show                             # Modern command
ip link show                             # Link layer info
ifconfig                                 # Traditional command

# Configure interfaces
sudo ip addr add 192.168.1.100/24 dev eth0    # Add IP address
sudo ip link set eth0 up                       # Bring interface up
sudo ip link set eth0 down                     # Bring interface down

# Persistent configuration (Ubuntu/Debian - /etc/netplan/)
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true
    eth1:
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]

# Apply netplan configuration
sudo netplan apply
```

#### Red Hat/CentOS Network Configuration

```bash
# Interface configuration files (/etc/sysconfig/network-scripts/)
# ifcfg-eth0
DEVICE=eth0
BOOTPROTO=static
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
DNS2=8.8.4.4
ONBOOT=yes

# Restart networking
sudo systemctl restart network
sudo nmcli connection reload
```

### Routing and Gateway Management

#### Routing Table Management

```bash
# View routing table
ip route show                            # Current routes
route -n                                 # Traditional command
netstat -rn                             # Alternative view

# Add/remove routes
sudo ip route add 192.168.2.0/24 via 192.168.1.1    # Add route
sudo ip route del 192.168.2.0/24                      # Delete route
sudo ip route add default via 192.168.1.1             # Default gateway

# Persistent routes (varies by distribution)
# Ubuntu/Debian: Add to netplan configuration
# Red Hat/CentOS: /etc/sysconfig/network-scripts/route-interface
```

#### Advanced Routing

```bash
# Policy-based routing
sudo ip rule add from 192.168.1.0/24 table 100
sudo ip route add default via 192.168.1.1 table 100

# Load balancing (multiple gateways)
sudo ip route add default scope global nexthop via 192.168.1.1 weight 1 nexthop via 192.168.2.1 weight 1
```

### DNS Configuration

#### DNS Client Configuration

```bash
# DNS resolution files
/etc/resolv.conf                         # DNS servers
/etc/hosts                              # Static hostname resolution
/etc/nsswitch.conf                      # Resolution order

# Example /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
search company.local
domain company.local

# DNS testing
nslookup hostname                        # Basic DNS lookup
dig hostname                            # Detailed DNS lookup
dig @8.8.8.8 hostname                   # Query specific server
host hostname                           # Simple lookup
```

#### DNS Server Setup (BIND)

```bash
# Install BIND
sudo apt install bind9                   # Ubuntu/Debian
sudo yum install bind                    # Red Hat/CentOS

# Main configuration (/etc/bind/named.conf.local)
zone "example.com" {
    type master;
    file "/etc/bind/db.example.com";
};

# Zone file (/etc/bind/db.example.com)
$TTL    604800
@       IN      SOA     ns1.example.com. admin.example.com. (
                              2021032901         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL

@       IN      NS      ns1.example.com.
@       IN      A       192.168.1.10
ns1     IN      A       192.168.1.10
www     IN      A       192.168.1.20
```

### DHCP Configuration

#### DHCP Server Setup

```bash
# Install DHCP server
sudo apt install isc-dhcp-server         # Ubuntu/Debian
sudo yum install dhcp                     # Red Hat/CentOS

# Configuration (/etc/dhcp/dhcpd.conf)
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.100 192.168.1.200;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8, 8.8.4.4;
    option domain-name "company.local";
    default-lease-time 600;
    max-lease-time 7200;
}

# Static reservations
host workstation1 {
    hardware ethernet 00:11:22:33:44:55;
    fixed-address 192.168.1.50;
}

# Start DHCP service
sudo systemctl enable dhcpd
sudo systemctl start dhcpd
```

### Firewall Configuration

#### iptables (Traditional Linux Firewall)

```bash
# Basic iptables rules
sudo iptables -L                         # List current rules
sudo iptables -F                         # Flush all rules

# Allow traffic
sudo iptables -A INPUT -i lo -j ACCEPT                    # Allow loopback
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT  # Allow established
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT        # Allow SSH
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT        # Allow HTTP

# Block traffic
sudo iptables -A INPUT -j DROP                            # Default drop

# Save rules (Ubuntu/Debian)
sudo iptables-save > /etc/iptables/rules.v4
```

#### UFW (Uncomplicated Firewall)

```bash
# UFW basic usage
sudo ufw enable                          # Enable firewall
sudo ufw disable                         # Disable firewall
sudo ufw status                          # Show status
sudo ufw status verbose                  # Detailed status

# Allow/deny rules
sudo ufw allow 22                        # Allow SSH
sudo ufw allow ssh                       # Allow SSH (by name)
sudo ufw allow from 192.168.1.0/24      # Allow from subnet
sudo ufw deny 23                         # Deny telnet
sudo ufw delete allow 80                 # Remove rule

# Application profiles
sudo ufw app list                        # List application profiles
sudo ufw allow 'Apache Full'            # Allow Apache
```

#### firewalld (Red Hat/CentOS/Fedora)

```bash
# firewalld management
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo firewall-cmd --state                # Check status

# Zone management
sudo firewall-cmd --get-default-zone     # Show default zone
sudo firewall-cmd --list-all            # List all settings
sudo firewall-cmd --zone=public --list-all  # List zone settings

# Add/remove services
sudo firewall-cmd --add-service=ssh      # Temporary
sudo firewall-cmd --add-service=ssh --permanent  # Permanent
sudo firewall-cmd --add-port=8080/tcp --permanent  # Add custom port
sudo firewall-cmd --reload               # Reload configuration
```

### Network Monitoring and Troubleshooting

#### Network Connectivity Testing

```bash
# Basic connectivity
ping -c 4 google.com                     # Test connectivity
ping6 -c 4 ipv6.google.com              # IPv6 connectivity
traceroute google.com                    # Show route path
mtr google.com                           # Continuous traceroute

# Port testing
telnet server.com 80                     # Test port connectivity
nc -zv server.com 80                     # Netcat port test
nmap -p 80,443 server.com               # Port scan
```

#### Network Statistics and Monitoring

```bash
# Network connections
netstat -tuln                           # Listening ports
netstat -i                              # Interface statistics
ss -tuln                                # Modern alternative to netstat
ss -s                                   # Socket statistics

# Bandwidth monitoring
iftop                                   # Real-time bandwidth usage
nethogs                                 # Per-process network usage
vnstat                                  # Network statistics
sar -n DEV 1 5                         # Network interface stats

# Packet capture
sudo tcpdump -i eth0                    # Capture packets on interface
sudo tcpdump -i eth0 port 80            # Capture HTTP traffic
sudo tcpdump -i eth0 host 192.168.1.1  # Capture traffic to/from host
```

#### Network Performance Optimization

```bash
# Network tuning parameters (/etc/sysctl.conf)
net.core.rmem_max = 16777216            # Increase receive buffer
net.core.wmem_max = 16777216            # Increase send buffer
net.ipv4.tcp_congestion_control = bbr   # Use BBR congestion control
net.core.netdev_max_backlog = 5000      # Increase network backlog

# Apply network optimizations
sudo sysctl -p
```

### XP Tasks - Network Administration

- [ ] Configure a static IP address on a network interface
- [ ] Set up DNS resolution with custom entries
- [ ] Configure firewall rules for web server access
- [ ] Monitor network traffic and identify bottlenecks
- [ ] Set up DHCP reservations for specific devices
- [ ] Troubleshoot network connectivity issues
- [ ] Implement network security policies

---

## Module 6: Security and Compliance

### System Hardening

#### Security Baseline Configuration

```bash
# Disable unnecessary services
sudo systemctl list-unit-files --type=service --state=enabled
sudo systemctl disable service-name
sudo systemctl mask service-name         # Prevent accidental enabling

# Remove unnecessary packages
sudo apt autoremove                      # Remove unused packages
sudo apt purge package-name              # Completely remove package

# Secure boot process
sudo chmod 700 /boot                     # Restrict boot directory access
sudo chown root:root /etc/grub.d/*       # Secure GRUB configuration
```

#### File System Security

```bash
# Secure file permissions
find / -type f -perm -4000 -ls 2>/dev/null    # Find SUID files
find / -type f -perm -2000 -ls 2>/dev/null    # Find SGID files
find / -type f -perm -1000 -ls 2>/dev/null    # Find sticky bit files

# Secure important directories
sudo chmod 700 /root                          # Root home directory
sudo chmod 644 /etc/passwd                    # User database
sudo chmod 640 /etc/shadow                    # Password hashes
sudo chmod 644 /etc/group                     # Group database

# Immutable files (prevent tampering)
sudo chattr +i /etc/passwd                    # Make file immutable
sudo chattr +i /etc/shadow
sudo lsattr /etc/passwd                       # Check attributes
```

#### Network Security

```bash
# Disable IPv6 (if not needed)
echo 'net.ipv6.conf.all.disable_ipv6 = 1' >> /etc/sysctl.conf

# IP spoofing protection
echo 'net.ipv4.conf.all.rp_filter = 1' >> /etc/sysctl.conf

# Disable IP forwarding (if not a router)
echo 'net.ipv4.ip_forward = 0' >> /etc/sysctl.conf

# Disable ICMP redirects
echo 'net.ipv4.conf.all.accept_redirects = 0' >> /etc/sysctl.conf
echo 'net.ipv4.conf.all.send_redirects = 0' >> /etc/sysctl.conf

# Apply changes
sudo sysctl -p
```

### User Security and Authentication

#### Password Policies

```bash
# Password policy configuration (/etc/login.defs)
PASS_MAX_DAYS   90                       # Password expiry
PASS_MIN_DAYS   1                        # Minimum password age
PASS_MIN_LEN    8                        # Minimum password length
PASS_WARN_AGE   7                        # Warning before expiry

# PAM password complexity (/etc/pam.d/common-password)
password requisite pam_pwquality.so retry=3 minlen=8 difok=3

# Account lockout policy (/etc/pam.d/common-auth)
auth required pam_tally2.so deny=3 onerr=fail unlock_time=600
```

#### SSH Security Hardening

```bash
# SSH server configuration (/etc/ssh/sshd_config)
Port 2222                               # Change default port
Protocol 2                              # Use SSH protocol 2
PermitRootLogin no                      # Disable root login
PasswordAuthentication no               # Use keys only
PubkeyAuthentication yes                # Enable key authentication
MaxAuthTries 3                          # Limit authentication attempts
ClientAliveInterval 300                 # Client timeout
ClientAliveCountMax 2                   # Maximum client alive messages
AllowUsers alice bob                    # Limit allowed users
DenyUsers baduser                       # Explicitly deny users

# Restart SSH service
sudo systemctl restart sshd
```

#### Two-Factor Authentication

```bash
# Install Google Authenticator PAM module
sudo apt install libpam-google-authenticator

# Configure for user
google-authenticator                     # Generate secret key and QR code

# PAM configuration (/etc/pam.d/sshd)
auth required pam_google_authenticator.so

# SSH configuration (/etc/ssh/sshd_config)
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
```

### Intrusion Detection and Prevention

#### Fail2ban Configuration

```bash
# Install fail2ban
sudo apt install fail2ban

# Configuration (/etc/fail2ban/jail.local)
[DEFAULT]
bantime = 3600                          # Ban for 1 hour
findtime = 600                          # Find failures in 10 minutes
maxretry = 3                            # Maximum retry attempts
ignoreip = 127.0.0.1/8 192.168.1.0/24  # Whitelist IPs

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3

[apache-auth]
enabled = true
port = http,https
logpath = /var/log/apache2/*error.log

# Check fail2ban status
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

#### Log Monitoring with LogWatch

```bash
# Install LogWatch
sudo apt install logwatch

# Configuration (/etc/logwatch/conf/logwatch.conf)
MailTo = admin@company.com
Range = yesterday
Detail = Med
Service = All

# Manual run
sudo logwatch --detail Med --service All --range yesterday --mailto admin@company.com
```

#### File Integrity Monitoring

```bash
# Install AIDE (Advanced Intrusion Detection Environment)
sudo apt install aide

# Initialize database
sudo aide --init
sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# Configuration (/etc/aide/aide.conf)
/bin p+i+u+g+s+m+c+md5
/sbin p+i+u+g+s+m+c+md5
/usr/bin p+i+u+g+s+m+c+md5
/etc p+i+u+g+s+m+c+md5

# Check for changes
sudo aide --check

# Automate with cron
echo "0 2 * * * root /usr/bin/aide --check" >> /etc/crontab
```

### Vulnerability Management

#### System Updates and Patching

```bash
# Automated updates (Ubuntu/Debian)
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades

# Configuration (/etc/apt/apt.conf.d/50unattended-upgrades)
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
    "${distro_id}:${distro_codename}-updates";
};

# Red Hat/CentOS automatic updates
sudo yum install yum-cron
sudo systemctl enable yum-cron
sudo systemctl start yum-cron
```

#### Security Scanning

```bash
# Nmap security scanning
nmap -sS -O target.com                  # SYN scan with OS detection
nmap -sV target.com                     # Version detection
nmap --script vuln target.com           # Vulnerability scripts

# OpenVAS vulnerability scanner
sudo apt install openvas
sudo openvas-setup
```

#### Compliance Auditing

```bash
# Lynis security auditing
sudo apt install lynis
sudo lynis audit system                 # Full system audit
sudo lynis audit system --auditor "IT Security" --cronjob

# CIS benchmark checking
wget https://github.com/dev-sec/cis-dil-benchmark/archive/master.zip
# Run benchmark tests according to CIS guidelines
```

### XP Tasks - Security & Compliance

- [ ] Implement system hardening baseline configuration
- [ ] Set up SSH key authentication with 2FA
- [ ] Configure fail2ban for intrusion prevention
- [ ] Set up automated security updates
- [ ] Perform vulnerability scan on your system
- [ ] Configure file integrity monitoring
- [ ] Create security incident response procedures

---

## Module 7: Monitoring and Performance Optimization

### System Monitoring Fundamentals

#### Key Performance Indicators (KPIs)

```bash
# The four golden signals of monitoring:
# 1. Latency - Response time
# 2. Traffic - Request rate
# 3. Errors - Error rate
# 4. Saturation - Resource utilization

# System load averages
uptime                                  # Load averages (1, 5, 15 min)
w                                       # Users and load
cat /proc/loadavg                       # Raw load average data
```

#### Resource Monitoring

```bash
# CPU monitoring
top                                     # Interactive process viewer
htop                                    # Enhanced process viewer
sar -u 1 10                            # CPU utilization over time
mpstat 1 5                             # Multi-processor statistics
iostat -c 1 5                          # CPU statistics

# Memory monitoring
free -h                                 # Memory usage summary
cat /proc/meminfo                       # Detailed memory information
vmstat 1 5                             # Virtual memory statistics
sar -r 1 10                            # Memory utilization over time

# Disk I/O monitoring
iostat -x 1 5                          # Extended I/O statistics
iotop                                   # Top-like I/O monitor
sar -d 1 10                            # Disk activity
lsof +D /path                          # Files open in directory
```

### Performance Analysis Tools

#### System Analysis

```bash
# Process analysis
ps aux --sort=-%cpu | head -10          # Top CPU processes
ps aux --sort=-%mem | head -10          # Top memory processes
pgrep -l process_name                   # Find processes by name
pidstat -p PID 1 5                     # Process statistics

# Network analysis
netstat -i                             # Interface statistics
ss -s                                  # Socket summary
sar -n DEV 1 10                        # Network device statistics
iftop                                  # Bandwidth usage by connection
nethogs                                # Network usage by process
```

#### Advanced Performance Tools

```bash
# Perf - Linux profiling tool
perf top                               # Real-time performance counters
perf record -g command                 # Record performance data
perf report                            # Analyze recorded data

# Strace - System call tracer
strace -p PID                          # Trace system calls of process
strace -c command                      # Count system calls
strace -e open,read,write command      # Trace specific system calls

# Ltrace - Library call tracer
ltrace -p PID                          # Trace library calls
ltrace -c command                      # Count library calls
```

### Monitoring Infrastructure

#### Nagios Core Setup

```bash
# Install Nagios Core
sudo apt install nagios4 nagios-plugins-contrib nagios-nrpe-plugin

# Main configuration (/etc/nagios4/nagios.cfg)
log_file=/var/log/nagios4/nagios.log
cfg_file=/etc/nagios4/objects/commands.cfg
cfg_file=/etc/nagios4/objects/contacts.cfg
cfg_file=/etc/nagios4/objects/timeperiods.cfg
cfg_file=/etc/nagios4/objects/templates.cfg
cfg_dir=/etc/nagios4/conf.d

# Define hosts (/etc/nagios4/conf.d/hosts.cfg)
define host {
    use                     linux-server
    host_name               webserver1
    alias                   Web Server 1
    address                 192.168.1.10
    contact_groups          admins
}

# Define services (/etc/nagios4/conf.d/services.cfg)
define service {
    use                     generic-service
    host_name               webserver1
    service_description     HTTP
    check_command           check_http
    contact_groups          admins
}
```

#### Zabbix Monitoring Setup

```bash
# Install Zabbix server
wget https://repo.zabbix.com/zabbix/5.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_5.4-1+ubuntu20.04_all.deb
sudo dpkg -i zabbix-release_5.4-1+ubuntu20.04_all.deb
sudo apt update
sudo apt install zabbix-server-mysql zabbix-frontend-php zabbix-nginx-conf zabbix-sql-scripts zabbix-agent

# Configure database
mysql -uroot -p
create database zabbix character set utf8 collate utf8_bin;
create user zabbix@localhost identified by 'password';
grant all privileges on zabbix.* to zabbix@localhost;
quit;

# Import initial schema
zcat /usr/share/doc/zabbix-sql-scripts/mysql/create.sql.gz | mysql -uzabbix -p zabbix
```

#### Prometheus and Grafana

```bash
# Install Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.30.3/prometheus-2.30.3.linux-amd64.tar.gz
tar xvf prometheus-2.30.3.linux-amd64.tar.gz
sudo mv prometheus-2.30.3.linux-amd64 /opt/prometheus

# Prometheus configuration (prometheus.yml)
global:
  scrape_interval: 15s

rule_files:
  - "first_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

# Install Node Exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.2.2/node_exporter-1.2.2.linux-amd64.tar.gz
tar xvf node_exporter-1.2.2.linux-amd64.tar.gz
sudo mv node_exporter-1.2.2.linux-amd64/node_exporter /usr/local/bin/
```

### Log Management

#### Centralized Logging with rsyslog

```bash
# Server configuration (/etc/rsyslog.conf)
# Enable UDP reception
$ModLoad imudp
$UDPServerRun 514
$UDPServerAddress 0.0.0.0

# Template for log format
$template DynamicFile,"/var/log/remote/%HOSTNAME%/%programname%.log"
*.* ?DynamicFile

# Client configuration
# Send logs to central server
*.* @@logserver:514

# Restart rsyslog
sudo systemctl restart rsyslog
```

#### ELK Stack (Elasticsearch, Logstash, Kibana)

```bash
# Install Elasticsearch
curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elastic.gpg
echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt update && sudo apt install elasticsearch

# Install Logstash
sudo apt install logstash

# Install Kibana
sudo apt install kibana

# Logstash configuration (/etc/logstash/conf.d/apache.conf)
input {
  file {
    path => "/var/log/apache2/access.log"
    start_position => "beginning"
  }
}

filter {
  grok {
    match => { "message" => "%{COMBINEDAPACHELOG}" }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
  }
}
```

### Performance Optimization

#### System Tuning

```bash
# CPU optimization
# Set CPU governor to performance
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Memory optimization (/etc/sysctl.conf)
vm.swappiness=10                        # Reduce swap usage
vm.vfs_cache_pressure=50               # Keep more cache
vm.dirty_ratio=15                       # Dirty memory threshold
vm.dirty_background_ratio=5             # Background dirty memory

# Network optimization
net.core.rmem_max = 16777216           # Max receive buffer
net.core.wmem_max = 16777216           # Max send buffer
net.core.netdev_max_backlog = 5000     # Network device backlog
net.ipv4.tcp_congestion_control = bbr  # BBR congestion control

# Apply changes
sudo sysctl -p
```

#### Application Performance Tuning

```bash
# Database optimization (MySQL/MariaDB)
# Configuration (/etc/mysql/my.cnf)
[mysqld]
innodb_buffer_pool_size = 1G           # InnoDB buffer pool
query_cache_size = 256M                 # Query cache
max_connections = 200                   # Maximum connections
slow_query_log = 1                      # Enable slow query log

# Web server optimization (Apache)
# Configuration (/etc/apache2/apache2.conf)
MaxRequestWorkers 400                   # Maximum worker processes
ThreadsPerChild 25                      # Threads per child process
ServerLimit 16                          # Maximum server processes

# Enable compression
LoadModule deflate_module modules/mod_deflate.so
<Location />
    SetOutputFilter DEFLATE
</Location>
```

#### Storage Performance Optimization

```bash
# I/O scheduler optimization
# For SSDs
echo noop | sudo tee /sys/block/sda/queue/scheduler

# For HDDs
echo deadline | sudo tee /sys/block/sda/queue/scheduler

# File system optimization
# Mount options for performance
/dev/sda1 / ext4 defaults,noatime,data=writeback 0 1

# SSD optimization
sudo fstrim -v /                        # Manual TRIM
sudo systemctl enable fstrim.timer      # Automatic TRIM
```

### Alerting and Notification

#### Email Alerting Setup

```bash
# Configure mail server (Postfix)
sudo apt install postfix mailutils

# Test email functionality
echo "Test message" | mail -s "Test Subject" admin@company.com

# Nagios email notifications (/etc/nagios4/objects/contacts.cfg)
define contact {
    contact_name                    admin
    use                            generic-contact
    alias                          System Administrator
    email                          admin@company.com
    service_notification_period    24x7
    host_notification_period       24x7
    service_notification_options   w,u,c,r
    host_notification_options      d,u,r
}
```

#### Slack Integration

```bash
# Nagios Slack notification script
#!/bin/bash
# slack-notify.sh

SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
HOSTNAME="$1"
SERVICE="$2"
STATE="$3"
OUTPUT="$4"

PAYLOAD="payload={\"channel\": \"#alerts\", \"username\": \"nagios\", \"text\": \"$HOSTNAME - $SERVICE is $STATE: $OUTPUT\"}"

curl -X POST --data-urlencode "$PAYLOAD" $SLACK_WEBHOOK
```

### XP Tasks - Monitoring & Performance

- [ ] Set up system resource monitoring with built-in tools
- [ ] Configure log rotation and centralized logging
- [ ] Install and configure a monitoring system (Nagios/Zabbix)
- [ ] Create performance baseline measurements
- [ ] Set up alerting for critical system events
- [ ] Optimize system performance parameters
- [ ] Implement automated performance reporting

---

## Module 8: Backup and Disaster Recovery

### Backup Strategy and Planning

#### Backup Types and Methods

```bash
# Backup types:
# Full backup - Complete copy of all data
# Incremental backup - Changes since last backup
# Differential backup - Changes since last full backup
# Snapshot backup - Point-in-time copy

# 3-2-1 Backup Rule:
# 3 copies of important data
# 2 different types of media
# 1 offsite copy
```

#### Backup Planning Considerations

- **Recovery Time Objective (RTO)**: Maximum acceptable downtime
- **Recovery Point Objective (RPO)**: Maximum acceptable data loss
- **Retention Policy**: How long to keep backups
- **Testing**: Regular restore testing
- **Documentation**: Backup and recovery procedures

### File-Level Backup Solutions

#### rsync Backups

```bash
# Basic rsync backup
rsync -av /source/ /backup/              # Archive mode, verbose

# Incremental backup with hard links
rsync -av --link-dest=/backup/previous /source/ /backup/current/

# Remote backup via SSH
rsync -av -e ssh /source/ user@server:/backup/

# Exclude files and directories
rsync -av --exclude='*.tmp' --exclude-from=exclude.txt /source/ /backup/

# Advanced rsync script
#!/bin/bash
SOURCE="/home/"
DEST="/backup/home/"
DATE=$(date +%Y%m%d_%H%M%S)
LATEST="$DEST/latest"
CURRENT="$DEST/$DATE"

# Create backup directory
mkdir -p "$CURRENT"

# Perform backup with hard links to previous backup
if [ -d "$LATEST" ]; then
    rsync -av --delete --link-dest="$LATEST" "$SOURCE" "$CURRENT"
else
    rsync -av --delete "$SOURCE" "$CURRENT"
fi

# Update latest link
rm -f "$LATEST"
ln -s "$CURRENT" "$LATEST"

# Clean old backups (keep 7 days)
find "$DEST" -maxdepth 1 -type d -name "20*" -mtime +7 -exec rm -rf {} \;
```

#### tar-based Backups

```bash
# Create compressed archive
tar -czf backup-$(date +%Y%m%d).tar.gz /home/

# Create archive with exclusions
tar --exclude='*.tmp' --exclude='/home/*/cache' -czf backup.tar.gz /home/

# Incremental backup with tar
tar -czf full-backup.tar.gz /home/
tar -czf incr-backup.tar.gz --newer-mtime="2021-01-01" /home/

# List archive contents
tar -tzf backup.tar.gz

# Extract archive
tar -xzf backup.tar.gz -C /restore/
```

### System-Level Backup Solutions

#### Disk Image Backups

```bash
# Full disk imaging with dd
sudo dd if=/dev/sda of=/backup/disk.img bs=4M status=progress

# Compressed disk image
sudo dd if=/dev/sda bs=4M status=progress | gzip > /backup/disk.img.gz

# Restore from image
sudo dd if=/backup/disk.img of=/dev/sdb bs=4M status=progress

# Partition table backup
sudo sfdisk -d /dev/sda > /backup/partition-table.txt
# Restore partition table
sudo sfdisk /dev/sda < /backup/partition-table.txt
```

#### LVM Snapshots

```bash
# Create LVM snapshot
sudo lvcreate -L 5G -s -n backup-snap /dev/vg0/root

# Mount snapshot
sudo mkdir /mnt/snapshot
sudo mount /dev/vg0/backup-snap /mnt/snapshot

# Backup from snapshot
tar -czf /backup/system-backup.tar.gz -C /mnt/snapshot .

# Remove snapshot
sudo umount /mnt/snapshot
sudo lvremove /dev/vg0/backup-snap
```

#### BTRFS Snapshots

```bash
# Create BTRFS snapshot
sudo btrfs subvolume snapshot /home /home/.snapshots/$(date +%Y%m%d_%H%M%S)

# List snapshots
sudo btrfs subvolume list /home

# Delete old snapshots
sudo btrfs subvolume delete /home/.snapshots/old_snapshot

# Send/receive for backup
sudo btrfs send /home/.snapshots/snapshot1 | ssh user@backup-server "sudo btrfs receive /backup/"
```

### Database Backup Solutions

#### MySQL/MariaDB Backups

```bash
# Full database dump
mysqldump -u root -p --all-databases > full-backup.sql
mysqldump -u root -p database_name > database-backup.sql

# Backup with binary logs for point-in-time recovery
mysqldump -u root -p --single-transaction --routines --triggers --all-databases > backup.sql

# Automated backup script
#!/bin/bash
DB_USER="backup_user"
DB_PASS="backup_password"
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Dump all databases
mysqldump -u "$DB_USER" -p"$DB_PASS" --single-transaction --routines --triggers --all-databases | gzip > "$BACKUP_DIR/mysql-backup-$DATE.sql.gz"

# Keep only 7 days of backups
find "$BACKUP_DIR" -name "mysql-backup-*.sql.gz" -mtime +7 -delete

# Backup binary logs
mysqlbinlog /var/log/mysql/mysql-bin.* | gzip > "$BACKUP_DIR/binlog-backup-$DATE.gz"
```

#### PostgreSQL Backups

```bash
# Database dump
pg_dump -U postgres database_name > database-backup.sql
pg_dumpall -U postgres > full-backup.sql

# Custom format dump
pg_dump -U postgres -Fc database_name > database-backup.dump

# Backup with WAL archiving
# postgresql.conf settings:
# wal_level = archive
# archive_mode = on
# archive_command = 'cp %p /backup/postgres/wal/%f'

# Base backup
pg_basebackup -U postgres -D /backup/postgres/base -Ft -z -P
```

### Automated Backup Systems

#### Bacula Configuration

```bash
# Install Bacula
sudo apt install bacula-server bacula-client

# Bacula Director configuration (/etc/bacula/bacula-dir.conf)
Director {
  Name = bacula-dir
  DIRport = 9101
  QueryFile = "/etc/bacula/scripts/query.sql"
  WorkingDirectory = "/var/lib/bacula"
  PidDirectory = "/var/run/bacula"
  Password = "console_password"
  Messages = Daemon
}

# File Daemon configuration (/etc/bacula/bacula-fd.conf)
FileDaemon {
  Name = client1-fd
  FDport = 9102
  WorkingDirectory = /var/lib/bacula
  Pid Directory = /var/run/bacula
  Maximum Concurrent Jobs = 20
}

# Job definition
Job {
  Name = "BackupClient1"
  Type = Backup
  Level = Incremental
  Client = client1-fd
  FileSet = "Full Set"
  Schedule = "WeeklyCycle"
  Storage = File
  Messages = Standard
  Pool = File
  Priority = 10
  Write Bootstrap = "/var/lib/bacula/%c.bsr"
}
```

#### Amanda Backup System

```bash
# Install Amanda
sudo apt install amanda-server amanda-client

# Amanda configuration (/etc/amanda/DailySet1/amanda.conf)
org "DailySet1"
mailto "admin@company.com"
dumpuser "backup"
tapecycle 7 tapes
runspercycle 1 day
tapetype HARDDISK
holdingdisk hd1 {
    comment "main holding disk"
    directory "/var/lib/amanda/holdings"
    use 1000 Mb
}

# Disk list (/etc/amanda/DailySet1/disklist)
client1.company.com /home comp-user-tar
client1.company.com /etc comp-root-tar
```

### Cloud Backup Solutions

#### AWS S3 Backup

```bash
# Install AWS CLI
sudo apt install awscli

# Configure AWS credentials
aws configure

# Sync to S3
aws s3 sync /backup/ s3://my-backup-bucket/

# Automated S3 backup script
#!/bin/bash
SOURCE="/home/"
S3_BUCKET="s3://my-backup-bucket"
DATE=$(date +%Y%m%d)

# Create local backup
tar -czf /tmp/backup-$DATE.tar.gz "$SOURCE"

# Upload to S3
aws s3 cp /tmp/backup-$DATE.tar.gz "$S3_BUCKET/"

# Clean up local file
rm /tmp/backup-$DATE.tar.gz

# Remove old backups from S3 (keep 30 days)
aws s3 ls "$S3_BUCKET/" | while read -r line; do
    createDate=`echo $line|awk {'print $1" "$2'}`
    createDate=`date -d"$createDate" +%s`
    olderThan=`date -d"30 days ago" +%s`
    if [[ $createDate -lt $olderThan ]]
    then
        fileName=`echo $line|awk {'print $4'}`
        if [[ $fileName != "" ]]
        then
            aws s3 rm "$S3_BUCKET/$fileName"
        fi
    fi
done
```

#### Google Cloud Storage Backup

```bash
# Install gsutil
curl https://sdk.cloud.google.com | bash

# Authenticate
gcloud auth login

# Sync to Google Cloud Storage
gsutil -m rsync -r -d /backup/ gs://my-backup-bucket/

# Automated backup with lifecycle management
gsutil lifecycle set lifecycle.json gs://my-backup-bucket/

# lifecycle.json
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {"age": 30}
      }
    ]
  }
}
```

### Disaster Recovery Planning

#### Business Continuity Planning

```bash
# Disaster Recovery Plan Components:
# 1. Risk Assessment
# 2. Business Impact Analysis
# 3. Recovery Strategies
# 4. Emergency Response Procedures
# 5. Testing and Maintenance

# Recovery Site Types:
# Hot Site - Fully operational backup facility
# Warm Site - Partially equipped facility
# Cold Site - Basic facility with no equipment
```

#### System Recovery Procedures

```bash
# Bare metal recovery preparation
# 1. Document hardware configuration
lshw > hardware-config.txt
lscpu > cpu-info.txt
lsblk > disk-layout.txt
ip addr show > network-config.txt

# 2. Create system rescue media
# Download SystemRescueCD or similar
# Create bootable USB with dd or similar tool

# 3. Document recovery procedures
# - Boot from rescue media
# - Restore partition table
# - Format filesystems
# - Restore data from backup
# - Reinstall bootloader
# - Test system functionality
```

### Backup Testing and Verification

#### Automated Backup Testing

```bash
#!/bin/bash
# Backup verification script

BACKUP_DIR="/backup"
TEST_DIR="/tmp/restore_test"
LOG_FILE="/var/log/backup_test.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

test_backup() {
    local backup_file=$1
    local test_dir="$TEST_DIR/$(basename "$backup_file" .tar.gz)"
    
    log "Testing backup: $backup_file"
    
    # Create test directory
    mkdir -p "$test_dir"
    
    # Extract backup
    if tar -xzf "$backup_file" -C "$test_dir"; then
        log "✓ Backup extraction successful"
    else
        log "✗ Backup extraction failed"
        return 1
    fi
    
    # Verify critical files
    critical_files=("/etc/passwd" "/etc/group" "/etc/fstab")
    for file in "${critical_files[@]}"; do
        if [ -f "$test_dir$file" ]; then
            log "✓ Critical file found: $file"
        else
            log "✗ Critical file missing: $file"
            return 1
        fi
    done
    
    # Clean up
    rm -rf "$test_dir"
    log "✓ Backup test completed successfully"
}

# Test all backup files
for backup in "$BACKUP_DIR"/*.tar.gz; do
    if [ -f "$backup" ]; then
        test_backup "$backup"
    fi
done
```

#### Database Backup Verification

```bash
#!/bin/bash
# MySQL backup verification script

BACKUP_FILE=$1
TEST_DB="backup_test_$(date +%s)"
MYSQL_USER="root"
MYSQL_PASS="password"

# Create test database
mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -e "CREATE DATABASE $TEST_DB;"

# Restore backup to test database
if mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" "$TEST_DB" < "$BACKUP_FILE"; then
    echo "✓ Backup restoration successful"
    
    # Verify table count
    table_count=$(mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$TEST_DB';")
    echo "✓ Restored $table_count tables"
    
    # Clean up test database
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -e "DROP DATABASE $TEST_DB;"
    echo "✓ Backup verification completed"
else
    echo "✗ Backup restoration failed"
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -e "DROP DATABASE IF EXISTS $TEST_DB;"
    exit 1
fi
```

### XP Tasks - Backup & Disaster Recovery

- [ ] Design a comprehensive backup strategy for a system
- [ ] Implement automated file-level backups with rsync
- [ ] Set up database backup automation
- [ ] Create and test system recovery procedures
- [ ] Configure cloud backup integration
- [ ] Develop backup verification and testing scripts
- [ ] Document disaster recovery procedures

---

## Module 9: Automation and Infrastructure as Code

### Automation Fundamentals

#### Benefits of Automation

- **Consistency**: Identical deployments every time
- **Speed**: Faster deployment and configuration
- **Reliability**: Reduced human error
- **Scalability**: Handle large-scale operations
- **Auditability**: Track changes and compliance
- **Cost Efficiency**: Reduce manual labor

#### Automation Tools Overview

```bash
# Configuration Management:
# - Ansible (Agentless, YAML-based)
# - Puppet (Agent-based, DSL)
# - Chef (Agent-based, Ruby DSL)
# - SaltStack (Agent-based, YAML/Python)

# Infrastructure as Code:
# - Terraform (Multi-cloud provisioning)
# - CloudFormation (AWS-specific)
# - Pulumi (Multiple languages)

# Orchestration:
# - Kubernetes (Container orchestration)
# - Docker Swarm (Container clustering)
# - Nomad (Workload orchestration)
```

### Ansible Configuration Management

#### Ansible Installation and Setup

```bash
# Install Ansible
sudo apt update
sudo apt install ansible

# Verify installation
ansible --version

# Create project structure
mkdir -p ansible-project/{playbooks,inventory,roles,group_vars,host_vars}
cd ansible-project

# Inventory file (inventory/hosts)
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[databases]
db1 ansible_host=192.168.1.20

[all:vars]
ansible_user=admin
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

#### Basic Ansible Playbooks

```yaml
# playbooks/webserver.yml
---
- name: Configure Web Servers
  hosts: webservers
  become: yes
  vars:
    apache_port: 80
    document_root: /var/www/html
  
  tasks:
    - name: Update package cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install Apache
      apt:
        name: apache2
        state: present
    
    - name: Start and enable Apache
      systemd:
        name: apache2
        state: started
        enabled: yes
    
    - name: Configure Apache virtual host
      template:
        src: vhost.conf.j2
        dest: /etc/apache2/sites-available/000-default.conf
      notify: restart apache
    
    - name: Create web content
      copy:
        content: |
          <html>
          <head><title>Welcome</title></head>
          <body><h1>Hello from {{ ansible_hostname }}</h1></body>
          </html>
        dest: "{{ document_root }}/index.html"
  
  handlers:
    - name: restart apache
      systemd:
        name: apache2
        state: restarted
```

#### Ansible Roles

```bash
# Create role structure
ansible-galaxy init roles/common

# roles/common/tasks/main.yml
---
- name: Update system packages
  apt:
    update_cache: yes
    upgrade: dist
  when: ansible_os_family == "Debian"

- name: Install essential packages
  package:
    name:
      - vim
      - htop
      - curl
      - wget
      - unzip
    state: present

- name: Configure timezone
  timezone:
    name: "{{ system_timezone | default('UTC') }}"

- name: Create admin user
  user:
    name: "{{ admin_user }}"
    groups: sudo
    shell: /bin/bash
    create_home: yes
  when: admin_user is defined

- name: Configure SSH key for admin user
  authorized_key:
    user: "{{ admin_user }}"
    key: "{{ admin_ssh_key }}"
  when: admin_user is defined and admin_ssh_key is defined
```

#### Advanced Ansible Features

```yaml
# playbooks/lamp-stack.yml
---
- name: Deploy LAMP Stack
  hosts: webservers
  become: yes
  vars_files:
    - vars/mysql.yml
  
  pre_tasks:
    - name: Update package cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
  
  roles:
    - common
    - apache
    - mysql
    - php
  
  post_tasks:
    - name: Verify web service
      uri:
        url: "http://{{ ansible_default_ipv4.address }}"
        status_code: 200
      delegate_to: localhost

# Using vault for sensitive data
# ansible-vault create vars/mysql.yml
mysql_root_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66386439653637343...

# Run playbook with vault
ansible-playbook -i inventory/hosts playbooks/lamp-stack.yml --ask-vault-pass
```

### Docker Containerization

#### Docker Basics

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Basic Docker commands
docker --version
docker pull nginx
docker run -d -p 80:80 --name webserver nginx
docker ps
docker logs webserver
docker exec -it webserver bash
docker stop webserver
docker rm webserver
```

#### Dockerfile Creation

```dockerfile
# Dockerfile for custom web application
FROM ubuntu:20.04

# Set maintainer
LABEL maintainer="admin@company.com"

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Update and install packages
RUN apt-get update && apt-get install -y \
    apache2 \
    php \
    libapache2-mod-php \
    php-mysql \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY src/ /var/www/html/

# Configure Apache
RUN echo 'ServerName localhost' >> /etc/apache2/apache2.conf
RUN a2enmod rewrite

# Set permissions
RUN chown -R www-data:www-data /var/www/html/
RUN chmod -R 755 /var/www/html/

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start Apache
CMD ["apache2ctl", "-D", "FOREGROUND"]
```

#### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
    volumes:
      - ./src:/var/www/html
    depends_on:
      - db
    environment:
      - DB_HOST=db
      - DB_NAME=webapp
      - DB_USER=webuser
      - DB_PASS=password
    networks:
      - webapp-network

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: webapp
      MYSQL_USER: webuser
      MYSQL_PASSWORD: password
    volumes:
      - db-data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - webapp-network

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    ports:
      - "8080:80"
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: rootpassword
    depends_on:
      - db
    networks:
      - webapp-network

volumes:
  db-data:

networks:
  webapp-network:
    driver: bridge

# Deploy application
docker-compose up -d
docker-compose ps
docker-compose logs
docker-compose down
```

### Terraform Infrastructure as Code

#### Terraform Basics

```bash
# Install Terraform
wget https://releases.hashicorp.com/terraform/1.0.0/terraform_1.0.0_linux_amd64.zip
unzip terraform_1.0.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify installation
terraform --version
```

#### Basic Terraform Configuration

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

# Data sources
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

# Resources
resource "aws_security_group" "web" {
  name_prefix = "web-sg"
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  count                  = 2
  ami                   = data.aws_ami.ubuntu.id
  instance_type         = var.instance_type
  vpc_security_group_ids = [aws_security_group.web.id]
  
  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y apache2
    systemctl start apache2
    systemctl enable apache2
    echo "<h1>Web Server ${count.index + 1}</h1>" > /var/www/html/index.html
  EOF
  
  tags = {
    Name = "web-server-${count.index + 1}"
  }
}

# Outputs
output "instance_ips" {
  description = "Public IP addresses of web servers"
  value       = aws_instance.web[*].public_ip
}
```

#### Terraform Workflow

```bash
# Initialize Terraform
terraform init

# Plan infrastructure changes
terraform plan

# Apply changes
terraform apply

# Show current state
terraform show

# Destroy infrastructure
terraform destroy
```

### CI/CD Pipeline Integration

#### GitLab CI/CD Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy
  - cleanup

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  ANSIBLE_HOST_KEY_CHECKING: "False"

before_script:
  - docker info
  - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY

build:
  stage: build
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main
    - develop

test:
  stage: test
  script:
    - docker run --rm $DOCKER_IMAGE ./run-tests.sh
  only:
    - main
    - develop

deploy_staging:
  stage: deploy
  script:
    - ansible-playbook -i inventory/staging playbooks/deploy.yml
      --extra-vars "docker_image=$DOCKER_IMAGE"
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy_production:
  stage: deploy
  script:
    - ansible-playbook -i inventory/production playbooks/deploy.yml
      --extra-vars "docker_image=$DOCKER_IMAGE"
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - main

cleanup:
  stage: cleanup
  script:
    - docker system prune -f
  when: always
```

### Monitoring and Alerting Automation

#### Automated Monitoring Setup

```yaml
# playbooks/monitoring.yml
---
- name: Setup Monitoring Stack
  hosts: monitoring
  become: yes
  vars:
    prometheus_version: "2.30.3"
    grafana_version: "8.2.0"
  
  tasks:
    - name: Create monitoring user
      user:
        name: monitoring
        system: yes
        shell: /bin/false
        home: /var/lib/monitoring
    
    - name: Install Prometheus
      unarchive:
        src: "https://github.com/prometheus/prometheus/releases/download/v{{ prometheus_version }}/prometheus-{{ prometheus_version }}.linux-amd64.tar.gz"
        dest: /opt
        remote_src: yes
        owner: monitoring
        group: monitoring
        mode: '0755'
    
    - name: Create Prometheus configuration
      template:
        src: prometheus.yml.j2
        dest: /etc/prometheus/prometheus.yml
        owner: monitoring
        group: monitoring
        mode: '0644'
      notify: restart prometheus
    
    - name: Create Prometheus systemd service
      template:
        src: prometheus.service.j2
        dest: /etc/systemd/system/prometheus.service
      notify:
        - reload systemd
        - restart prometheus
    
    - name: Install and configure Grafana
      apt:
        deb: "https://dl.grafana.com/oss/release/grafana_{{ grafana_version }}_amd64.deb"
      notify: restart grafana
  
  handlers:
    - name: reload systemd
      systemd:
        daemon_reload: yes
    
    - name: restart prometheus
      systemd:
        name: prometheus
        state: restarted
        enabled: yes
    
    - name: restart grafana
      systemd:
        name: grafana-server
        state: restarted
        enabled: yes
```

### XP Tasks - Automation & IaC

- [ ] Create an Ansible playbook to configure a web server
- [ ] Build a Docker container for a simple application
- [ ] Set up Docker Compose for multi-service application
- [ ] Write Terraform configuration for cloud infrastructure
- [ ] Implement CI/CD pipeline with automated testing
- [ ] Create automated monitoring and alerting setup
- [ ] Develop infrastructure automation for disaster recovery

---

## Module 10: Capstone Project - Complete System Administration Environment

### Project Overview

Build a comprehensive system administration environment that demonstrates mastery of all core concepts. This project will create a complete infrastructure with web services, databases, monitoring, backup, and automation.

#### Project Requirements

**Core Infrastructure:**

1. **Multi-tier Web Application** (Web, App, Database layers)
2. **Load Balancing and High Availability**
3. **Centralized Monitoring and Logging**
4. **Automated Backup and Recovery**
5. **Security Implementation**
6. **Infrastructure as Code**
7. **CI/CD Pipeline**
8. **Documentation and Procedures**

### Implementation Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │  Monitoring     │
│   (HAProxy)     │    │  (Prometheus)   │
└─────────┬───────┘    └─────────────────┘
          │
    ┌─────┴─────┐
    │           │
┌───▼────┐ ┌───▼────┐    ┌─────────────────┐
│Web-01  │ │Web-02  │    │  Log Server     │
│(Apache)│ │(Apache)│    │  (ELK Stack)    │
└───┬────┘ └───┬────┘    └─────────────────┘
    │          │
    └─────┬────┘
          │
    ┌─────▼─────┐         ┌─────────────────┐
    │  App-01   │         │  Backup Server  │
    │ (Python)  │         │  (Bacula)       │
    └─────┬─────┘         └─────────────────┘
          │
    ┌─────▼─────┐
    │   DB-01   │
    │  (MySQL)  │
    └───────────┘
```

### Phase 1: Infrastructure Setup

#### Terraform Infrastructure Provisioning

```hcl
# infrastructure/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  
  backend "s3" {
    bucket = "sysadmin-terraform-state"
    key    = "infrastructure/terraform.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC and Networking
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "sysadmin-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = {
    Terraform = "true"
    Environment = var.environment
  }
}

# Security Groups
resource "aws_security_group" "web" {
  name_prefix = "web-sg"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Launch Template
resource "aws_launch_template" "web" {
  name_prefix   = "web-template"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  
  vpc_security_group_ids = [aws_security_group.web.id]
  
  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    environment = var.environment
  }))
  
  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "web-server"
      Environment = var.environment
    }
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "web" {
  name               = "web-asg"
  vpc_zone_identifier = module.vpc.public_subnets
  target_group_arns   = [aws_lb_target_group.web.arn]
  health_check_type   = "ELB"
  
  min_size         = 2
  max_size         = 4
  desired_capacity = 2
  
  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }
}

# Application Load Balancer
resource "aws_lb" "web" {
  name               = "web-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web.id]
  subnets            = module.vpc.public_subnets
  
  enable_deletion_protection = false
}

resource "aws_lb_target_group" "web" {
  name     = "web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher            = "200"
    path               = "/health"
    port               = "traffic-port"
    protocol           = "HTTP"
    timeout            = 5
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "web" {
  load_balancer_arn = aws_lb.web.arn
  port              = "80"
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}
```

### Phase 2: Configuration Management

#### Ansible Inventory and Configuration

```ini
# inventory/production
[load_balancers]
lb-01 ansible_host=10.0.101.10

[web_servers]
web-01 ansible_host=10.0.101.11
web-02 ansible_host=10.0.101.12

[app_servers]
app-01 ansible_host=10.0.1.10

[databases]
db-01 ansible_host=10.0.1.11

[monitoring]
monitor-01 ansible_host=10.0.1.20

[logging]
log-01 ansible_host=10.0.1.21

[backup]
backup-01 ansible_host=10.0.1.22

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/sysadmin-key.pem
```

#### Complete Application Deployment Playbook

```yaml
# playbooks/deploy_application.yml
---
- name: Deploy Complete Application Stack
  hosts: all
  become: yes
  gather_facts: yes
  
  pre_tasks:
    - name: Update package cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install common packages
      apt:
        name:
          - htop
          - vim
          - curl
          - wget
          - unzip
          - ntp
        state: present

- name: Configure Load Balancer
  hosts: load_balancers
  become: yes
  roles:
    - haproxy
  vars:
    haproxy_backend_servers:
      - name: web-01
        address: "{{ hostvars['web-01']['ansible_default_ipv4']['address'] }}:80"
      - name: web-02
        address: "{{ hostvars['web-02']['ansible_default_ipv4']['address'] }}:80"

- name: Configure Web Servers
  hosts: web_servers
  become: yes
  roles:
    - apache
    - php
    - filebeat
  vars:
    apache_document_root: /var/www/html
    php_version: "7.4"

- name: Configure Application Servers
  hosts: app_servers
  become: yes
  roles:
    - python
    - gunicorn
    - filebeat
  vars:
    app_directory: /opt/webapp
    python_version: "3.9"

- name: Configure Database Servers
  hosts: databases
  become: yes
  roles:
    - mysql
    - filebeat
  vars:
    mysql_root_password: "{{ vault_mysql_root_password }}"
    mysql_databases:
      - name: webapp
        collation: utf8_general_ci
        encoding: utf8
    mysql_users:
      - name: webapp_user
        password: "{{ vault_mysql_webapp_password }}"
        priv: "webapp.*:ALL"

- name: Configure Monitoring
  hosts: monitoring
  become: yes
  roles:
    - prometheus
    - grafana
    - alertmanager
  vars:
    prometheus_targets:
      - job_name: 'web-servers'
        static_configs:
          - targets: 
            - "{{ hostvars['web-01']['ansible_default_ipv4']['address'] }}:9100"
            - "{{ hostvars['web-02']['ansible_default_ipv4']['address'] }}:9100"

- name: Configure Logging
  hosts: logging
  become: yes
  roles:
    - elasticsearch
    - logstash
    - kibana

- name: Configure Backup
  hosts: backup
  become: yes
  roles:
    - bacula-director
    - bacula-storage
  vars:
    backup_clients:
      - name: web-01
        address: "{{ hostvars['web-01']['ansible_default_ipv4']['address'] }}"
      - name: web-02
        address: "{{ hostvars['web-02']['ansible_default_ipv4']['address'] }}"
      - name: db-01
        address: "{{ hostvars['db-01']['ansible_default_ipv4']['address'] }}"
```

### Phase 3: Application Code and CI/CD

#### Sample Application (Flask)

```python
# app/app.py
from flask import Flask, request, jsonify, render_template
import mysql.connector
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'webapp_user'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'database': os.environ.get('DB_NAME', 'webapp')
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        logger.error(f"Database connection error: {e}")
        return None

@app.route('/health') def health_check(): """Health check endpoint for load balancer""" try: connection = get_db_connection() if connection: connection.close() return jsonify({ 'status': 'healthy', 'timestamp': datetime.now().isoformat(), 'database': 'connected' }), 200 else: return jsonify({ 'status': 'unhealthy', 'timestamp': datetime.now().isoformat(), 'database': 'disconnected' }), 503 except Exception as e: logger.error(f"Health check failed: {e}") return jsonify({ 'status': 'unhealthy', 'timestamp': datetime.now().isoformat(), 'error': str(e) }), 503

@app.route('/') def index(): """Main application page""" return render_template('index.html')

@app.route('/api/users', methods=['GET']) def get_users(): """Get all users""" connection = get_db_connection() if not connection: return jsonify({'error': 'Database connection failed'}), 500

```
try:
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email, created_at FROM users")
    users = cursor.fetchall()
    return jsonify(users)
except Exception as e:
    logger.error(f"Error fetching users: {e}")
    return jsonify({'error': 'Internal server error'}), 500
finally:
    cursor.close()
    connection.close()
```

@app.route('/api/users', methods=['POST']) def create_user(): """Create a new user""" data = request.get_json() if not data or 'username' not in data or 'email' not in data: return jsonify({'error': 'Username and email are required'}), 400

```
connection = get_db_connection()
if not connection:
    return jsonify({'error': 'Database connection failed'}), 500

try:
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (username, email) VALUES (%s, %s)",
        (data['username'], data['email'])
    )
    connection.commit()
    return jsonify({
        'message': 'User created successfully',
        'user_id': cursor.lastrowid
    }), 201
except mysql.connector.IntegrityError:
    return jsonify({'error': 'Username or email already exists'}), 409
except Exception as e:
    logger.error(f"Error creating user: {e}")
    return jsonify({'error': 'Internal server error'}), 500
finally:
    cursor.close()
    connection.close()
```

if **name** == '**main**': app.run(host='0.0.0.0', port=5000, debug=False)

````

#### CI/CD Pipeline Configuration
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - security_scan
  - deploy_staging
  - integration_tests
  - deploy_production
  - post_deployment

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  STAGING_ENVIRONMENT: "staging"
  PRODUCTION_ENVIRONMENT: "production"

# Test Stage
unit_tests:
  stage: test
  image: python:3.9
  services:
    - mysql:8.0
  variables:
    MYSQL_ROOT_PASSWORD: testpassword
    MYSQL_DATABASE: webapp_test
    DB_HOST: mysql
    DB_USER: root
    DB_PASSWORD: testpassword
    DB_NAME: webapp_test
  before_script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
  script:
    - python -m pytest tests/ --cov=app --cov-report=xml
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
  only:
    - merge_requests
    - main
    - develop

lint_code:
  stage: test
  image: python:3.9
  before_script:
    - pip install flake8 black isort
  script:
    - flake8 app/ tests/
    - black --check app/ tests/
    - isort --check-only app/ tests/
  only:
    - merge_requests
    - main
    - develop

# Build Stage
build_docker_image:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main
    - develop

# Security Scanning
security_scan:
  stage: security_scan
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - apk add --no-cache curl
    - curl -sSfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
  script:
    - trivy image --exit-code 0 --severity HIGH,CRITICAL $DOCKER_IMAGE
  only:
    - main
    - develop

# Staging Deployment
deploy_staging:
  stage: deploy_staging
  image: alpine:latest
  before_script:
    - apk add --no-cache ansible openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
  script:
    - ansible-playbook -i inventory/staging playbooks/deploy.yml
      --extra-vars "docker_image=$DOCKER_IMAGE environment=$STAGING_ENVIRONMENT"
  environment:
    name: staging
    url: https://staging.sysadmin-project.com
  only:
    - develop

# Integration Tests
integration_tests:
  stage: integration_tests
  image: alpine:latest
  before_script:
    - apk add --no-cache curl jq
  script:
    - ./scripts/integration_tests.sh staging.sysadmin-project.com
  dependencies:
    - deploy_staging
  only:
    - develop

# Production Deployment
deploy_production:
  stage: deploy_production
  image: alpine:latest
  before_script:
    - apk add --no-cache ansible openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
  script:
    - ansible-playbook -i inventory/production playbooks/deploy.yml
      --extra-vars "docker_image=$DOCKER_IMAGE environment=$PRODUCTION_ENVIRONMENT"
  environment:
    name: production
    url: https://sysadmin-project.com
  when: manual
  only:
    - main

# Post Deployment
smoke_tests:
  stage: post_deployment
  image: alpine:latest
  before_script:
    - apk add --no-cache curl jq
  script:
    - ./scripts/smoke_tests.sh sysadmin-project.com
  dependencies:
    - deploy_production
  only:
    - main

notify_deployment:
  stage: post_deployment
  image: alpine:latest
  before_script:
    - apk add --no-cache curl
  script:
    - |
      curl -X POST -H 'Content-type: application/json' \
      --data '{"text":"🚀 Deployment completed successfully for commit '$CI_COMMIT_SHORT_SHA'"}' \
      $SLACK_WEBHOOK_URL
  dependencies:
    - deploy_production
  when: on_success
  only:
    - main
````

### Phase 4: Monitoring and Alerting

#### Comprehensive Monitoring Configuration

```yaml
# roles/prometheus/templates/prometheus.yml.j2
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets:
{% for host in groups['all'] %}
        - '{{ hostvars[host]['ansible_default_ipv4']['address'] }}:9100'
{% endfor %}

  - job_name: 'application'
    static_configs:
      - targets:
{% for host in groups['app_servers'] %}
        - '{{ hostvars[host]['ansible_default_ipv4']['address'] }}:5000'
{% endfor %}
    metrics_path: '/metrics'

  - job_name: 'mysql-exporter'
    static_configs:
      - targets:
{% for host in groups['databases'] %}
        - '{{ hostvars[host]['ansible_default_ipv4']['address'] }}:9104'
{% endfor %}

  - job_name: 'apache-exporter'
    static_configs:
      - targets:
{% for host in groups['web_servers'] %}
        - '{{ hostvars[host]['ansible_default_ipv4']['address'] }}:9117'
{% endfor %}

  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
        - https://sysadmin-project.com
        - https://staging.sysadmin-project.com
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter:9115
```

#### Alert Rules Configuration

```yaml
# roles/prometheus/files/alert_rules.yml
groups:
  - name: system_alerts
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is above 80% on {{ $labels.instance }}"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 85% on {{ $labels.instance }}"

      - alert: DiskSpaceWarning
        expr: (node_filesystem_avail_bytes{fstype!="tmpfs"} / node_filesystem_size_bytes{fstype!="tmpfs"}) * 100 < 15
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Low disk space warning"
          description: "Disk usage is above 85% on {{ $labels.instance }} mount {{ $labels.mountpoint }}"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.job }} on {{ $labels.instance }} has been down for more than 1 minute"

  - name: application_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(flask_http_request_exceptions_total[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High application error rate"
          description: "Application error rate is above 10% for the last 5 minutes"

      - alert: DatabaseConnectionFailure
        expr: mysql_up == 0
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: "Database connection failure"
          description: "Cannot connect to MySQL database on {{ $labels.instance }}"

      - alert: WebsiteDown
        expr: probe_success == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Website is down"
          description: "Website {{ $labels.instance }} is not responding"

  - name: infrastructure_alerts
    rules:
      - alert: LoadBalancerBackendDown
        expr: haproxy_server_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Load balancer backend is down"
          description: "Backend server {{ $labels.server }} in {{ $labels.backend }} is down"

      - alert: SSLCertificateExpiration
        expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 30
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "SSL certificate expiring soon"
          description: "SSL certificate for {{ $labels.instance }} expires in less than 30 days"
```

### Phase 5: Backup and Recovery

#### Comprehensive Backup Strategy

```bash
#!/bin/bash
# scripts/backup_manager.sh - Comprehensive backup management script

set -euo pipefail

# Configuration
BACKUP_ROOT="/backup"
LOG_FILE="/var/log/backup_manager.log"
RETENTION_DAYS=30
MYSQL_USER="backup_user"
MYSQL_PASS="$(cat /etc/mysql/backup_password)"
S3_BUCKET="sysadmin-project-backups"
NOTIFICATION_WEBHOOK="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"

# Functions
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

notify() {
    local message="$1"
    local color="${2:-good}"
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"attachments\":[{\"color\":\"$color\",\"text\":\"$message\"}]}" \
        "$NOTIFICATION_WEBHOOK" 2>/dev/null || true
}

backup_files() {
    local backup_name="$1"
    local source_path="$2"
    local backup_path="$BACKUP_ROOT/files/$backup_name"
    local date_suffix=$(date +%Y%m%d_%H%M%S)
    
    log "Starting file backup: $backup_name"
    
    mkdir -p "$backup_path"
    
    # Create incremental backup with rsync
    if rsync -av --delete --link-dest="$backup_path/latest" \
        "$source_path" "$backup_path/$date_suffix/"; then
        
        # Update latest link
        rm -f "$backup_path/latest"
        ln -s "$date_suffix" "$backup_path/latest"
        
        log "File backup completed successfully: $backup_name"
        return 0
    else
        log "File backup failed: $backup_name"
        return 1
    fi
}

backup_mysql() {
    local backup_path="$BACKUP_ROOT/mysql"
    local date_suffix=$(date +%Y%m%d_%H%M%S)
    
    log "Starting MySQL backup"
    
    mkdir -p "$backup_path"
    
    # Full database dump
    if mysqldump -u "$MYSQL_USER" -p"$MYSQL_PASS" \
        --single-transaction --routines --triggers --all-databases | \
        gzip > "$backup_path/mysql-full-$date_suffix.sql.gz"; then
        
        log "MySQL backup completed successfully"
        return 0
    else
        log "MySQL backup failed"
        return 1
    fi
}

backup_to_cloud() {
    local local_path="$1"
    local s3_path="$2"
    
    log "Starting cloud backup: $local_path -> $s3_path"
    
    if aws s3 sync "$local_path" "s3://$S3_BUCKET/$s3_path" --delete; then
        log "Cloud backup completed successfully"
        return 0
    else
        log "Cloud backup failed"
        return 1
    fi
}

cleanup_old_backups() {
    log "Cleaning up backups older than $RETENTION_DAYS days"
    
    # Clean local backups
    find "$BACKUP_ROOT" -type f -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
    find "$BACKUP_ROOT" -type f -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete
    find "$BACKUP_ROOT" -type d -name "20*" -mtime +$RETENTION_DAYS -exec rm -rf {} +
    
    log "Local backup cleanup completed"
}

verify_backups() {
    log "Starting backup verification"
    
    local failures=0
    
    # Verify file backups
    for backup_dir in "$BACKUP_ROOT"/files/*/latest; do
        if [ -d "$backup_dir" ]; then
            local backup_name=$(basename $(dirname "$backup_dir"))
            if [ -f "$backup_dir/etc/passwd" ] || [ -f "$backup_dir/var/www/html/index.html" ]; then
                log "✓ File backup verified: $backup_name"
            else
                log "✗ File backup verification failed: $backup_name"
                ((failures++))
            fi
        fi
    done
    
    # Verify MySQL backups
    local latest_mysql_backup=$(ls -t "$BACKUP_ROOT"/mysql/mysql-full-*.sql.gz 2>/dev/null | head -1)
    if [ -n "$latest_mysql_backup" ] && [ -f "$latest_mysql_backup" ]; then
        if zcat "$latest_mysql_backup" | head -20 | grep -q "MySQL dump"; then
            log "✓ MySQL backup verified"
        else
            log "✗ MySQL backup verification failed"
            ((failures++))
        fi
    else
        log "✗ No MySQL backup found"
        ((failures++))
    fi
    
    if [ $failures -eq 0 ]; then
        log "All backup verifications passed"
        return 0
    else
        log "$failures backup verification(s) failed"
        return 1
    fi
}

# Main backup execution
main() {
    log "Starting comprehensive backup process"
    notify "🔄 Starting backup process"
    
    local overall_success=true
    
    # File system backups
    backup_files "web_servers" "/var/www/" || overall_success=false
    backup_files "application" "/opt/webapp/" || overall_success=false
    backup_files "system_configs" "/etc/" || overall_success=false
    backup_files "log_files" "/var/log/" || overall_success=false
    
    # Database backups
    backup_mysql || overall_success=false
    
    # Cloud backup
    backup_to_cloud "$BACKUP_ROOT" "$(date +%Y/%m/%d)" || overall_success=false
    
    # Verification
    verify_backups || overall_success=false
    
    # Cleanup
    cleanup_old_backups
    
    # Final notification
    if [ "$overall_success" = true ]; then
        log "Comprehensive backup completed successfully"
        notify "✅ Backup completed successfully"
    else
        log "Backup process completed with errors"
        notify "❌ Backup completed with errors" "danger"
    fi
}

# Execute main function
main "$@"
```

### Phase 6: Documentation and Procedures

#### Operations Runbook

````markdown
# System Administration Operations Runbook

## System Architecture Overview
- **Load Balancer**: HAProxy on lb-01 (10.0.101.10)
- **Web Servers**: Apache on web-01, web-02 (10.0.101.11-12)
- **Application Server**: Python/Flask on app-01 (10.0.1.10)
- **Database**: MySQL on db-01 (10.0.1.11)
- **Monitoring**: Prometheus/Grafana on monitor-01 (10.0.1.20)
- **Logging**: ELK Stack on log-01 (10.0.1.21)
- **Backup**: Bacula on backup-01 (10.0.1.22)

## Common Operations

### Service Management
```bash
# Check service status across all servers
ansible all -i inventory/production -m service -a "name=apache2 state=started"

# Restart application server
ansible app_servers -i inventory/production -m systemd -a "name=webapp state=restarted"

# Check system health
ansible all -i inventory/production -m command -a "uptime"
````

### Deployment Procedures

1. **Pre-deployment Checklist**
    
    - [ ] Backup current application
    - [ ] Verify staging environment
    - [ ] Check monitoring alerts
    - [ ] Notify team of deployment
2. **Deployment Steps**
    
    ```bash
    # Deploy to staging
    ansible-playbook -i inventory/staging playbooks/deploy.yml --extra-vars "docker_image=new_image:tag"
    
    # Run integration tests
    ./scripts/integration_tests.sh staging.sysadmin-project.com
    
    # Deploy to production
    ansible-playbook -i inventory/production playbooks/deploy.yml --extra-vars "docker_image=new_image:tag"
    ```
    
3. **Post-deployment Verification**
    
    - [ ] Check application health endpoints
    - [ ] Verify monitoring metrics
    - [ ] Test critical user flows
    - [ ] Monitor error logs

### Incident Response Procedures

#### High Severity Incidents

1. **Immediate Response**
    
    - Check system status dashboard
    - Identify affected services
    - Implement immediate mitigation
    - Notify stakeholders
2. **Investigation**
    
    - Gather logs and metrics
    - Identify root cause
    - Document findings
3. **Resolution**
    
    - Implement permanent fix
    - Verify resolution
    - Update monitoring/alerting
    - Conduct post-mortem

#### Common Troubleshooting

**Web Application Not Responding**

```bash
# Check load balancer status
ssh lb-01 "sudo systemctl status haproxy"

# Check web server health
ansible web_servers -i inventory/production -m uri -a "url=http://localhost/health"

# Check application server
ssh app-01 "sudo systemctl status webapp"
ssh app-01 "sudo journalctl -u webapp -f"

# Check database connectivity
ssh db-01 "sudo systemctl status mysql"
mysql -h db-01 -u webapp_user -p -e "SELECT 1"
```

**High CPU Usage**

```bash
# Identify processes consuming CPU
ansible all -i inventory/production -m shell -a "top -bn1 | head -20"

# Check for runaway processes
ansible all -i inventory/production -m shell -a "ps aux --sort=-%cpu | head -10"

# Monitor real-time usage
ssh target-server "htop"
```

**Disk Space Issues**

```bash
# Check disk usage
ansible all -i inventory/production -m shell -a "df -h"

# Find large files
ansible all -i inventory/production -m shell -a "find /var/log -type f -size +100M"

# Clean up logs
ansible all -i inventory/production -m shell -a "journalctl --vacuum-time=7d"
```

### Maintenance Procedures

#### Weekly Maintenance

```bash
#!/bin/bash
# weekly_maintenance.sh

# Update security patches
ansible all -i inventory/production -m apt -a "update_cache=yes upgrade=yes" --become

# Rotate logs
ansible all -i inventory/production -m command -a "logrotate -f /etc/logrotate.conf" --become

# Clean temporary files
ansible all -i inventory/production -m shell -a "find /tmp -type f -mtime +7 -delete" --become

# Check and repair file systems
ansible all -i inventory/production -m shell -a "fsck -n /dev/sda1" --become

# Update SSL certificates if needed
ansible web_servers -i inventory/production -m command -a "certbot renew --dry-run" --become
```

#### Monthly Maintenance

- Review and update security policies
- Analyze performance metrics and optimize
- Update monitoring and alerting rules
- Review and test backup/recovery procedures
- Update documentation
- Security vulnerability assessment

### Disaster Recovery Procedures

#### Database Recovery

```bash
# Stop application services
ansible app_servers -i inventory/production -m systemd -a "name=webapp state=stopped" --become

# Restore from latest backup
mysql -u root -p < /backup/mysql/latest_backup.sql

# Verify data integrity
mysql -u root -p -e "CHECK TABLE webapp.users; CHECK TABLE webapp.sessions;"

# Start application services
ansible app_servers -i inventory/production -m systemd -a "name=webapp state=started" --become
```

#### Full System Recovery

1. Provision new infrastructure using Terraform
2. Run Ansible playbooks to configure services
3. Restore data from backups
4. Update DNS records
5. Verify system functionality
6. Update monitoring configurations

````

### Phase 7: Final Integration and Testing

#### Comprehensive System Test Suite
```bash
#!/bin/bash
# scripts/system_integration_tests.sh

set -euo pipefail

BASE_URL="$1"
LOG_FILE="/tmp/integration_tests.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

test_web_frontend() {
    log "Testing web frontend..."
    
    if curl -f -s -o /dev/null "$BASE_URL"; then
        log "✓ Web frontend is accessible"
        return 0
    else
        log "✗ Web frontend is not accessible"
        return 1
    fi
}

test_api_endpoints() {
    log "Testing API endpoints..."
    
    # Test health endpoint
    if curl -f -s "$BASE_URL/health" | jq -e '.status == "healthy"' > /dev/null; then
        log "✓ Health endpoint is working"
    else
        log "✗ Health endpoint is not working"
        return 1
    fi
    
    # Test user API
    local test_user="{\"username\":\"testuser_$(date +%s)\",\"email\":\"test@example.com\"}"
    
    if user_id=$(curl -f -s -X POST -H "Content-Type: application/json" \
        -d "$test_user" "$BASE_URL/api/users" | jq -r '.user_id'); then
        log "✓ User creation API is working (ID: $user_id)"
        
        # Test user retrieval
        if curl -f -s "$BASE_URL/api/users" | jq -e ".[] | select(.id == $user_id)" > /dev/null; then
            log "✓ User retrieval API is working"
        else
            log "✗ User retrieval API is not working"
            return 1
        fi
    else
        log "✗ User creation API is not working"
        return 1
    fi
}

test_database_connectivity() {
    log "Testing database connectivity..."
    
    if curl -f -s "$BASE_URL/health" | jq -e '.database == "connected"' > /dev/null; then
        log "✓ Database connectivity is working"
        return 0
    else
        log "✗ Database connectivity is not working"
        return 1
    fi
}

test_load_balancer() {
    log "Testing load balancer..."
    
    local responses=()
    for i in {1..10}; do
        response=$(curl -f -s "$BASE_URL/api/server-info" | jq -r '.hostname' 2>/dev/null || echo "error")
        responses+=("$response")
    done
    
    local unique_responses=$(printf '%s\n' "${responses[@]}" | sort -u | wc -l)
    
    if [ "$unique_responses" -gt 1 ]; then
        log "✓ Load balancer is distributing traffic across multiple servers"
        return 0
    else
        log "⚠ Load balancer appears to be sending traffic to only one server"
        return 0  # Not a failure, might be expected in some configurations
    fi
}

test_ssl_certificate() {
    log "Testing SSL certificate..."
    
    if echo | openssl s_client -servername "$BASE_URL" -connect "$BASE_URL:443" 2>/dev/null | \
       openssl x509 -noout -dates | grep "notAfter" | \
       awk -F= '{print $2}' | xargs -I {} date -d "{}" +%s > /tmp/cert_expiry; then
        
        local cert_expiry=$(cat /tmp/cert_expiry)
        local current_time=$(date +%s)
        local days_until_expiry=$(( (cert_expiry - current_time) / 86400 ))
        
        if [ "$days_until_expiry" -gt 30 ]; then
            log "✓ SSL certificate is valid and expires in $days_until_expiry days"
            return 0
        else
            log "⚠ SSL certificate expires in $days_until_expiry days"
            return 0  # Warning, not failure
        fi
    else
        log "✗ Could not verify SSL certificate"
        return 1
    fi
}

test_monitoring() {
    log "Testing monitoring systems..."
    
    # Test Prometheus
    if curl -f -s -o /dev/null "http://monitor-01:9090/-/healthy"; then
        log "✓ Prometheus is healthy"
    else
        log "✗ Prometheus is not healthy"
        return 1
    fi
    
    # Test Grafana
    if curl -f -s -o /dev/null "http://monitor-01:3000/api/health"; then
        log "✓ Grafana is healthy"
    else
        log "✗ Grafana is not healthy"
        return 1
    fi
}

# Main test execution
main() {
    log "Starting comprehensive integration tests for $BASE_URL"
    
    local test_functions=(
        "test_web_frontend"
        "test_api_endpoints"
        "test_database_connectivity"
        "test_load_balancer"
        "test_ssl_certificate"
        "test_monitoring"
    )
    
    local passed=0
    local failed=0
    
    for test_func in "${test_functions[@]}"; do
        if $test_func; then
            ((passed++))
        else
            ((failed++))
        fi
    done
    
    log "Integration tests completed: $passed passed, $failed failed"
    
    if [ $failed -eq 0 ]; then
        log "🎉 All integration tests passed!"
        exit 0
    else
        log "❌ Some integration tests failed"
        exit 1
    fi
}

main "$@"
````

### Capstone XP Tasks - Complete Project

- [ ] **Infrastructure Setup**: Deploy complete infrastructure using Terraform
- [ ] **Configuration Management**: Configure all services using Ansible
- [ ] **Application Deployment**: Deploy and configure the sample application
- [ ] **Monitoring Implementation**: Set up comprehensive monitoring and alerting
- [ ] **Backup System**: Implement automated backup and recovery procedures
- [ ] **Security Hardening**: Implement security policies and access controls
- [ ] **CI/CD Pipeline**: Set up automated testing and deployment pipeline
- [ ] **Documentation**: Create comprehensive operations documentation
- [ ] **Disaster Recovery**: Test full system recovery procedures
- [ ] **Performance Optimization**: Tune system performance and scalability
- [ ] **Integration Testing**: Execute end-to-end system tests
- [ ] **Operations Procedures**: Develop incident response and maintenance procedures

---

## Quick Reference Guides

### Essential Commands Cheat Sheet

#### User Management

```bash
# Create user with home directory and shell
sudo useradd -m -s /bin/bash username

# Add user to sudo group
sudo usermod -aG sudo username

# Change password
sudo passwd username

# Lock/unlock user account
sudo usermod -L username  # lock
sudo usermod -U username  # unlock

# Delete user and home directory
sudo userdel -r username
```

#### Service Management (systemd)

```bash
# Service operations
sudo systemctl start service_name
sudo systemctl stop service_name
sudo systemctl restart service_name
sudo systemctl reload service_name
sudo systemctl status service_name

# Auto-start configuration
sudo systemctl enable service_name
sudo systemctl disable service_name
sudo systemctl is-enabled service_name

# View service logs
sudo journalctl -u service_name -f
sudo journalctl -u service_name --since "1 hour ago"
```

#### File System Management

```bash
# Disk usage and mounting
df -h                    # Disk space usage
du -sh /path/*          # Directory space usage
lsblk                   # Block devices
sudo mount /dev/sdb1 /mnt/disk
sudo umount /mnt/disk

# File permissions
chmod 755 file          # rwxr-xr-x
chmod 644 file          # rw-r--r--
chown user:group file   # Change ownership
```

#### Network Troubleshooting

```bash
# Connectivity testing
ping -c 4 hostname
traceroute hostname
nmap -p 80,443 hostname

# Network information
ip addr show            # IP addresses
ip route show           # Routing table
netstat -tuln          # Listening ports
ss -tuln               # Socket statistics
```

#### Process Management

```bash
# Process viewing and control
ps aux                 # All processes
top                    # Real-time process view
htop                   # Enhanced process viewer
kill -9 PID           # Force kill process
killall process_name  # Kill by name
pgrep process_name    # Find PID by name
```

### Troubleshooting Flowcharts

#### Service Not Starting

```
Service won't start
        ↓
Check service status
    systemctl status service_name
        ↓
Check service logs
    journalctl -u service_name
        ↓
Common issues:
├── Configuration error → Fix config file
├── Port already in use → Check with netstat/ss
├── Permission denied → Check file permissions
├── Missing dependencies → Install required packages
└── Resource limits → Check ulimits, memory
```

#### Website Not Loading

```
Website not responding
        ↓
Check from server locally
    curl http://localhost
        ↓
    Working? ────No──── Check web server
        │                   ├── systemctl status apache2/nginx
        │                   ├── Check error logs
        │                   └── Check configuration
        Yes
        ↓
Check firewall
    ├── ufw status
    ├── iptables -L
    └── Check cloud security groups
        ↓
Check DNS resolution
    ├── nslookup domain
    ├── dig domain
    └── Check /etc/hosts
        ↓
Check network connectivity
    ├── ping server
    ├── traceroute server
    └── Check routing tables
```

#### High System Load

```
High system load
        ↓
Check CPU usage
    top, htop, sar -u
        ↓
Identify top processes
    ps aux --sort=-%cpu
        ↓
Check disk I/O
    iostat -x, iotop
        ↓
Check memory usage
    free -h, vmstat
        ↓
Actions:
├── Kill runaway processes
├── Restart problematic services
├── Scale resources (CPU/RAM)
└── Optimize applications
```

### Emergency Procedures

#### System Recovery Boot

```bash
# Boot from rescue/recovery media
# Mount root filesystem
mkdir /mnt/recover
mount /dev/sda1 /mnt/recover

# Chroot into system
chroot /mnt/recover

# Fix critical issues:
# - Repair filesystem: fsck /dev/sda1
# - Fix bootloader: grub-install /dev/sda
# - Reset passwords: passwd username
# - Fix network config: edit /etc/netplan/ or /etc/network/interfaces

# Exit chroot and reboot
exit
umount /mnt/recover
reboot
```

#### Emergency User Access

```bash
# Single user mode (GRUB)
# Add to kernel line: init=/bin/bash

# Or use recovery mode
# Select "Advanced options" → "recovery mode" → "root shell"

# Reset root password
passwd root

# Enable SSH root login temporarily
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
systemctl restart ssh

# Create emergency admin user
useradd -m -G sudo emergency_admin
passwd emergency_admin
```

### Performance Optimization Quick Wins

#### System Tuning

```bash
# Reduce swappiness
echo 'vm.swappiness=10' >> /etc/sysctl.conf

# Increase file limits
echo '* soft nofile 65536' >> /etc/security/limits.conf
echo '* hard nofile 65536' >> /etc/security/limits.conf

# Enable BBR TCP congestion control
echo 'net.core.default_qdisc=fq' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_congestion_control=bbr' >> /etc/sysctl.conf

# Apply changes
sysctl -p
```

#### Database Optimization (MySQL)

```sql
-- Check slow queries
SHOW VARIABLES LIKE 'slow_query_log';
SET GLOBAL slow_query_log = 'ON';

-- Optimize tables
OPTIMIZE TABLE table_name;

-- Check index usage
EXPLAIN SELECT * FROM table_name WHERE column = 'value';

-- Monitor connections
SHOW PROCESSLIST;
SHOW STATUS LIKE 'Threads_connected';
```

#### Web Server Optimization (Apache)

```bash
# Enable compression
a2enmod deflate
a2enmod expires
a2enmod headers

# Optimize MPM configuration
# Edit /etc/apache2/mods-available/mpm_prefork.conf
<IfModule mpm_prefork_module>
    StartServers             4
    MinSpareServers          20
    MaxSpareServers          40
    MaxRequestWorkers        200
    MaxConnectionsPerChild   4500
</IfModule>
```

### Security Hardening Checklist

#### System Security

- [ ] Regular security updates: `apt update && apt upgrade`
- [ ] Remove unnecessary packages: `apt autoremove`
- [ ] Disable unused services: `systemctl list-unit-files --state=enabled`
- [ ] Configure automatic updates: `dpkg-reconfigure unattended-upgrades`
- [ ] Set up fail2ban: `apt install fail2ban`
- [ ] Configure firewall: `ufw enable`
- [ ] Secure SSH configuration
- [ ] Regular security audits: `lynis audit system`

#### User Security

- [ ] Strong password policies
- [ ] Remove default accounts
- [ ] Use SSH keys instead of passwords
- [ ] Implement 2FA where possible
- [ ] Regular access reviews
- [ ] Principle of least privilege

#### Network Security

- [ ] Change default ports
- [ ] Use VPN for remote access
- [ ] Network segmentation
- [ ] Regular port scans: `nmap -sS localhost`
- [ ] SSL/TLS for all web services
- [ ] Keep certificates updated

### Monitoring and Alerting Setup

#### Key Metrics to Monitor

```bash
# System metrics
- CPU usage (avg > 80% for 5 minutes)
- Memory usage (> 85%)
- Disk space (< 15% free)
- System load (> number of CPUs)
- Network I/O
- Disk I/O

# Application metrics
- Response time (> 2 seconds)
- Error rate (> 5%)
- Request rate
- Database connections
- Queue length

# Security metrics
- Failed login attempts
- Privilege escalation events
- File integrity violations
- Network intrusion attempts
```

#### Alerting Best Practices

```yaml
# Alert severity levels
Critical: Immediate action required (service down, data loss)
Warning: Attention needed (high resource usage, performance degradation)
Info: Awareness (maintenance, updates, normal events)

# Alert routing
Critical → Phone/SMS + Email + Slack
Warning → Email + Slack
Info → Slack only

# Alert fatigue prevention
- Use appropriate thresholds
- Implement alert suppression during maintenance
- Regular review and tuning of alerts
- Clear escalation procedures
```

---

## Advanced Topics and Future Learning

### Cloud Computing Integration

- **AWS/Azure/GCP**: Cloud-specific system administration
- **Infrastructure as Code**: Advanced Terraform, CloudFormation
- **Container Orchestration**: Kubernetes administration
- **Serverless Computing**: Function-as-a-Service management
- **Cloud Security**: Identity and Access Management (IAM)

### DevOps and SRE Practices

- **Site Reliability Engineering**: Error budgets, SLI/SLO/SLA
- **Chaos Engineering**: Resilience testing with tools like Chaos Monkey
- **GitOps**: Infrastructure and application management through Git
- **Observability**: Advanced monitoring with OpenTelemetry
- **Service Mesh**: Istio, Linkerd for microservices

### Advanced Security

- **Zero Trust Architecture**: Never trust, always verify
- **Security Information and Event Management (SIEM)**
- **Vulnerability Management**: Automated scanning and remediation
- **Compliance Frameworks**: SOC 2, ISO 27001, PCI DSS
- **Incident Response**: Automated response and forensics

### Automation and Orchestration

- **Advanced Ansible**: Dynamic inventories, custom modules
- **Puppet/Chef**: Alternative configuration management
- **Kubernetes Operators**: Custom resource management
- **Event-Driven Automation**: Respond to system events automatically
- **AI/ML in Operations**: Predictive maintenance, anomaly detection

### Specialized Platforms

- **Database Administration**: Advanced MySQL, PostgreSQL, MongoDB
- **High-Performance Computing (HPC)**: Cluster management
- **Content Delivery Networks (CDN)**: Global content distribution
- **Message Queues**: RabbitMQ, Apache Kafka administration
- **Search Engines**: Elasticsearch cluster management

---

## Certification Paths

### Linux Certifications

- **Red Hat Certified System Administrator (RHCSA)**
- **Red Hat Certified Engineer (RHCE)**
- **Linux Professional Institute (LPIC-1, LPIC-2, LPIC-3)**
- **CompTIA Linux+**

### Cloud Certifications

- **AWS Certified SysOps Administrator**
- **Azure Administrator Associate**
- **Google Cloud Professional Cloud Architect**
- **Kubernetes Certified Administrator (CKA)**

### Security Certifications

- **CompTIA Security+**
- **Certified Information Systems Security Professional (CISSP)**
- **Certified Ethical Hacker (CEH)**

### DevOps Certifications

- **Docker Certified Associate**
- **Terraform Associate**
- **Jenkins Engineer**

---

## Community Resources

### Documentation and Learning

- **Red Hat Documentation**: Access.redhat.com
- **Ubuntu Documentation**: Help.ubuntu.com
- **Linux Documentation Project**: tldp.org
- **Arch Wiki**: wiki.archlinux.org (excellent for any distro)

### Communities and Forums

- **r/sysadmin**: Reddit community
- **Server Fault**: Stack Exchange for sysadmins
- **Linux.org**: General Linux community
- **Spiceworks**: IT professional community

### Tools and Resources

- **GitHub**: Open source tools and scripts
- **Ansible Galaxy**: Pre-built Ansible roles
- **Docker Hub**: Container images
- **Terraform Registry**: Infrastructure modules

### Blogs and News

- **Ars Technica**: Technology news
- **The Register**: IT industry news
- **Linux Journal**: Linux-focused articles
- **Red Hat Blog**: Enterprise Linux insights

---

## Final Words

System Administration is a continuously evolving field that requires ongoing learning and adaptation. The fundamentals covered in this guide provide a solid foundation, but the journey doesn't end here.

**Key Success Factors:**

1. **Hands-on Practice**: Nothing replaces actual experience
2. **Continuous Learning**: Technology changes rapidly
3. **Community Engagement**: Learn from others' experiences
4. **Documentation**: Always document your work
5. **Automation First**: Automate repetitive tasks
6. **Security Mindset**: Security is everyone's responsibility

**Remember:**

- Start with the basics and build complexity gradually
- Test everything in non-production environments first
- Keep backups of everything important
- Monitor your systems proactively
- Learn from failures and incidents
- Stay curious and keep experimenting

The skills you've learned through this comprehensive guide will serve as your foundation for a successful career in system administration. Whether you're managing a small startup's infrastructure or enterprise-level systems, these principles and practices will guide you toward building reliable, secure, and efficient computing environments.

**Tags:** #SystemAdministration #Linux #Windows #DevOps #Infrastructure #Security #Monitoring #Automation #CloudComputing #BestPractices# System Administration

#SystemAdministration #Linux #Windows #DevOps #Infrastructure #Security #Monitoring #Automation

**Related:** [[Linux Basics]] | [[Command Line Interface]] | [[Network Administration]] | [[Security Management]] | [[Performance Monitoring]] | [[Backup and Recovery]]

---

## Overview

System Administration involves managing, configuring, and maintaining computer systems and networks. System administrators ensure systems run efficiently, securely, and reliably while supporting users and business operations.

**Core Responsibilities:**

- **System Installation & Configuration**
- **User and Access Management**
- **Security Implementation & Monitoring**
- **Performance Optimization**
- **Backup and Disaster Recovery**
- **Network Administration**
- **Automation and Scripting**
- **Troubleshooting and Support**

---

## Module 1: System Administration Fundamentals

### What is System Administration?

System Administration is the discipline of managing computer systems, networks, and IT infrastructure. It encompasses:

- **Server Management**: Installing, configuring, and maintaining servers
- **User Management**: Creating accounts, managing permissions, access control
- **Security**: Implementing security policies, monitoring threats
- **Monitoring**: Tracking system performance, availability, and health
- **Automation**: Scripting routine tasks and processes
- **Documentation**: Maintaining system documentation and procedures

### Core Principles

#### 1. Reliability and Availability

```bash
# System uptime monitoring
uptime                          # Check system uptime
systemctl status critical-service
journalctl -u service-name -f   # Monitor service logs

# High availability concepts
# - Redundancy
# - Load balancing  
# - Failover mechanisms
# - Disaster recovery planning
```

#### 2. Security First

```bash
# Security hardening basics
sudo ufw enable                 # Enable firewall
sudo fail2ban-client status     # Check intrusion prevention
sudo lynis audit system         # Security audit tool

# Regular security tasks
sudo apt update && sudo apt upgrade    # Keep systems updated
sudo chkrootkit                        # Check for rootkits
```

#### 3. Automation and Efficiency

```bash
# Automate routine tasks
crontab -e                      # Schedule automated tasks
ansible-playbook deploy.yml     # Configuration management
bash /scripts/maintenance.sh    # Automated maintenance
```

#### 4. Monitoring and Alerting

```bash
# System monitoring
htop                           # Process monitoring
iotop                          # I/O monitoring
netstat -tuln                  # Network connections
df -h && free -h              # Disk and memory usage
```

### System Architecture Understanding

#### Hardware Components

- **CPU**: Processing power, cores, architecture
- **Memory (RAM)**: System and application memory
- **Storage**: HDDs, SSDs, RAID configurations
- **Network**: NICs, bandwidth, connectivity
- **Power**: UPS, redundant power supplies

#### Software Layers

```
Applications
├── Application Software (Web servers, databases)
├── Middleware (Application servers, message queues)  
├── Operating System (Linux, Windows, Unix)
├── Drivers (Hardware abstraction)
└── Firmware/BIOS (Hardware initialization)
```

### XP Tasks - Fundamentals

- [ ] Check system information (CPU, memory, disk) on your system
- [ ] Review system logs for the past 24 hours
- [ ] Identify running services and their status
- [ ] Check network configuration and connectivity
- [ ] Document current system configuration
- [ ] Create a basic system monitoring script

---

## Module 2: User and Access Management

### User Account Management

#### Linux User Management

```bash
# Create users
sudo useradd -m -s /bin/bash username     # Create user with home directory
sudo useradd -m -G sudo username          # Create user with sudo access
sudo passwd username                      # Set password

# Modify users  
sudo usermod -aG groupname username       # Add user to group
sudo usermod -s /bin/zsh username         # Change shell
sudo usermod -l newname oldname           # Rename user
sudo usermod -L username                  # Lock account
sudo usermod -U username                  # Unlock account

# Delete users
sudo userdel username                     # Delete user (keep home)
sudo userdel -r username                  # Delete user and home directory

# User information
id username                               # User ID and groups
finger username                           # User information
last username                             # Login history
w                                         # Currently logged in users
```

#### Windows User Management

```powershell
# PowerShell user management
New-LocalUser -Name "username" -Description "User description"
Set-LocalUser -Name "username" -Password (ConvertTo-SecureString "password" -AsPlainText -Force)
Add-LocalGroupMember -Group "Administrators" -Member "username"
Get-LocalUser                             # List users
Remove-LocalUser -Name "username"         # Delete user

# Command Prompt
net user username password /add          # Create user
net user username /active:no             # Disable user
net localgroup administrators username /add  # Add to admin group
```

### Group Management

#### Linux Groups

```bash
# Group operations
sudo groupadd groupname                   # Create group
sudo groupdel groupname                   # Delete group
sudo gpasswd -a username groupname        # Add user to group
sudo gpasswd -d username groupname        # Remove user from group

# View groups
groups username                           # User's groups
getent group                              # All groups
grep "^groupname:" /etc/group            # Group information
```

#### Common Linux Groups

```bash
# Important system groups
sudo        # Sudo access
wheel       # Administrative access (some distros)
www-data    # Web server group
mysql       # Database group
docker      # Docker access
audio       # Audio device access
video       # Video device access
```

### Permission Management

#### File Permissions (Linux)

```bash
# Basic permissions
chmod 755 /path/to/file                   # rwxr-xr-x
chmod 644 /path/to/file                   # rw-r--r--
chmod 600 /path/to/file                   # rw-------

# Recursive permissions
chmod -R 755 /path/to/directory

# Symbolic permissions
chmod u+x filename                        # Add execute for owner
chmod g-w filename                        # Remove write for group
chmod o=r filename                        # Set others to read only
chmod a+r filename                        # Add read for all

# Special permissions
chmod +t /tmp                             # Sticky bit
chmod u+s /usr/bin/passwd                 # SUID
chmod g+s /shared/directory               # SGID
```

#### Access Control Lists (ACLs)

```bash
# Set ACLs
setfacl -m u:username:rwx filename        # Give user full access
setfacl -m g:groupname:r-x filename       # Give group read/execute
setfacl -m d:u:username:rwx directory/    # Default ACL for directory

# View ACLs
getfacl filename                          # Show file ACLs
ls -la filename                           # Shows '+' if ACLs present

# Remove ACLs
setfacl -x u:username filename            # Remove user ACL
setfacl -b filename                       # Remove all ACLs
```

### SSH Key Management

#### SSH Key Generation and Management

```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -C "user@email.com"
ssh-keygen -t ed25519 -C "user@email.com"    # More secure option

# Copy public key to server
ssh-copy-id user@server
cat ~/.ssh/id_rsa.pub | ssh user@server 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'

# SSH agent for key management
eval "$(ssh-agent -s)"                    # Start SSH agent
ssh-add ~/.ssh/id_rsa                     # Add key to agent
ssh-add -l                                # List loaded keys
```

#### SSH Configuration

```bash
# Client configuration (~/.ssh/config)
Host myserver
    HostName server.example.com
    User myuser
    Port 2222
    IdentityFile ~/.ssh/myserver_key
    
Host jumpbox
    HostName jump.example.com
    User admin
    ProxyJump bastion.example.com

# Server configuration (/etc/ssh/sshd_config)
Port 22
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers myuser
```

### Privilege Escalation and Sudo

#### Sudo Configuration

```bash
# Edit sudoers file (always use visudo)
sudo visudo

# Sudoers examples
username ALL=(ALL:ALL) ALL               # Full sudo access
username ALL=(ALL) NOPASSWD: ALL         # No password required
username ALL=(ALL) /bin/systemctl        # Specific command only
%admin ALL=(ALL) ALL                     # Group access

# Sudo aliases
Cmnd_Alias NETWORKING = /sbin/route, /sbin/ifconfig, /bin/ping
User_Alias WEBADMINS = alice, bob, charlie
WEBADMINS ALL = NETWORKING

# Test sudo configuration
sudo -l                                   # List user's sudo privileges
sudo -u otheruser command                 # Run as different user
```

### XP Tasks - User & Access Management

- [ ] Create a new user with appropriate groups
- [ ] Set up SSH key authentication for a user
- [ ] Configure sudo access for specific commands
- [ ] Create a shared directory with group permissions
- [ ] Set up ACLs for fine-grained access control
- [ ] Audit user accounts and permissions
- [ ] Configure SSH server security settings

---

## Module 3: Service and Process Management

### Understanding Services

#### Service Types

- **System Services**: Core OS functionality (networking, logging)
- **Application Services**: User applications (web servers, databases)
- **User Services**: Per-user services
- **Socket Services**: On-demand services triggered by connections

### Systemd Service Management (Modern Linux)

#### Basic Service Operations

```bash
# Service status
systemctl status service-name
systemctl is-active service-name
systemctl is-enabled service-name
systemctl is-failed service-name

# Start/stop/restart services
sudo systemctl start service-name
sudo systemctl stop service-name
sudo systemctl restart service-name
sudo systemctl reload service-name        # Reload config without restart

# Enable/disable auto-start
sudo systemctl enable service-name        # Start at boot
sudo systemctl disable service-name       # Don't start at boot
sudo systemctl mask service-name          # Prevent service from starting
sudo systemctl unmask service-name        # Remove mask
```

#### Service Discovery and Analysis

```bash
# List services
systemctl list-units --type=service
systemctl list-units --type=service --state=active
systemctl list-units --type=service --state=failed
systemctl list-unit-files --type=service

# Service dependencies
systemctl list-dependencies service-name
systemctl show service-name
```

#### Creating Custom Services

```bash
# Create service file (/etc/systemd/system/myapp.service)
sudo nano /etc/systemd/system/myapp.service

# Example service file
[Unit]
Description=My Application
After=network.target
Requires=network.target

[Service]
Type=simple
User=myuser
Group=mygroup
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/start.sh
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable myapp.service
sudo systemctl start myapp.service
```

### Process Management

#### Process Monitoring

```bash
# Real-time process monitoring
top                                       # Traditional process viewer
htop                                      # Enhanced process viewer
atop                                      # Advanced system monitor
iotop                                     # I/O monitoring
```

#### Process Control

```bash
# List processes
ps aux                                    # All processes
ps -ef                                    # Full format
ps -u username                            # User's processes
pgrep -u username                         # Process IDs by user

# Kill processes
kill PID                                  # Graceful termination
kill -9 PID                              # Force kill
kill -HUP PID                            # Reload signal
killall process-name                      # Kill by name
pkill -f pattern                         # Kill by pattern

# Process priority
nice -n 10 command                        # Start with lower priority
renice 10 -p PID                         # Change running process priority
```

#### Background Job Management

```bash
# Job control
command &                                 # Run in background
nohup command &                          # Run immune to hangups
jobs                                     # List jobs
fg %1                                    # Bring job 1 to foreground
bg %1                                    # Send job 1 to background

# Advanced background execution
screen -S session-name command           # Detachable session
tmux new-session -d -s mysession         # Terminal multiplexer
```

### Windows Service Management

#### Windows Services

```powershell
# PowerShell service management
Get-Service                              # List all services
Get-Service -Name "ServiceName"          # Specific service
Start-Service -Name "ServiceName"        # Start service
Stop-Service -Name "ServiceName"         # Stop service
Restart-Service -Name "ServiceName"      # Restart service
Set-Service -Name "ServiceName" -StartupType Automatic  # Auto-start

# Command prompt
sc query                                 # List services
sc query ServiceName                     # Service status
net start ServiceName                    # Start service
net stop ServiceName                     # Stop service
```

### Performance Monitoring and Tuning

#### Resource Monitoring

```bash
# CPU monitoring
top -n 1                                 # Single snapshot
sar -u 1 10                             # CPU utilization (10 samples)
mpstat 1 5                              # Multiprocessor stats

# Memory monitoring
free -h                                  # Memory usage
vmstat 1 5                              # Virtual memory stats
sar -r 1 10                             # Memory utilization

# Disk I/O monitoring
iostat -x 1                             # Extended I/O stats
sar -d 1 10                             # Disk activity
iotop                                   # Top-like I/O monitor

# Network monitoring
sar -n DEV 1 10                         # Network interface stats
netstat -i                              # Interface statistics
ss -tuln                                # Socket statistics
```

#### Performance Tuning

```bash
# System limits
ulimit -a                               # Show current limits
ulimit -n 4096                          # Set file descriptor limit

# Persistent limits (/etc/security/limits.conf)
* soft nofile 4096
* hard nofile 8192
* soft nproc 2048
* hard nproc 4096

# Kernel parameters (/etc/sysctl.conf)
vm.swappiness=10                        # Reduce swap usage
net.core.somaxconn=1024                 # Increase connection queue
fs.file-max=65536                       # Maximum open files

# Apply sysctl changes
sudo sysctl -p
```

### XP Tasks - Service & Process Management

- [ ] Check status of all system services
- [ ] Create a custom systemd service
- [ ] Monitor system processes and resource usage
- [ ] Set up process monitoring and alerting
- [ ] Configure service dependencies and startup order
- [ ] Optimize system performance parameters
- [ ] Practice process troubleshooting techniques

---

## Module 4: Storage and File System Management

### File System Types and Concepts

#### Common File Systems

```bash
# Linux file systems
ext4        # Default Linux filesystem
xfs         # High-performance filesystem
btrfs       # Advanced filesystem with snapshots
zfs         # Advanced filesystem with built-in RAID

# Other file systems
ntfs        # Windows filesystem
fat32       # Universal compatibility
exfat       # Large file support
```

#### File System Hierarchy

```bash
# Standard Linux directory structure
/           # Root directory
/bin        # Essential binaries
/boot       # Boot loader files
/dev        # Device files
/etc        # Configuration files
/home       # User home directories
/lib        # Essential libraries
/media      # Removable media
/mnt        # Mount points
/opt        # Optional packages
/proc       # Process information
/root       # Root user home
/run        # Runtime data
/sbin       # System binaries
/srv        # Service data
/sys        # System information
/tmp        # Temporary files
/usr        # User programs
/var        # Variable data
```

### Disk Management

#### Disk Information and Partitioning

```bash
# View disks and partitions
lsblk                                    # Block device tree
fdisk -l                                 # List all disks
parted -l                                # Parted disk info
df -h                                    # Mounted filesystem usage
du -sh /path                            # Directory usage

# Partition management
sudo fdisk /dev/sdb                      # Partition disk (MBR)
sudo parted /dev/sdb                     # Partition disk (GPT)
sudo gdisk /dev/sdb                      # GPT partitioning

# Create partitions with parted
sudo parted /dev/sdb mklabel gpt
sudo parted /dev/sdb mkpart primary ext4 0% 100%
```

#### File System Creation and Management

```bash
# Create file systems
sudo mkfs.ext4 /dev/sdb1                 # Create ext4 filesystem
sudo mkfs.xfs /dev/sdb1                  # Create XFS filesystem
sudo mkfs.btrfs /dev/sdb1                # Create Btrfs filesystem

# File system checks and repair
sudo fsck /dev/sdb1                      # Check filesystem
sudo fsck.ext4 /dev/sdb1                 # Check ext4 specifically
sudo xfs_repair /dev/sdb1                # Repair XFS filesystem

# File system information
sudo tune2fs -l /dev/sdb1                # Ext4 filesystem info
sudo xfs_info /dev/sdb1                  # XFS filesystem info
```

### Mount Management

#### Mounting File Systems

```bash
# Manual mounting
sudo mkdir /mnt/mydisk
sudo mount /dev/sdb1 /mnt/mydisk         # Mount filesystem
sudo mount -t ext4 /dev/sdb1 /mnt/mydisk # Specify filesystem type
sudo umount /mnt/mydisk                  # Unmount

# Mount with options
sudo mount -o rw,noatime /dev/sdb1 /mnt/mydisk      # Read-write, no access time
sudo mount -o ro /dev/sdb1 /mnt/mydisk              # Read-only
sudo mount -o bind /source /target                   # Bind mount
```

#### Automatic Mounting (/etc/fstab)

```bash
# Edit fstab for persistent mounts
sudo nano /etc/fstab

# fstab format: device mountpoint filesystem options dump pass
/dev/sdb1 /mnt/mydisk ext4 defaults 0 2
UUID=abc123 /home/user/data ext4 defaults,noatime 0 2
//server/share /mnt/network cifs username=user,password=pass 0 0

# Test fstab entries
sudo mount -a                           # Mount all fstab entries
sudo findmnt --verify                   # Verify fstab
```

### Logical Volume Management (LVM)

#### LVM Concepts

- **Physical Volume (PV)**: Physical disk or partition
- **Volume Group (VG)**: Collection of physical volumes
- **Logical Volume (LV)**: Virtual partition from volume group

#### LVM Operations

```bash
# Create physical volume
sudo pvcreate /dev/sdb1
sudo pvdisplay                           # Show physical volumes

# Create volume group
sudo vgcreate myvg /dev/sdb1
sudo vgdisplay                           # Show volume groups

# Create logical volume
sudo lvcreate -n mylv -L 10G myvg        # Create 10GB logical volume
sudo lvcreate -n mylv -l 100%FREE myvg   # Use all free space
sudo lvdisplay                           # Show logical volumes

# Extend logical volume
sudo lvextend -L +5G /dev/myvg/mylv      # Add 5GB
sudo resize2fs /dev/myvg/mylv            # Resize ext4 filesystem
```

### RAID Configuration

#### Software RAID with mdadm

```bash
# RAID levels
# RAID 0: Striping (performance, no redundancy)
# RAID 1: Mirroring (redundancy)
# RAID 5: Striping with parity (performance + redundancy)
# RAID 10: Striped mirrors (performance + redundancy)

# Create RAID arrays
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1  # RAID 1
sudo mdadm --create /dev/md1 --level=5 --raid-devices=3 /dev/sdb1 /dev/sdc1 /dev/sdd1  # RAID 5

# Monitor RAID
cat /proc/mdstat                         # RAID status
sudo mdadm --detail /dev/md0            # Detailed info

# RAID configuration file
sudo mdadm --detail --scan >> /etc/mdadm/mdadm.conf
```

### Storage Performance and Optimization

#### Monitoring Storage Performance

```bash
# I/O statistics
iostat -x 1                             # Extended I/O stats
sar -d 1 10                             # Disk activity
iotop                                   # Process I/O usage
lsof +D /path                           # Files open in directory

# Disk performance testing
sudo hdparm -tT /dev/sda                # Disk speed test
sudo dd if=/dev/zero of=/tmp/test bs=1G count=1 oflag=dsync  # Write test
```

#### Storage Optimization

```bash
# Mount options for performance
# noatime: Don't update access times
# data=writeback: Faster writes (less safe)
# barrier=0: Disable barriers (SSD optimization)

# SSD optimization
sudo fstrim -v /                        # Manual TRIM
sudo systemctl enable fstrim.timer      # Automatic TRIM

# File system tuning
sudo tune2fs -o journal_data_writeback /dev/sdb1  # Change journaling mode
```

### Backup and Recovery

#### File-level Backup Tools

```bash
# rsync backups
rsync -av --delete /source/ /backup/    # Mirror backup
rsync -av --backup --backup-dir=/backup/old /source/ /backup/  # Incremental

# tar archives
tar -czf backup-$(date +%Y%m%d).tar.gz /home/  # Compressed archive
tar -xzf backup.tar.gz                  # Extract archive

# System backup with excludes
rsync -av --exclude='/proc/*' --exclude='/tmp/*' --exclude='/sys/*' / /backup/
```

#### Block-level Backup Tools

```bash
# dd for disk imaging
sudo dd if=/dev/sda of=/backup/disk.img bs=4M status=progress  # Full disk image
sudo dd if=/dev/sda1 of=/backup/partition.img bs=4M            # Partition image

# Restore from image
sudo dd if=/backup/disk.img of=/dev/sdb bs=4M status=progress
```

### XP Tasks - Storage Management

- [ ] Create and format a new partition
- [ ] Set up automatic mounting in /etc/fstab
- [ ] Configure LVM with physical and logical volumes
- [ ] Monitor disk I/O performance
- [ ] Set up a simple RAID array (if multiple disks available)
- [ ] Create automated backup scripts
- [ ] Practice file system repair and recovery

---

## Module 5: Network Administration

### Network Fundamentals

#### OSI Model and TCP/IP Stack

```bash
# Layer understanding
Physical     # Cables, switches, NICs
Data Link    # MAC addresses, Ethernet
Network      # IP addresses, routing
Transport    # TCP, UDP ports
Session      # Connection management
Presentation # Encryption, compression
Application  # HTTP, SSH, FTP
```

#### IP Addressing and Subnetting

```bash
# IPv4 address classes
Class A: 1.0.0.0    - 126.255.255.255  (/8)
Class B: 128.0.0.0  - 191.255.255.255  (/16)
Class C: 192.0.0.0  - 223.255.255.255  (/24)

# Private IP ranges
10.0.0.0/8       # Class A private
172.16.0.0/12    # Class B private
192.168.0.0/16   # Class C private

# Subnet calculation examples
192.168.1.0/24   # 256 addresses (254 usable)
192.168.1.0/25   # 128 addresses (126 usable)
192.168.1.0/26   # 64 addresses (62 usable)
```

### Network Interface Configuration

#### Linux Network Configuration

```bash
# View network interfaces
ip addr show                             # Modern command
ip link show                             # Link layer info
ifconfig                                 # Traditional command

# Configure interfaces
sudo ip addr add 192.168.1.100/24 dev eth0    # Add IP address
sudo ip link set eth0 up                       # Bring interface up
sudo ip link set eth0 down                     # Bring interface down

# Persistent configuration (Ubuntu/Debian - /etc/netplan/)
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true
    eth1:
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]

# Apply netplan configuration
sudo netplan apply
```

#### Red Hat/CentOS Network Configuration

```bash
# Interface configuration files (/etc/sysconfig/network-scripts/)
# ifcfg-eth0
DEVICE=eth0
BOOTPROTO=static
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
DNS2=8.8.4.4
ONBOOT=yes

# Restart networking
sudo systemctl restart network
sudo nmcli connection reload
```

### Routing and Gateway Management

#### Routing Table Management

```bash
# View routing table
ip route show                            # Current routes
route -n                                 # Traditional command
netstat -rn                             # Alternative view

# Add/remove routes
sudo ip route add 192.168.2.0/24 via 192.168.1.1    # Add route
sudo ip route del 192.168.2.0/24                      # Delete route
sudo ip route add default via 192.168.1.1             # Default gateway

# Persistent routes (varies by distribution)
# Ubuntu/Debian: Add to netplan configuration
# Red Hat/CentOS: /etc/sysconfig/network-scripts/route-interface
```

#### Advanced Routing

```bash
# Policy-based routing
sudo ip rule add from 192.168.1.0/24 table 100
sudo ip route add default via 192.168.1.1 table 100

# Load balancing (multiple gateways)
sudo ip route add default scope global nexthop via 192.168.1.1 weight 1 nexthop via 192.168.2.1 weight 1
```

### DNS Configuration

#### DNS Client Configuration

```bash
# DNS resolution files
/etc/resolv.conf                         # DNS servers
/etc/hosts                              # Static hostname resolution
/etc/nsswitch.conf                      # Resolution order

# Example /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
search company.local
domain company.local

# DNS testing
nslookup hostname                        # Basic DNS lookup
dig hostname                            # Detailed DNS lookup
dig @8.8.8.8 hostname                   # Query specific server
host hostname                           # Simple lookup
```

#### DNS Server Setup (BIND)

```bash
# Install BIND
sudo apt install bind9                   # Ubuntu/Debian
sudo yum install bind                    # Red Hat/CentOS

# Main configuration (/etc/bind/named.conf.local)
zone "example.com" {
    type master;
    file "/etc/bind/db.example.com";
};

# Zone file (/etc/bind/db.example.com)
$TTL    604800
@       IN      SOA     ns1.example.com. admin.example.com. (
                              2021032901         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL

@       IN      NS      ns1.example.com.
@       IN      A       192.168.1.10
ns1     IN      A       192.168.1.10
www     IN      A       192.168.1.20
```

### DHCP Configuration

#### DHCP Server Setup

```bash
# Install DHCP server
sudo apt install isc-dhcp-server         # Ubuntu/Debian
sudo yum install dhcp                     # Red Hat/CentOS

# Configuration (/etc/dhcp/dhcpd.conf)
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.100 192.168.1.200;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8, 8.8.4.4;
    option domain-name "company.local";
    default-lease-time 600;
    max-lease-time 7200;
}

# Static reservations
host workstation1 {
    hardware ethernet 00:11:22:33:44:55;
    fixed-address 192.168.1.50;
}

# Start DHCP service
sudo systemctl enable dhcpd
sudo systemctl start dhcpd
```

### Firewall Configuration

#### iptables (Traditional Linux Firewall)

```bash
# Basic iptables rules
sudo iptables -L                         # List current rules
sudo iptables -F                         # Flush all rules

# Allow traffic
sudo iptables -A INPUT -i lo -j ACCEPT                    # Allow loopback
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT  # Allow established
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT        # Allow SSH
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT        # Allow HTTP

# Block traffic
sudo iptables -A INPUT -j DROP                            # Default drop

# Save rules (Ubuntu/Debian)
sudo iptables-save > /etc/iptables/rules.v4
```

#### UFW (Uncomplicated Firewall)

```bash
# UFW basic usage
sudo ufw enable                          # Enable firewall
sudo ufw disable                         # Disable firewall
sudo ufw status                          # Show status
sudo ufw status verbose                  # Detailed status

# Allow/deny rules
sudo ufw allow 22                        # Allow SSH
sudo ufw allow ssh                       # Allow SSH (by name)
sudo ufw allow from 192.168.1.0/24      # Allow from subnet
sudo ufw deny 23                         # Deny telnet
sudo ufw delete allow 80                 # Remove rule

# Application profiles
sudo ufw app list                        # List application profiles
sudo ufw allow 'Apache Full'            # Allow Apache
```

#### firewalld (Red Hat/CentOS/Fedora)

```bash
# firewalld management
sudo systemctl start firewalld
sudo systemctl enable firewalld
sudo firewall-cmd --state                # Check status

# Zone management
sudo firewall-cmd --get-default-zone     # Show default zone
sudo firewall-cmd --list-all            # List all settings
sudo firewall-cmd --zone=public --list-all  # List zone settings

# Add/remove services
sudo firewall-cmd --add-service=ssh      # Temporary
sudo firewall-cmd --add-service=ssh --permanent  # Permanent
sudo firewall-cmd --add-port=8080/tcp --permanent  # Add custom port
sudo firewall-cmd --reload               # Reload configuration
```

### Network Monitoring and Troubleshooting

#### Network Connectivity Testing

```bash
# Basic connectivity
ping -c 4 google.com                     # Test connectivity
ping6 -c 4 ipv6.google.com              # IPv6 connectivity
traceroute google.com                    # Show route path
mtr google.com                           # Continuous traceroute

# Port testing
telnet server.com 80                     # Test port connectivity
nc -zv server.com 80                     # Netcat port test
nmap -p 80,443 server.com               # Port scan
```

#### Network Statistics and Monitoring

```bash
# Network connections
netstat -tuln                           # Listening ports
netstat -i                              # Interface statistics
ss -tuln                                # Modern alternative to netstat
ss -s                                   # Socket statistics

# Bandwidth monitoring
iftop                                   # Real-time bandwidth usage
nethogs                                 # Per-process network usage
vnstat                                  # Network statistics
sar -n DEV 1 5                         # Network interface stats

# Packet capture
sudo tcpdump -i eth0                    # Capture packets on interface
sudo tcpdump -i eth0 port 80            # Capture HTTP traffic
sudo tcpdump -i eth0 host 192.168.1.1  # Capture traffic to/from host
```

#### Network Performance Optimization

```bash
# Network tuning parameters (/etc/sysctl.conf)
net.core.rmem_max = 16777216            # Increase receive buffer
net.core.wmem_max = 16777216            # Increase send buffer
net.ipv4.tcp_congestion_control = bbr   # Use BBR congestion control
net.core.netdev_max_backlog = 5000      # Increase network backlog

# Apply network optimizations
sudo sysctl -p
```

### XP Tasks - Network Administration

- [ ] Configure a static IP address on a network interface
- [ ] Set up DNS resolution with custom entries
- [ ] Configure firewall rules for web server access
- [ ] Monitor network traffic and identify bottlenecks
- [ ] Set up DHCP reservations for specific devices
- [ ] Troubleshoot network connectivity issues
- [ ] Implement network security policies

---

## Module 6: Security and Compliance

### System Hardening

#### Security Baseline Configuration

```bash
# Disable unnecessary services
sudo systemctl list-unit-files --type=service --state=enabled
sudo systemctl disable service-name
sudo systemctl mask service-name         # Prevent accidental enabling

# Remove unnecessary packages
sudo apt autoremove                      # Remove unused packages
sudo apt purge package-name              # Completely remove package

# Secure boot process
sudo chmod 700 /boot                     # Restrict boot directory access
sudo chown root:root /etc/grub.d/*       # Secure GRUB configuration
```

#### File System Security

```bash
# Secure file permissions
find / -type f -perm -4000 -ls 2>/dev/null    # Find SUID files
find / -type f -perm -2000 -ls 2>/dev/null    # Find SGID files
find / -type f -perm -1000 -ls 2>/dev/null    # Find sticky bit files

# Secure important directories
sudo chmod 700 /root                          # Root home directory
sudo chmod 644 /etc/passwd                    # User database
sudo chmod 640 /etc/shadow                    # Password hashes
sudo chmod 644 /etc/group                     # Group database

# Immutable files (prevent tampering)
sudo chattr +i /etc/passwd                    # Make file immutable
sudo chattr +i /etc/shadow
sudo lsattr /etc/passwd                       # Check attributes
```

#### Network Security

```bash
# Disable IPv6 (if not needed)
echo 'net.ipv6.conf.all.disable_ipv6 = 1' >> /etc/sysctl.conf

# IP spoofing protection
echo 'net.ipv4.conf.all.rp_filter = 1' >> /etc/sysctl.conf

# Disable IP forwarding (if not a router)
echo 'net.ipv4.ip_forward = 0' >> /etc/sysctl.conf

# Disable ICMP redirects
echo 'net.ipv4.conf.all.accept_redirects = 0' >> /etc/sysctl.conf
echo 'net.ipv4.conf.all.send_redirects = 0' >> /etc/sysctl.conf

# Apply changes
sudo sysctl -p
```

### User Security and Authentication

#### Password Policies

```bash
# Password policy configuration (/etc/login.defs)
PASS_MAX_DAYS   90                       # Password expiry
PASS_MIN_DAYS   1                        # Minimum password age
PASS_MIN_LEN    8                        # Minimum password length
PASS_WARN_AGE   7                        # Warning before expiry

# PAM password complexity (/etc/pam.d/common-password)
password requisite pam_pwquality.so retry=3 minlen=8 difok=3

# Account lockout policy (/etc/pam.d/common-auth)
auth required pam_tally2.so deny=3 onerr=fail unlock_time=600
```

#### SSH Security Hardening

```bash
# SSH server configuration (/etc/ssh/sshd_config)
Port 2222                               # Change default port
Protocol 2                              # Use SSH protocol 2
PermitRootLogin no                      # Disable root login
PasswordAuthentication no               # Use keys only
PubkeyAuthentication yes                # Enable key authentication
MaxAuthTries 3                          # Limit authentication attempts
ClientAliveInterval 300                 # Client timeout
ClientAliveCountMax 2                   # Maximum client alive messages
AllowUsers alice bob                    # Limit allowed users
DenyUsers baduser                       # Explicitly deny users

# Restart SSH service
sudo systemctl restart sshd
```

#### Two-Factor Authentication

```bash
# Install Google Authenticator PAM module
sudo apt install libpam-google-authenticator

# Configure for user
google-authenticator                     # Generate secret key and QR code

# PAM configuration (/etc/pam.d/sshd)
auth required pam_google_authenticator.so

# SSH configuration (/etc/ssh/sshd_config)
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
```

### Intrusion Detection and Prevention

#### Fail2ban Configuration

```bash
# Install fail2ban
sudo apt install fail2ban

# Configuration (/etc/fail2ban/jail.local)
[DEFAULT]
bantime = 3600                          # Ban for 1 hour
findtime = 600                          # Find failures in 10 minutes
maxretry = 3                            # Maximum retry attempts
ignoreip = 127.0.0.1/8 192.168.1.0/24  # Whitelist IPs

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3

[apache-auth]
enabled = true
port = http,https
logpath = /var/log/apache2/*error.log

# Check fail2ban status
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

#### Log Monitoring with LogWatch

```bash
# Install LogWatch
sudo apt install logwatch

# Configuration (/etc/logwatch/conf/logwatch.conf)
MailTo = admin@company.com
Range = yesterday
Detail = Med
Service = All

# Manual run
sudo logwatch --detail Med --service All --range yesterday --mailto admin@company.com
```

#### File Integrity Monitoring

```bash
# Install AIDE (Advanced Intrusion Detection Environment)
sudo apt install aide

# Initialize database
sudo aide --init
sudo mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# Configuration (/etc/aide/aide.conf)
/bin p+i+u+g+s+m+c+md5
/sbin p+i+u+g+s+m+c+md5
/usr/bin p+i+u+g+s+m+c+md5
/etc p+i+u+g+s+m+c+md5

# Check for changes
sudo aide --check

# Automate with cron
echo "0 2 * * * root /usr/bin/aide --check" >> /etc/crontab
```

### Vulnerability Management

#### System Updates and Patching

```bash
# Automated updates (Ubuntu/Debian)
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades

# Configuration (/etc/apt/apt.conf.d/50unattended-upgrades)
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
    "${distro_id}:${distro_codename}-updates";
};

# Red Hat/CentOS automatic updates
sudo yum install yum-cron
sudo systemctl enable yum-cron
sudo systemctl start yum-cron
```

#### Security Scanning

```bash
# Nmap security scanning
nmap -sS -O target.com                  # SYN scan with OS detection
nmap -sV target.com                     # Version detection
nmap --script vuln target.com           # Vulnerability scripts

# OpenVAS vulnerability scanner
sudo apt install openvas
sudo openvas-setup
```

#### Compliance Auditing

```bash
# Lynis security auditing
sudo apt install lynis
sudo lynis audit system                 # Full system audit
sudo lynis audit system --auditor "IT Security" --cronjob

# CIS benchmark checking
wget https://github.com/dev-sec/cis-dil-benchmark/archive/master.zip
# Run benchmark tests according to CIS guidelines
```

### XP Tasks - Security & Compliance

- [ ] Implement system hardening baseline configuration
- [ ] Set up SSH key authentication with 2FA
- [ ] Configure fail2ban for intrusion prevention
- [ ] Set up automated security updates
- [ ] Perform vulnerability scan on your system
- [ ] Configure file integrity monitoring
- [ ] Create security incident response procedures

---

## Module 7: Monitoring and Performance Optimization

### System Monitoring Fundamentals

#### Key Performance Indicators (KPIs)

```bash
# The four golden signals of monitoring:
# 1. Latency - Response time
# 2. Traffic - Request rate
# 3. Errors - Error rate
# 4. Saturation - Resource utilization

# System load averages
uptime                                  # Load averages (1, 5, 15 min)
w                                       # Users and load
cat /proc/loadavg                       # Raw load average data
```

#### Resource Monitoring

```bash
# CPU monitoring
top                                     # Interactive process viewer
htop                                    # Enhanced process viewer
sar -u 1 10                            # CPU utilization over time
mpstat 1 5                             # Multi-processor statistics
iostat -c 1 5                          # CPU statistics

# Memory monitoring
free -h                                 # Memory usage summary
cat /proc/meminfo                       # Detailed memory information
vmstat 1 5                             # Virtual memory statistics
sar -r 1 10                            # Memory utilization over time

# Disk I/O monitoring
iostat -x 1 5                          # Extended I/O statistics
iotop                                   # Top-like I/O monitor
sar -d 1 10                            # Disk activity
lsof +D /path                          # Files open in directory
```

### Performance Analysis Tools

#### System Analysis

```bash
# Process analysis
ps aux --sort=-%cpu | head -10          # Top CPU processes
ps aux --sort=-%mem | head -10          # Top memory processes
pgrep -l process_name                   # Find processes by name
pidstat -p PID 1 5                     # Process statistics

# Network analysis
netstat -i                             # Interface statistics
ss -s                                  # Socket summary
sar -n DEV 1 10                        # Network device statistics
iftop                                  # Bandwidth usage by connection
nethogs                                # Network usage by process
```

#### Advanced Performance Tools

```bash
# Perf - Linux profiling tool
perf top                               # Real-time performance counters
perf record -g command                 # Record performance data
perf report                            # Analyze recorded data

# Strace - System call tracer
strace -p PID                          # Trace system calls of process
strace -c command                      # Count system calls
strace -e open,read,write command      # Trace specific system calls

# Ltrace - Library call tracer
ltrace -p PID                          # Trace library calls
ltrace -c command                      # Count library calls
```

### Monitoring Infrastructure

#### Nagios Core Setup

```bash
# Install Nagios Core
sudo apt install nagios4 nagios-plugins-contrib nagios-nrpe-plugin

# Main configuration (/etc/nagios4/nagios.cfg)
log_file=/var/log/nagios4/nagios.log
cfg_file=/etc/nagios4/objects/commands.cfg
cfg_file=/etc/nagios4/objects/contacts.cfg
cfg_file=/etc/nagios4/objects/timeperiods.cfg
cfg_file=/etc/nagios4/objects/templates.cfg
cfg_dir=/etc/nagios4/conf.d

# Define hosts (/etc/nagios4/conf.d/hosts.cfg)
define host {
    use                     linux-server
    host_name               webserver1
    alias                   Web Server 1
    address                 192.168.1.10
    contact_groups          admins
}

# Define services (/etc/nagios4/conf.d/services.cfg)
define service {
    use                     generic-service
    host_name               webserver1
    service_description     HTTP
    check_command           check_http
    contact_groups          admins
}
```

#### Zabbix Monitoring Setup

```bash
# Install Zabbix server
wget https://repo.zabbix.com/zabbix/5.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_5.4-1+ubuntu20.04_all.deb
sudo dpkg -i zabbix-release_5.4-1+ubuntu20.04_all.deb
sudo apt update
sudo apt install zabbix-server-mysql zabbix-frontend-php zabbix-nginx-conf zabbix-sql-scripts zabbix-agent

# Configure database
mysql -uroot -p
create database zabbix character set utf8 collate utf8_bin;
create user zabbix@localhost identified by 'password';
grant all privileges on zabbix.* to zabbix@localhost;
quit;

# Import initial schema
zcat /usr/share/doc/zabbix-sql-scripts/mysql/create.sql.gz | mysql -uzabbix -p zabbix
```

#### Prometheus and Grafana

```bash
# Install Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.30.3/prometheus-2.30.3.linux-amd64.tar.gz
tar xvf prometheus-2.30.3.linux-amd64.tar.gz
sudo mv prometheus-2.30.3.linux-amd64 /opt/prometheus

# Prometheus configuration (prometheus.yml)
global:
  scrape_interval: 15s

rule_files:
  - "first_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

# Install Node Exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.2.2/node_exporter-1.2.2.linux-amd64.tar.gz
tar xvf node_exporter-1.2.2.linux-amd64.tar.gz
sudo mv node_exporter-1.2.2.linux-amd64/node_exporter /usr/local/bin/
```

### Log Management

#### Centralized Logging with rsyslog

```bash
# Server configuration (/etc/rsyslog.conf)
# Enable UDP reception
$ModLoad imudp
$UDPServerRun 514
$UDPServerAddress 0.0.0.0

# Template for log format
$template DynamicFile,"/var/log/remote/%HOSTNAME%/%programname%.log"
*.* ?DynamicFile

# Client configuration
# Send logs to central server
*.* @@logserver:514

# Restart rsyslog
sudo systemctl restart rsyslog
```

#### ELK Stack (Elasticsearch, Logstash, Kibana)

```bash
# Install Elasticsearch
curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elastic.gpg
echo "deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt update && sudo apt install elasticsearch

# Install Logstash
sudo apt install logstash

# Install Kibana
sudo apt install kibana

# Logstash configuration (/etc/logstash/conf.d/apache.conf)
input {
  file {
    path => "/var/log/apache2/access.log"
    start_position => "beginning"
  }
}

filter {
  grok {
    match => { "message" => "%{COMBINEDAPACHELOG}" }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
  }
}
```

### Performance Optimization

#### System Tuning

```bash
# CPU optimization
# Set CPU governor to performance
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Memory optimization (/etc/sysctl.conf)
vm.swappiness=10                        # Reduce swap usage
vm.vfs_cache_pressure=50               # Keep more cache
vm.dirty_ratio=15                       # Dirty memory threshold
vm.dirty_background_ratio=5             # Background dirty memory

# Network optimization
net.core.rmem_max = 16777216           # Max receive buffer
net.core.wmem_max = 16777216           # Max send buffer
net.core.netdev_max_backlog = 5000     # Network device backlog
net.ipv4.tcp_congestion_control = bbr  # BBR congestion control

# Apply changes
sudo sysctl -p
```

#### Application Performance Tuning

```bash
# Database optimization (MySQL/MariaDB)
# Configuration (/etc/mysql/my.cnf)
[mysqld]
innodb_buffer_pool_size = 1G           # InnoDB buffer pool
query_cache_size = 256M                 # Query cache
max_connections = 200                   # Maximum connections
slow_query_log = 1                      # Enable slow query log

# Web server optimization (Apache)
# Configuration (/etc/apache2/apache2.conf)
MaxRequestWorkers 400                   # Maximum worker processes
ThreadsPerChild 25                      # Threads per child process
ServerLimit 16                          # Maximum server processes

# Enable compression
LoadModule deflate_module modules/mod_deflate.so
<Location />
    SetOutputFilter DEFLATE
</Location>
```

#### Storage Performance Optimization

```bash
# I/O scheduler optimization
# For SSDs
echo noop | sudo tee /sys/block/sda/queue/scheduler

# For HDDs
echo deadline | sudo tee /sys/block/sda/queue/scheduler

# File system optimization
# Mount options for performance
/dev/sda1 / ext4 defaults,noatime,data=writeback 0 1

# SSD optimization
sudo fstrim -v /                        # Manual TRIM
sudo systemctl enable fstrim.timer      # Automatic TRIM
```

### Alerting and Notification

#### Email Alerting Setup

```bash
# Configure mail server (Postfix)
sudo apt install postfix mailutils

# Test email functionality
echo "Test message" | mail -s "Test Subject" admin@company.com

# Nagios email notifications (/etc/nagios4/objects/contacts.cfg)
define contact {
    contact_name                    admin
    use                            generic-contact
    alias                          System Administrator
    email                          admin@company.com
    service_notification_period    24x7
    host_notification_period       24x7
    service_notification_options   w,u,c,r
    host_notification_options      d,u,r
}
```

#### Slack Integration

```bash
# Nagios Slack notification script
#!/bin/bash
# slack-notify.sh

SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
HOSTNAME="$1"
SERVICE="$2"
STATE="$3"
OUTPUT="$4"

PAYLOAD="payload={\"channel\": \"#alerts\", \"username\": \"nagios\", \"text\": \"$HOSTNAME - $SERVICE is $STATE: $OUTPUT\"}"

curl -X POST --data-urlencode "$PAYLOAD" $SLACK_WEBHOOK
```

### XP Tasks - Monitoring & Performance

- [ ] Set up system resource monitoring with built-in tools
- [ ] Configure log rotation and centralized logging
- [ ] Install and configure a monitoring system (Nagios/Zabbix)
- [ ] Create performance baseline measurements
- [ ] Set up alerting for critical system events
- [ ] Optimize system performance parameters
- [ ] Implement automated performance reporting

---

## Module 8: Backup and Disaster Recovery

### Backup Strategy and Planning

#### Backup Types and Methods

```bash
# Backup types:
# Full backup - Complete copy of all data
# Incremental backup - Changes since last backup
# Differential backup - Changes since last full backup
# Snapshot backup - Point-in-time copy

# 3-2-1 Backup Rule:
# 3 copies of important data
# 2 different types of media
# 1 offsite copy
```

#### Backup Planning Considerations

- **Recovery Time Objective (RTO)**: Maximum acceptable downtime
- **Recovery Point Objective (RPO)**: Maximum acceptable data loss
- **Retention Policy**: How long to keep backups
- **Testing**: Regular restore testing
- **Documentation**: Backup and recovery procedures

### File-Level Backup Solutions

#### rsync Backups

```bash
# Basic rsync backup
rsync -av /source/ /backup/              # Archive mode, verbose

# Incremental backup with hard links
rsync -av --link-dest=/backup/previous /source/ /backup/current/

# Remote backup via SSH
rsync -av -e ssh /source/ user@server:/backup/

# Exclude files and directories
rsync -av --exclude='*.tmp' --exclude-from=exclude.txt /source/ /backup/

# Advanced rsync script
#!/bin/bash
SOURCE="/home/"
DEST="/backup/home/"
DATE=$(date +%Y%m%d_%H%M%S)
LATEST="$DEST/latest"
CURRENT="$DEST/$DATE"

# Create backup directory
mkdir -p "$CURRENT"

# Perform backup with hard links to previous backup
if [ -d "$LATEST" ]; then
    rsync -av --delete --link-dest="$LATEST" "$SOURCE" "$CURRENT"
else
    rsync -av --delete "$SOURCE" "$CURRENT"
fi

# Update latest link
rm -f "$LATEST"
ln -s "$CURRENT" "$LATEST"

# Clean old backups (keep 7 days)
find "$DEST" -maxdepth 1 -type d -name "20*" -mtime +7 -exec rm -rf {} \;
```

#### tar-based Backups

```bash
# Create compressed archive
tar -czf backup-$(date +%Y%m%d).tar.gz /home/

# Create archive with exclusions
tar --exclude='*.tmp' --exclude='/home/*/cache' -czf backup.tar.gz /home/

# Incremental backup with tar
tar -czf full-backup.tar.gz /home/
tar -czf incr-backup.tar.gz --newer-mtime="2021-01-01" /home/

# List archive contents
tar -tzf backup.tar.gz

# Extract archive
tar -xzf backup.tar.gz -C /restore/
```

### System-Level Backup Solutions

#### Disk Image Backups

```bash
# Full disk imaging with dd
sudo dd if=/dev/sda of=/backup/disk.img bs=4M status=progress

# Compressed disk image
sudo dd if=/dev/sda bs=4M status=progress | gzip > /backup/disk.img.gz

# Restore from image
sudo dd if=/backup/disk.img of=/dev/sdb bs=4M status=progress

# Partition table backup
sudo sfdisk -d /dev/sda > /backup/partition-table.txt
# Restore partition table
sudo sfdisk /dev/sda < /backup/partition-table.txt
```

#### LVM Snapshots

```bash
# Create LVM snapshot
sudo lvcreate -L 5G -s -n backup-snap /dev/vg0/root

# Mount snapshot
sudo mkdir /mnt/snapshot
sudo mount /dev/vg0/backup-snap /mnt/snapshot

# Backup from snapshot
tar -czf /backup/system-backup.tar.gz -C /mnt/snapshot .

# Remove snapshot
sudo umount /mnt/snapshot
sudo lvremove /dev/vg0/backup-snap
```

#### BTRFS Snapshots

```bash
# Create BTRFS snapshot
sudo btrfs subvolume snapshot /home /home/.snapshots/$(date +%Y%m%d_%H%M%S)

# List snapshots
sudo btrfs subvolume list /home

# Delete old snapshots
sudo btrfs subvolume delete /home/.snapshots/old_snapshot

# Send/receive for backup
sudo btrfs send /home/.snapshots/snapshot1 | ssh user@backup-server "sudo btrfs receive /backup/"
```

### Database Backup Solutions

#### MySQL/MariaDB Backups

```bash
# Full database dump
mysqldump -u root -p --all-databases > full-backup.sql
mysqldump -u root -p database_name > database-backup.sql

# Backup with binary logs for point-in-time recovery
mysqldump -u root -p --single-transaction --routines --triggers --all-databases > backup.sql

# Automated backup script
#!/bin/bash
DB_USER="backup_user"
DB_PASS="backup_password"
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Dump all databases
mysqldump -u "$DB_USER" -p"$DB_PASS" --single-transaction --routines --triggers --all-databases | gzip > "$BACKUP_DIR/mysql-backup-$DATE.sql.gz"

# Keep only 7 days of backups
find "$BACKUP_DIR" -name "mysql-backup-*.sql.gz" -mtime +7 -delete

# Backup binary logs
mysqlbinlog /var/log/mysql/mysql-bin.* | gzip > "$BACKUP_DIR/binlog-backup-$DATE.gz"
```

#### PostgreSQL Backups

```bash
# Database dump
pg_dump -U postgres database_name > database-backup.sql
pg_dumpall -U postgres > full-backup.sql

# Custom format dump
pg_dump -U postgres -Fc database_name > database-backup.dump

# Backup with WAL archiving
# postgresql.conf settings:
# wal_level = archive
# archive_mode = on
# archive_command = 'cp %p /backup/postgres/wal/%f'

# Base backup
pg_basebackup -U postgres -D /backup/postgres/base -Ft -z -P
```

### Automated Backup Systems

#### Bacula Configuration

```bash
# Install Bacula
sudo apt install bacula-server bacula-client

# Bacula Director configuration (/etc/bacula/bacula-dir.conf)
Director {
  Name = bacula-dir
  DIRport = 9101
  QueryFile = "/etc/bacula/scripts/query.sql"
  WorkingDirectory = "/var/lib/bacula"
  PidDirectory = "/var/run/bacula"
  Password = "console_password"
  Messages = Daemon
}

# File Daemon configuration (/etc/bacula/bacula-fd.conf)
FileDaemon {
  Name = client1-fd
  FDport = 9102
  WorkingDirectory = /var/lib/bacula
  Pid Directory = /var/run/bacula
  Maximum Concurrent Jobs = 20
}

# Job definition
Job {
  Name = "BackupClient1"
  Type = Backup
  Level = Incremental
  Client = client1-fd
  FileSet = "Full Set"
  Schedule = "WeeklyCycle"
  Storage = File
  Messages = Standard
  Pool = File
  Priority = 10
  Write Bootstrap = "/var/lib/bacula/%c.bsr"
}
```

#### Amanda Backup System

```bash
# Install Amanda
sudo apt install amanda-server amanda-client

# Amanda configuration (/etc/amanda/DailySet1/amanda.conf)
org "DailySet1"
mailto "admin@company.com"
dumpuser "backup"
tapecycle 7 tapes
runspercycle 1 day
tapetype HARDDISK
holdingdisk hd1 {
    comment "main holding disk"
    directory "/var/lib/amanda/holdings"
    use 1000 Mb
}

# Disk list (/etc/amanda/DailySet1/disklist)
client1.company.com /home comp-user-tar
client1.company.com /etc comp-root-tar
```

### Cloud Backup Solutions

#### AWS S3 Backup

```bash
# Install AWS CLI
sudo apt install awscli

# Configure AWS credentials
aws configure

# Sync to S3
aws s3 sync /backup/ s3://my-backup-bucket/

# Automated S3 backup script
#!/bin/bash
SOURCE="/home/"
S3_BUCKET="s3://my-backup-bucket"
DATE=$(date +%Y%m%d)

# Create local backup
tar -czf /tmp/backup-$DATE.tar.gz "$SOURCE"

# Upload to S3
aws s3 cp /tmp/backup-$DATE.tar.gz "$S3_BUCKET/"

# Clean up local file
rm /tmp/backup-$DATE.tar.gz

# Remove old backups from S3 (keep 30 days)
aws s3 ls "$S3_BUCKET/" | while read -r line; do
    createDate=`echo $line|awk {'print $1" "$2'}`
    createDate=`date -d"$createDate" +%s`
    olderThan=`date -d"30 days ago" +%s`
    if [[ $createDate -lt $olderThan ]]
    then
        fileName=`echo $line|awk {'print $4'}`
        if [[ $fileName != "" ]]
        then
            aws s3 rm "$S3_BUCKET/$fileName"
        fi
    fi
done
```

#### Google Cloud Storage Backup

```bash
# Install gsutil
curl https://sdk.cloud.google.com | bash

# Authenticate
gcloud auth login

# Sync to Google Cloud Storage
gsutil -m rsync -r -d /backup/ gs://my-backup-bucket/

# Automated backup with lifecycle management
gsutil lifecycle set lifecycle.json gs://my-backup-bucket/

# lifecycle.json
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {"age": 30}
      }
    ]
  }
}
```

### Disaster Recovery Planning

#### Business Continuity Planning

```bash
# Disaster Recovery Plan Components:
# 1. Risk Assessment
# 2. Business Impact Analysis
# 3. Recovery Strategies
# 4. Emergency Response Procedures
# 5. Testing and Maintenance

# Recovery Site Types:
# Hot Site - Fully operational backup facility
# Warm Site - Partially equipped facility
# Cold Site - Basic facility with no equipment
```

#### System Recovery Procedures

```bash
# Bare metal recovery preparation
# 1. Document hardware configuration
lshw > hardware-config.txt
lscpu > cpu-info.txt
lsblk > disk-layout.txt
ip addr show > network-config.txt

# 2. Create system rescue media
# Download SystemRescueCD or similar
# Create bootable USB with dd or similar tool

# 3. Document recovery procedures
# - Boot from rescue media
# - Restore partition table
# - Format filesystems
# - Restore data from backup
# - Reinstall bootloader
# - Test system functionality
```

### Backup Testing and Verification

#### Automated Backup Testing

```bash
#!/bin/bash
# Backup verification script

BACKUP_DIR="/backup"
TEST_DIR="/tmp/restore_test"
LOG_FILE="/var/log/backup_test.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

test_backup() {
    local backup_file=$1
    local test_dir="$TEST_DIR/$(basename "$backup_file" .tar.gz)"
    
    log "Testing backup: $backup_file"
    
    # Create test directory
    mkdir -p "$test_dir"
    
    # Extract backup
    if tar -xzf "$backup_file" -C "$test_dir"; then
        log "✓ Backup extraction successful"
    else
        log "✗ Backup extraction failed"
        return 1
    fi
    
    # Verify critical files
    critical_files=("/etc/passwd" "/etc/group" "/etc/fstab")
    for file in "${critical_files[@]}"; do
        if [ -f "$test_dir$file" ]; then
            log "✓ Critical file found: $file"
        else
            log "✗ Critical file missing: $file"
            return 1
        fi
    done
    
    # Clean up
    rm -rf "$test_dir"
    log "✓ Backup test completed successfully"
}

# Test all backup files
for backup in "$BACKUP_DIR"/*.tar.gz; do
    if [ -f "$backup" ]; then
        test_backup "$backup"
    fi
done
```

#### Database Backup Verification

```bash
#!/bin/bash
# MySQL backup verification script

BACKUP_FILE=$1
TEST_DB="backup_test_$(date +%s)"
MYSQL_USER="root"
MYSQL_PASS="password"

# Create test database
mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -e "CREATE DATABASE $TEST_DB;"

# Restore backup to test database
if mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" "$TEST_DB" < "$BACKUP_FILE"; then
    echo "✓ Backup restoration successful"
    
    # Verify table count
    table_count=$(mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$TEST_DB';")
    echo "✓ Restored $table_count tables"
    
    # Clean up test database
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -e "DROP DATABASE $TEST_DB;"
    echo "✓ Backup verification completed"
else
    echo "✗ Backup restoration failed"
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -e "DROP DATABASE IF EXISTS $TEST_DB;"
    exit 1
fi
```

### XP Tasks - Backup & Disaster Recovery

- [ ] Design a comprehensive backup strategy for a system
- [ ] Implement automated file-level backups with rsync
- [ ] Set up database backup automation
- [ ] Create and test system recovery procedures
- [ ] Configure cloud backup integration
- [ ] Develop backup verification and testing scripts
- [ ] Document disaster recovery procedures

---

## Module 9: Automation and Infrastructure as Code

### Automation Fundamentals

#### Benefits of Automation

- **Consistency**: Identical deployments every time
- **Speed**: Faster deployment and configuration
- **Reliability**: Reduced human error
- **Scalability**: Handle large-scale operations
- **Auditability**: Track changes and compliance
- **Cost Efficiency**: Reduce manual labor

#### Automation Tools Overview

```bash
# Configuration Management:
# - Ansible (Agentless, YAML-based)
# - Puppet (Agent-based, DSL)
# - Chef (Agent-based, Ruby DSL)
# - SaltStack (Agent-based, YAML/Python)

# Infrastructure as Code:
# - Terraform (Multi-cloud provisioning)
# - CloudFormation (AWS-specific)
# - Pulumi (Multiple languages)

# Orchestration:
# - Kubernetes (Container orchestration)
# - Docker Swarm (Container clustering)
# - Nomad (Workload orchestration)
```

### Ansible Configuration Management

#### Ansible Installation and Setup

```bash
# Install Ansible
sudo apt update
sudo apt install ansible

# Verify installation
ansible --version

# Create project structure
mkdir -p ansible-project/{playbooks,inventory,roles,group_vars,host_vars}
cd ansible-project

# Inventory file (inventory/hosts)
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[databases]
db1 ansible_host=192.168.1.20

[all:vars]
ansible_user=admin
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

#### Basic Ansible Playbooks

```yaml
# playbooks/webserver.yml
---
- name: Configure Web Servers
  hosts: webservers
  become: yes
  vars:
    apache_port: 80
    document_root: /var/www/html
  
  tasks:
    - name: Update package cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install Apache
      apt:
        name: apache2
        state: present
    
    - name: Start and enable Apache
      systemd:
        name: apache2
        state: started
        enabled: yes
    
    - name: Configure Apache virtual host
      template:
        src: vhost.conf.j2
        dest: /etc/apache2/sites-available/000-default.conf
      notify: restart apache
    
    - name: Create web content
      copy:
        content: |
          <html>
          <head><title>Welcome</title></head>
          <body><h1>Hello from {{ ansible_hostname }}</h1></body>
          </html>
        dest: "{{ document_root }}/index.html"
  
  handlers:
    - name: restart apache
      systemd:
        name: apache2
        state: restarted
```

#### Ansible Roles

```bash
# Create role structure
ansible-galaxy init roles/common

# roles/common/tasks/main.yml
---
- name: Update system packages
  apt:
    update_cache: yes
    upgrade: dist
  when: ansible_os_family == "Debian"

- name: Install essential packages
  package:
    name:
      - vim
      - htop
      - curl
      - wget
      - unzip
    state: present

- name: Configure timezone
  timezone:
    name: "{{ system_timezone | default('UTC') }}"

- name: Create admin user
  user:
    name: "{{ admin_user }}"
    groups: sudo
    shell: /bin/bash
    create_home: yes
  when: admin_user is defined

- name: Configure SSH key for admin user
  authorized_key:
    user: "{{ admin_user }}"
    key: "{{ admin_ssh_key }}"
  when: admin_user is defined and admin_ssh_key is defined
```

#### Advanced Ansible Features

```yaml
# playbooks/lamp-stack.yml
---
- name: Deploy LAMP Stack
  hosts: webservers
  become: yes
  vars_files:
    - vars/mysql.yml
  
  pre_tasks:
    - name: Update package cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
  
  roles:
    - common
    - apache
    - mysql
    - php
  
  post_tasks:
    - name: Verify web service
      uri:
        url: "http://{{ ansible_default_ipv4.address }}"
        status_code: 200
      delegate_to: localhost

# Using vault for sensitive data
# ansible-vault create vars/mysql.yml
mysql_root_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66386439653637343...

# Run playbook with vault
ansible-playbook -i inventory/hosts playbooks/lamp-stack.yml --ask-vault-pass
```

### Docker Containerization

#### Docker Basics

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Basic Docker commands
docker --version
docker pull nginx
docker run -d -p 80:80 --name webserver nginx
docker ps
docker logs webserver
docker exec -it webserver bash
docker stop webserver
docker rm webserver
```

#### Dockerfile Creation

```dockerfile
# Dockerfile for custom web application
FROM ubuntu:20.04

# Set maintainer
LABEL maintainer="admin@company.com"

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Update and install packages
RUN apt-get update && apt-get install -y \
    apache2 \
    php \
    libapache2-mod-php \
    php-mysql \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY src/ /var/www/html/

# Configure Apache
RUN echo 'ServerName localhost' >> /etc/apache2/apache2.conf
RUN a2enmod rewrite

# Set permissions
RUN chown -R www-data:www-data /var/www/html/
RUN chmod -R 755 /var/www/html/

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start Apache
CMD ["apache2ctl", "-D", "FOREGROUND"]
```

#### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
    volumes:
      - ./src:/var/www/html
    depends_on:
      - db
    environment:
      - DB_HOST=db
      - DB_NAME=webapp
      - DB_USER=webuser
      - DB_PASS=password
    networks:
      - webapp-network

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: webapp
      MYSQL_USER: webuser
      MYSQL_PASSWORD: password
    volumes:
      - db-data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - webapp-network

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    ports:
      - "8080:80"
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: rootpassword
    depends_on:
      - db
    networks:
      - webapp-network

volumes:
  db-data:

networks:
  webapp-network:
    driver: bridge

# Deploy application
docker-compose up -d
docker-compose ps
docker-compose logs
docker-compose down
```

### Terraform Infrastructure as Code

#### Terraform Basics

```bash
# Install Terraform
wget https://releases.hashicorp.com/terraform/1.0.0/terraform_1.0.0_linux_amd64.zip
unzip terraform_1.0.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify installation
terraform --version
```

#### Basic Terraform Configuration

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

# Data sources
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

# Resources
resource "aws_security_group" "web" {
  name_prefix = "web-sg"
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  count                  = 2
  ami                   = data.aws_ami.ubuntu.id
  instance_type         = var.instance_type
  vpc_security_group_ids = [aws_security_group.web.id]
  
  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y apache2
    systemctl start apache2
    systemctl enable apache2
    echo "<h1>Web Server ${count.index + 1}</h1>" > /var/www/html/index.html
  EOF
  
  tags = {
    Name = "web-server-${count.index + 1}"
  }
}

# Outputs
output "instance_ips" {
  description = "Public IP addresses of web servers"
  value       = aws_instance.web[*].public_ip
}
```

#### Terraform Workflow

```bash
# Initialize Terraform
terraform init

# Plan infrastructure changes
terraform plan

# Apply changes
terraform apply

# Show current state
terraform show

# Destroy infrastructure
terraform destroy
```

### CI/CD Pipeline Integration

#### GitLab CI/CD Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy
  - cleanup

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  ANSIBLE_HOST_KEY_CHECKING: "False"

before_script:
  - docker info
  - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY

build:
  stage: build
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main
    - develop

test:
  stage: test
  script:
    - docker run --rm $DOCKER_IMAGE ./run-tests.sh
  only:
    - main
    - develop

deploy_staging:
  stage: deploy
  script:
    - ansible-playbook -i inventory/staging playbooks/deploy.yml
      --extra-vars "docker_image=$DOCKER_IMAGE"
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy_production:
  stage: deploy
  script:
    - ansible-playbook -i inventory/production playbooks/deploy.yml
      --extra-vars "docker_image=$DOCKER_IMAGE"
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - main

cleanup:
  stage: cleanup
  script:
    - docker system prune -f
  when: always
```

### Monitoring and Alerting Automation

#### Automated Monitoring Setup

```yaml
# playbooks/monitoring.yml
---
- name: Setup Monitoring Stack
  hosts: monitoring
  become: yes
  vars:
    prometheus_version: "2.30.3"
    grafana_version: "8.2.0"
  
  tasks:
    - name: Create monitoring user
      user:
        name: monitoring
        system: yes
        shell: /bin/false
        home: /var/lib/monitoring
    
    - name: Install Prometheus
      unarchive:
        src: "https://github.com/prometheus/prometheus/releases/download/v{{ prometheus_version }}/prometheus-{{ prometheus_version }}.linux-amd64.tar.gz"
        dest: /opt
        remote_src: yes
        owner: monitoring
        group: monitoring
        mode: '0755'
    
    - name: Create Prometheus configuration
      template:
        src: prometheus.yml.j2
        dest: /etc/prometheus/prometheus.yml
        owner: monitoring
        group: monitoring
        mode: '0644'
      notify: restart prometheus
    
    - name: Create Prometheus systemd service
      template:
        src: prometheus.service.j2
        dest: /etc/systemd/system/prometheus.service
      notify:
        - reload systemd
        - restart prometheus
    
    - name: Install and configure Grafana
      apt:
        deb: "https://dl.grafana.com/oss/release/grafana_{{ grafana_version }}_amd64.deb"
      notify: restart grafana
  
  handlers:
    - name: reload systemd
      systemd:
        daemon_reload: yes
    
    - name: restart prometheus
      systemd:
        name: prometheus
        state: restarted
        enabled: yes
    
    - name: restart grafana
      systemd:
        name: grafana-server
        state: restarted
        enabled: yes
```

### XP Tasks - Automation & IaC

- [ ] Create an Ansible playbook to configure a web server
- [ ] Build a Docker container for a simple application
- [ ] Set up Docker Compose for multi-service application
- [ ] Write Terraform configuration for cloud infrastructure
- [ ] Implement CI/CD pipeline with automated testing
- [ ] Create automated monitoring and alerting setup
- [ ] Develop infrastructure automation for disaster recovery

---

## Module 10: Capstone Project - Complete System Administration Environment

### Project Overview

Build a comprehensive system administration environment that demonstrates mastery of all core concepts. This project will create a complete infrastructure with web services, databases, monitoring, backup, and automation.

#### Project Requirements

**Core Infrastructure:**

1. **Multi-tier Web Application** (Web, App, Database layers)
2. **Load Balancing and High Availability**
3. **Centralized Monitoring and Logging**
4. **Automated Backup and Recovery**
5. **Security Implementation**
6. **Infrastructure as Code**
7. **CI/CD Pipeline**
8. **Documentation and Procedures**

### Implementation Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │  Monitoring     │
│   (HAProxy)     │    │  (Prometheus)   │
└─────────┬───────┘    └─────────────────┘
          │
    ┌─────┴─────┐
    │           │
┌───▼────┐ ┌───▼────┐    ┌─────────────────┐
│Web-01  │ │Web-02  │    │  Log Server     │
│(Apache)│ │(Apache)│    │  (ELK Stack)    │
└───┬────┘ └───┬────┘    └─────────────────┘
    │          │
    └─────┬────┘
          │
    ┌─────▼─────┐         ┌─────────────────┐
    │  App-01   │         │  Backup Server  │
    │ (Python)  │         │  (Bacula)       │
    └─────┬─────┘         └─────────────────┘
          │
    ┌─────▼─────┐
    │   DB-01   │
    │  (MySQL)  │
    └───────────┘
```

### Phase 1: Infrastructure Setup

#### Terraform Infrastructure Provisioning

```hcl
# infrastructure/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  
  backend "s3" {
    bucket = "sysadmin-terraform-state"
    key    = "infrastructure/terraform.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC and Networking
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "sysadmin-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = {
    Terraform = "true"
    Environment = var.environment
  }
}

# Security Groups
resource "aws_security_group" "web" {
  name_prefix = "web-sg"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Launch Template
resource "aws_launch_template" "web" {
  name_prefix   = "web-template"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  
  vpc_security_group_ids = [aws_security_group.web.id]
  
  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    environment = var.environment
  }))
  
  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "web-server"
      Environment = var.environment
    }
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "web" {
  name               = "web-asg"
  vpc_zone_identifier = module.vpc.public_subnets
  target_group_arns   = [aws_lb_target_group.web.arn]
  health_check_type   = "ELB"
  
  min_size         = 2
  max_size         = 4
  desired_capacity = 2
  
  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }
}

# Application Load Balancer
resource "aws_lb" "web" {
  name               = "web-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web.id]
  subnets            = module.vpc.public_subnets
  
  enable_deletion_protection = false
}

resource "aws_lb_target_group" "web" {
  name     = "web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher            = "200"
    path               = "/health"
    port               = "traffic-port"
    protocol           = "HTTP"
    timeout            = 5
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "web" {
  load_balancer_arn = aws_lb.web.arn
  port              = "80"
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}
```

### Phase 2: Configuration Management

#### Ansible Inventory and Configuration

```ini
# inventory/production
[load_balancers]
lb-01 ansible_host=10.0.101.10

[web_servers]
web-01 ansible_host=10.0.101.11
web-02 ansible_host=10.0.101.12

[app_servers]
app-01 ansible_host=10.0.1.10

[databases]
db-01 ansible_host=10.0.1.11

[monitoring]
monitor-01 ansible_host=10.0.1.20

[logging]
log-01 ansible_host=10.0.1.21

[backup]
backup-01 ansible_host=10.0.1.22

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/sysadmin-key.pem
```

#### Complete Application Deployment Playbook

```yaml
# playbooks/deploy_application.yml
---
- name: Deploy Complete Application Stack
  hosts: all
  become: yes
  gather_facts: yes
  
  pre_tasks:
    - name: Update package cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install common packages
      apt:
        name:
          - htop
          - vim
          - curl
          - wget
          - unzip
          - ntp
        state: present

- name: Configure Load Balancer
  hosts: load_balancers
  become: yes
  roles:
    - haproxy
  vars:
    haproxy_backend_servers:
      - name: web-01
        address: "{{ hostvars['web-01']['ansible_default_ipv4']['address'] }}:80"
      - name: web-02
        address: "{{ hostvars['web-02']['ansible_default_ipv4']['address'] }}:80"

- name: Configure Web Servers
  hosts: web_servers
  become: yes
  roles:
    - apache
    - php
    - filebeat
  vars:
    apache_document_root: /var/www/html
    php_version: "7.4"

- name: Configure Application Servers
  hosts: app_servers
  become: yes
  roles:
    - python
    - gunicorn
    - filebeat
  vars:
    app_directory: /opt/webapp
    python_version: "3.9"

- name: Configure Database Servers
  hosts: databases
  become: yes
  roles:
    - mysql
    - filebeat
  vars:
    mysql_root_password: "{{ vault_mysql_root_password }}"
    mysql_databases:
      - name: webapp
        collation: utf8_general_ci
        encoding: utf8
    mysql_users:
      - name: webapp_user
        password: "{{ vault_mysql_webapp_password }}"
        priv: "webapp.*:ALL"

- name: Configure Monitoring
  hosts: monitoring
  become: yes
  roles:
    - prometheus
    - grafana
    - alertmanager
  vars:
    prometheus_targets:
      - job_name: 'web-servers'
        static_configs:
          - targets: 
            - "{{ hostvars['web-01']['ansible_default_ipv4']['address'] }}:9100"
            - "{{ hostvars['web-02']['ansible_default_ipv4']['address'] }}:9100"

- name: Configure Logging
  hosts: logging
  become: yes
  roles:
    - elasticsearch
    - logstash
    - kibana

- name: Configure Backup
  hosts: backup
  become: yes
  roles:
    - bacula-director
    - bacula-storage
  vars:
    backup_clients:
      - name: web-01
        address: "{{ hostvars['web-01']['ansible_default_ipv4']['address'] }}"
      - name: web-02
        address: "{{ hostvars['web-02']['ansible_default_ipv4']['address'] }}"
      - name: db-01
        address: "{{ hostvars['db-01']['ansible_default_ipv4']['address'] }}"
```

