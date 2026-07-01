---
tags: [networking, study-note, infrastructure]
date_created: 2026-05-28
---
# DHCP and DNS Processes

DHCP and DNS are the backbone services of any IP network, handling automatic configuration and human-friendly addressing.

---

## 📚 Core Notes
- [[OSI 7-Layer Model]] (Application Layer protocols)
- [[Common Port Numbers]] (Ports 53, 67, 68)

## 🔗 Related MOCs
- [[Networking Basics MOC]]
- [[index|🏠 Home]]

## 📖 Resources
- [CompTIA Network+ Core Services Guide]
- TCP/IP Illustrated, Volume 1 (The Protocols)

## 💡 Key Concepts

### 1. DHCP (Dynamic Host Configuration Protocol)
- **Purpose:** Automatically assigns IP addresses, subnet masks, default gateways, and DNS server addresses to client devices.
- **Ports Used:** UDP 67 (Server) and UDP 68 (Client).
- **The D-O-R-A Process:**
	1. **D - Discover (Client to All):** Client broadcasts a request looking for any available DHCP server.
	2. **O - Offer (Server to Client):** Server responds with an available IP address offer.
	3. **R - Request (Client to Server):** Client accepts the offer and asks to lease that specific IP.
	4. **A - Acknowledge (Server to Client):** Server confirms the lease setup.

### 2. DNS (Domain Name System)
- **Purpose:** Resolves human-readable domain names (e.g., `google.com`) into machine-readable IP addresses (e.g., `142.250.190.46`).
- **Ports Used:** UDP 53 (Queries) and TCP 53 (Zone transfers between servers).
- **The Resolution Hierarchy:**
	1. **Local Cache / Hosts File:** The client checks its own recent history first.
	2. **Recursive Resolver:** The ISP or local network server that fetches the answer for the client.
	3. **Root Server:** Directs the query to the correct Top-Level Domain (TLD) server based on the suffix (e.g., `.com`, `.org`).
	4. **TLD Server:** Directs the query to the Authoritative Name Server managing that specific domain.
	5. **Authoritative Name Server:** Holds the definitive DNS records and returns the final IP address.

---

## 🛠️ Essential Diagnostic Commands

### Windows Commands
- `ipconfig /release` -> Forces the client to drop its current DHCP IP lease.
- `ipconfig /renew` -> Triggers a new DHCP DORA process to request an IP.
- `ipconfig /flushdns` -> Clears out the local Windows DNS query cache.
- `nslookup google.com` -> Directly queries a DNS server to check resolution health.

### Linux / macOS Commands
- `sudo dhclient -r` -> Releases current DHCP address assignment.
- `sudo dhclient` -> Obtains a fresh DHCP address assignment.
- `dig google.com` -> Advanced tool to display detailed DNS resolution paths and records.

---

up:: [[Networking Basics MOC]]
