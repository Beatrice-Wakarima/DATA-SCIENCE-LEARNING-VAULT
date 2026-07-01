---
tags: [networking, study-note, ports]
date_created: 2026-05-28
---
# Common Port Numbers

Ports act as virtual doors on a device, directing network traffic to the correct application or service at the Transport Layer (Layer 4).

---

## 📚 Core Notes
- [[OSI 7-Layer Model]] (Layer 4 addressing)
- [[TCP vs UDP]]

## 🔗 Related MOCs
- [[Networking Basics MOC]]
- [[index|🏠 Home]]

## 📖 Resources
- [IANA Service Name and Transport Protocol Port Number Registry](https://iana.org)
- CompTIA A+ Core 1 Exam Objectives

## 💡 Key Concepts

### 📂 File Transfer & Remote Access Ports
* **Port 20/21 (TCP) - FTP (File Transfer Protocol):** Used to transfer files between a client and server. Port 21 is for commands/control; Port 22 is for data.
* **Port 22 (TCP) - SSH (Secure Shell) & SFTP:** Allows secure, encrypted remote command-line access.
* **Port 23 (TCP) - Telnet:** An older, insecure (unencrypted) tool for remote command-line access.
* **Port 3389 (TCP/UDP) - RDP (Remote Desktop Protocol):** Microsoft's proprietary protocol for full graphical remote desktop access.

### 🌐 Web & Core Infrastructure Ports
* **Port 53 (TCP/UDP) - DNS (Domain Name System):** Resolves human-readable domain names (like google.com) into machine-readable IP addresses.
* **Port 67/68 (UDP) - DHCP (Dynamic Host Configuration Protocol):** Automatically assigns IP addresses, subnet masks, and default gateways to devices on a network.
* **Port 80 (TCP) - HTTP (Hypertext Transfer Protocol):** Sends unencrypted web traffic.
* **Port 443 (TCP) - HTTPS (Hypertext Transfer Protocol Secure):** Sends web traffic encrypted via SSL/TLS.

### 📧 Email & Management Ports
* **Port 25 (TCP) - SMTP (Simple Mail Transfer Protocol):** Used for sending email between servers.
* **Port 110 (TCP) - POP3 (Post Office Protocol v3):** Used by clients to retrieve email from a server (downloads and typically deletes from the server).
* **Port 143 (TCP) - IMAP (Internet Message Access Protocol):** Used by clients to retrieve email from a server (keeps emails synced across multiple devices).
* **Port 161/162 (UDP) - SNMP (Simple Network Management Protocol):** Used by administrators to monitor and manage network devices like routers and switches.

---

## 📊 Summary Quick-Reference Table


| Port | Protocol | Service | Description | Security |
| :--- | :--- | :--- | :--- | :--- |
| **20/21** | TCP | FTP | File Transfer | Insecure |
| **22** | TCP | SSH / SFTP | Secure Remote Access | **Secure** |
| **23** | TCP | Telnet | Insecure Remote Access | Insecure |
| **25** | TCP | SMTP | Email Sending | Insecure |
| **53** | UDP/TCP | DNS | Name Resolution | Neutral |
| **67/68** | UDP | DHCP | IP Assignment | Neutral |
| **80** | TCP | HTTP | Web Traffic | Insecure |
| **110** | TCP | POP3 | Email Retrieval | Insecure |
| **143** | TCP | IMAP | Email Retrieval | Insecure |
| **161/162**| UDP | SNMP | Network Monitoring | Neutral |
| **443** | TCP | HTTPS | Secure Web Traffic | **Secure** |
| **3389** | TCP/UDP | RDP | Remote Desktop | **Secure** |

---

up:: [[Networking Basics MOC]]
