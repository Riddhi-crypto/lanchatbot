# LAN Chatbot — Project Report

## 1. Introduction

### 1.1 Problem Statement
In local area network environments such as college labs, offices, and homes, there is often a need for quick, lightweight communication between PCs without relying on internet-based services. Existing solutions like WhatsApp or Slack require internet access and external accounts. This project addresses the need for a simple, self-hosted, real-time chat application that works entirely within a LAN.

### 1.2 Objective
To design and develop a multi-client, real-time chat application using Python socket programming that enables communication between multiple PCs connected to the same Local Area Network, with both terminal-based and web-based interfaces.

### 1.3 Scope
- Multi-threaded TCP server handling up to 10 simultaneous connections
- Terminal-based client for lightweight usage
- Web-based GUI client using Flask and Socket.IO
- Private messaging, user management, and server commands
- Logging and chat history

---

## 2. Literature Survey

### 2.1 Socket Programming
Socket programming is a method of communication between two computers using a network socket. A socket is one endpoint of a two-way communication link between two programs running on the network. Python's built-in `socket` module provides access to the BSD socket interface, supporting both TCP (reliable, connection-oriented) and UDP (unreliable, connectionless) protocols.

### 2.2 Client-Server Architecture
The client-server model is a distributed application structure that partitions tasks between resource providers (servers) and service requesters (clients). In this model, the server listens for incoming connections and processes requests, while clients initiate connections and send/receive data.

### 2.3 Multi-threading
Multi-threading allows concurrent execution of multiple threads within a single process. In the context of a chat server, each client connection is handled by a separate thread, enabling simultaneous communication without blocking.

### 2.4 WebSocket Protocol
WebSocket provides full-duplex communication channels over a single TCP connection. Flask-SocketIO builds on top of this to enable real-time, event-driven communication between the web browser and the server.

---

## 3. System Design

### 3.1 Architecture Diagram
```
                    ┌─────────────────┐
                    │   CHAT SERVER   │
                    │   (Python)      │
                    │                 │
                    │  ┌───────────┐  │
                    │  │ Thread    │  │
         ┌────────▶│  │ Manager   │◀─────────┐
         │         │  └───────────┘  │        │
         │         │  ┌───────────┐  │        │
         │         │  │ Message   │  │        │
         │         │  │ Router    │  │        │
         │         │  └───────────┘  │        │
         │         │  ┌───────────┐  │        │
         │         │  │ User      │  │        │
         │         │  │ Manager   │  │        │
         │         │  └───────────┘  │        │
         │         └─────────────────┘        │
         │                                    │
    ┌────┴─────┐                        ┌────┴─────┐
    │ Client 1 │                        │ Client 2 │
    │(Terminal) │                        │  (Web)   │
    └──────────┘                        └──────────┘
```

### 3.2 Data Flow
1. Client establishes TCP connection to server
2. Client sends JSON-formatted join request with username
3. Server validates username (uniqueness check)
4. Server broadcasts join notification to all clients
5. Client sends messages as JSON packets
6. Server receives, logs, and broadcasts messages
7. On disconnect, server removes client and notifies others

### 3.3 Message Protocol (JSON)
```json
// Join Request
{"type": "join", "username": "Riddhi"}

// Chat Message
{"type": "chat", "message": "Hello everyone!"}

// Private Message
{"type": "private", "target": "Alice", "message": "Hi!"}

// Server Response
{"type": "chat", "username": "Riddhi", "message": "Hello!", "timestamp": "14:30:05", "msg_id": 1}

// System Notification
{"type": "notification", "message": "Alice joined", "online_users": ["Riddhi", "Alice"], "user_count": 2}
```

---

## 4. Implementation

### 4.1 Technologies Used
| Technology | Purpose |
|-----------|---------|
| Python 3.x | Core programming language |
| `socket` module | TCP/IP networking |
| `threading` module | Concurrent client handling |
| `json` module | Message serialization |
| Flask | Web framework |
| Flask-SocketIO | WebSocket support |
| HTML/CSS/JS | Web GUI frontend |

### 4.2 Server Implementation
The server uses the `socket.AF_INET` address family (IPv4) and `socket.SOCK_STREAM` (TCP) for reliable communication. Key methods:

- `start()`: Binds to host:port and listens for connections
- `handle_client()`: Dedicated thread per client for message handling
- `process_message()`: Routes messages based on type (chat/private/command)
- `broadcast()`: Sends messages to all connected clients
- `disconnect_client()`: Cleans up on disconnection

Thread safety is ensured using `threading.Lock()` for shared data access.

### 4.3 Client Implementation (Terminal)
The terminal client creates a TCP socket and connects to the server. Two threads run concurrently:
- **Receiver thread**: Continuously listens for incoming messages
- **Sender thread**: Reads user input and transmits to server

### 4.4 Web GUI Implementation
The web interface uses Flask as the HTTP server and Flask-SocketIO for real-time communication. The frontend is a single-page application with:
- Login screen with username input
- Chat area with message bubbles (self vs. others)
- Online user sidebar
- Typing indicators
- Private message support

---

## 5. Testing

### 5.1 Test Cases

| Test Case | Input | Expected Output | Status |
|-----------|-------|-----------------|--------|
| Server startup | `python server.py` | Server running on 0.0.0.0:5000 | PASS |
| Client connection | `python client.py` | Connected, username prompt | PASS |
| Duplicate username | Same username twice | Error: username taken | PASS |
| Send message | Type "Hello" | Message broadcast to all | PASS |
| Private message | `/pm @Alice Hi` | Only Alice receives | PASS |
| User disconnect | Close client | Leave notification sent | PASS |
| Multiple clients | 3+ clients | All receive messages | PASS |
| Web GUI login | Enter username | Chat interface opens | PASS |
| Web GUI messaging | Type and send | Real-time delivery | PASS |
| Server commands | `/users`, `/stats` | Correct output | PASS |

### 5.2 Testing Environment
- OS: Windows 11 / Ubuntu 22.04
- Python: 3.10+
- Network: Local Area Network (192.168.x.x)
- Browser: Chrome, Firefox (for web GUI)

---

## 6. Results

The LAN Chatbot successfully demonstrates:
1. **Multi-client TCP communication** over a Local Area Network
2. **Real-time message delivery** with sub-second latency
3. **Concurrent handling** of multiple clients using threads
4. **User-friendly web interface** accessible via browser
5. **Private messaging** for direct user-to-user communication
6. **Robust error handling** for disconnections and invalid inputs

---

## 7. Conclusion

This project successfully implements a real-time, multi-client chat application using Python socket programming. It demonstrates key networking concepts including TCP/IP communication, multi-threading, client-server architecture, and JSON-based protocols. The addition of a web-based GUI using Flask-SocketIO makes it accessible and user-friendly. The project serves as a practical application of computer networking principles learned during the B.Tech curriculum.

### Future Enhancements
- End-to-end encryption (AES/RSA) for secure communication
- File sharing between clients
- Chat rooms and channels
- Message persistence using SQLite
- Voice messaging support

---

## 8. References

1. Kurose, J.F. & Ross, K.W. (2021). *Computer Networking: A Top-Down Approach*. Pearson.
2. Python Documentation — `socket` module: https://docs.python.org/3/library/socket.html
3. Python Documentation — `threading` module: https://docs.python.org/3/library/threading.html
4. Flask Documentation: https://flask.palletsprojects.com/
5. Flask-SocketIO Documentation: https://flask-socketio.readthedocs.io/
6. RFC 793 — Transmission Control Protocol: https://www.rfc-editor.org/rfc/rfc793

---

**Submitted by:** Riddhi Sahu (RA2311030020069)  
**Programme:** B.Tech CSE (Cybersecurity), Third Year  
**Institution:** SRM Institute of Science and Technology, Ramapuram, Chennai
