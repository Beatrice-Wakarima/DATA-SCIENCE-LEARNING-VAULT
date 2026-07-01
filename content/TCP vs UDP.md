---
tags: [networking, study-note, transport-layer]
date_created: 2026-05-28
---
# TCP vs UDP

A comparison of the two primary Transport Layer protocols used to transmit data across networks.

---

## 📚 Core Notes
- [[OSI 7-Layer Model]] (Layer 4 Protocols)
- [[Common Port Numbers]]

## 🔗 Related MOCs
- [[Networking Basics MOC]]
- [[index|🏠 Home]]

## 📖 Resources
- Professor Messer CompTIA Network+ Training
- RFC 793 (TCP) & RFC 768 (UDP)

## 💡 Key Concepts

### 1. TCP (Transmission Control Protocol)
- **Characteristics:** Connection-oriented, reliable, slower.
- **How it works:** Establishes a connection using a **3-Way Handshake** before sending data.
- **Features:** 
  - Error checking (retransmits lost data).
  - Flow control (prevents overwhelming the receiver).
  - Guarantees data arrives in the correct order.
- **Use Cases:** Web browsing (HTTP/HTTPS), Email (SMTP), File transfers (FTP), Remote access (SSH).

### 2. UDP (User Datagram Protocol)
- **Characteristics:** Connectionless, unreliable, faster ("Fire and Forget").
- **How it works:** Sends data directly to the destination without checking if the receiver is ready or if the data arrived safely.
- **Features:**
  - No handshakes or connection setup overhead.
  - No retransmission of lost packets.
  - No ordering guarantee (packets can arrive out of order).
- **Use Cases:** Live video streaming, Online gaming, Voice over IP (VoIP), DNS queries.

---

## 📊 Summary Comparison


| Feature | TCP | UDP |
| :--- | :--- | :--- |
| **Connection** | Connection-oriented | Connectionless |
| **Speed** | Slower (high overhead) | Faster (low overhead) |
| **Reliability** | Guaranteed delivery | Best-effort delivery |
| **Data Unit** | Segment | Datagram |
| **Header Size** | 20 bytes (minimum) | 8 bytes |

---

## 🤝 The TCP 3-Way Handshake
To establish a connection, TCP uses three distinct packets:
1. **SYN** (Synchronize) -> Client asks to connect.
2. **SYN-ACK** (Synchronize-Acknowledge) -> Server responds and agrees.
3. **ACK** (Acknowledge) -> Client confirms, connection established.

---

up:: [[Networking Basics MOC]]
