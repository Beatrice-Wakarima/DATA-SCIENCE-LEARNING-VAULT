---
tags: [networking, study-note, theory]
date_created: 2026-05-28
---
# OSI 7-Layer Model

The Open Systems Interconnection (OSI) model is a conceptual framework used to understand how data moves across a network. It standardizes communication protocols into seven distinct layers.

---

## 📚 Core Notes
- [[Networking Basics MOC]]
- [[TCP vs UDP]]
- [[Common Port Numbers]]

## 🔗 Related MOCs
- [[Networking Basics MOC]]
- [[index|🏠 Home]]

## 📖 Resources
- [CompTIA Network+ Objective 1.1]
- [Wireshark Packet Analysis Guide]

## 💡 Key Concepts

### 7. Application Layer
- **Purpose:** Where the user interacts with the network application.
- **Data Unit:** Data
- **Protocols/Examples:** HTTP, HTTPS, FTP, SMTP, DNS, SSH.

### 6. Presentation Layer
- **Purpose:** Formats, encrypts, and compresses data so the application layer can understand it.
- **Data Unit:** Data
- **Protocols/Examples:** SSL/TLS, JPEG, GIF, MP3, ASCII.

### 5. Session Layer
- **Purpose:** Establishes, manages, and terminates connections (sessions) between local and remote applications.
- **Data Unit:** Data
- **Protocols/Examples:** NetBIOS, RPC, PPTP.

### 4. Transport Layer
- **Purpose:** Manages end-to-end delivery of data, flow control, and error checking.
- **Data Unit:** Segments (TCP) / Datagrams (UDP)
- **Protocols/Examples:** TCP, UDP.

### 3. Network Layer
- **Purpose:** Handles logical addressing and routing of data packets across different networks.
- **Data Unit:** Packets
- **Protocols/Examples:** IPv4, IPv6, ICMP (Ping), Routers.

### 2. Data Link Layer
- **Purpose:** Handles physical addressing (MAC addresses) and error detection on a single local network segment.
- **Data Unit:** Frames
- **Protocols/Examples:** Ethernet, Wi-Fi (802.11), Switches, MAC addresses.

### 1. Physical Layer
- **Purpose:** Transmits raw bit streams over physical media (cables, radio waves, light).
- **Data Unit:** Bits
- **Protocols/Examples:** Cat6 Cables, Fiber Optics, Hubs, RJ-45 connectors.

---

## 🧠 Memory Trick (Mnemonic)
To remember the layers from top (7) to bottom (1):
> **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing
*(Application, Presentation, Session, Transport, Network, Data Link, Physical)*

To remember the layers from bottom (1) to top (7):
> **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way

---

up:: [[Networking Basics MOC]]
