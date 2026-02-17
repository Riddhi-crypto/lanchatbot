# 💬 LAN Chatbot — Real-Time PC-to-PC Chat Application

> A multi-threaded, real-time chat application that enables communication between multiple PCs over a Local Area Network (LAN) using Python Socket Programming.

**Author:** Riddhi Sahu | RA2311030020069  
**Programme:** B.Tech CSE (Cybersecurity) | Third Year  
**Institution:** SRM Institute of Science and Technology, Ramapuram, Chennai

---

## 📌 Project Overview

LAN Chatbot is a client-server chat application built using Python's `socket` and `threading` modules. It allows multiple users connected to the same Local Area Network to communicate in real-time. The project includes both a **terminal-based client** and a **web-based GUI** (built with Flask + Socket.IO).

### Key Features

| Feature | Description |
|---------|-------------|
| Multi-client support | Multiple users can connect and chat simultaneously |
| Real-time messaging | Instant message delivery using TCP sockets |
| Private messaging | Send direct messages using `/pm @username message` |
| Web-based GUI | Modern, responsive chat interface in the browser |
| Terminal client | Lightweight CLI client for terminal users |
| User management | Join/leave notifications, online user list |
| Typing indicators | See when someone is typing (web GUI) |
| Chat history | Last 50 messages loaded for new users |
| Server commands | `/users`, `/stats`, `/help`, `/broadcast` |
| Color-coded output | ANSI colored terminal output for readability |
| Connection logging | Server logs all events with timestamps |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    LAN (Local Network)                   │
│                                                          │
│  ┌──────────┐     ┌──────────────┐     ┌──────────┐     │
│  │ Client 1 │────▶│              │◀────│ Client 2 │     │
│  │(Terminal) │     │   SERVER     │     │  (Web)   │     │
│  └──────────┘     │  (TCP/5000)  │     └──────────┘     │
│                   │  or          │                       │
│  ┌──────────┐     │  (HTTP/8080) │     ┌──────────┐     │
│  │ Client 3 │────▶│              │◀────│ Client 4 │     │
│  │  (Web)   │     └──────────────┘     │(Terminal) │     │
│  └──────────┘                          └──────────┘     │
└─────────────────────────────────────────────────────────┘
```

### Communication Flow

1. **Server** starts and listens on a specified port
2. **Clients** connect to the server's IP address
3. Client sends a **join** message with their username
4. Server **broadcasts** the join event to all connected clients
5. When a client sends a message, the server **relays** it to all other clients
6. Private messages are routed **directly** to the target client
7. On disconnect, the server **notifies** all remaining clients

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| Networking | `socket` (TCP/IP) |
| Concurrency | `threading` (multi-threaded) |
| Protocol | JSON over TCP |
| Web Framework | Flask |
| Real-time Web | Flask-SocketIO |
| Frontend | HTML5, CSS3, JavaScript |
| Data Format | JSON |

---

## 📁 Project Structure

```
lan-chatbot/
├── server.py              # TCP server (terminal mode)
├── client.py              # TCP client (terminal mode)
├── web_app.py             # Flask + SocketIO web server
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── templates/
│   └── index.html         # Web GUI (login + chat interface)
└── docs/
    └── project_report.md  # Detailed project report
```

---

## 🚀 How to Run

### Prerequisites

- Python 3.8 or above
- Two or more PCs on the **same LAN** (or use `localhost` for testing)

### Option 1: Terminal Mode (Socket-based)

**Step 1 — Start the server:**
```bash
python server.py
```

**Step 2 — Connect clients (on same or different PCs):**
```bash
# On same machine (testing)
python client.py

# On another PC in the LAN
python client.py --host 192.168.1.100
```

### Option 2: Web GUI Mode (Flask + SocketIO)

**Step 1 — Install dependencies:**
```bash
pip install -r requirements.txt
```

**Step 2 — Start the web server:**
```bash
python web_app.py
```

**Step 3 — Open browser:**
```
http://localhost:8080
```
Share your IP (e.g., `http://192.168.1.100:8080`) with others on the LAN.

---

## 💻 Commands Reference

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/users` | List all online users |
| `/pm @user message` | Send a private message |
| `/stats` | Show server statistics |
| `/clear` | Clear chat screen (terminal) |
| `/quit` | Disconnect from server |

### Server-side Commands

| Command | Description |
|---------|-------------|
| `/users` | List connected users |
| `/broadcast msg` | Send message to all users |
| `/quit` | Shut down server |

---

## 📸 Screenshots

### Web GUI — Login Screen
- Clean, modern login interface with Google-inspired design
- Username validation and duplicate checking

### Web GUI — Chat Interface
- Real-time messaging with color-coded usernames
- Online user sidebar with status indicators
- Typing indicators and message timestamps
- Private message support with purple highlighting

### Terminal Client
- ANSI color-coded messages
- Join/leave notifications
- Command support

---

## 🔧 Technical Concepts Used

1. **Socket Programming (TCP/IP):** Creating server and client sockets, binding, listening, accepting connections, and data transmission using Python's `socket` module.

2. **Multi-threading:** Using `threading` module to handle multiple client connections concurrently without blocking.

3. **JSON Protocol:** All messages are serialized as JSON objects for structured communication between server and clients.

4. **Event-driven Architecture:** Flask-SocketIO uses WebSocket protocol for real-time, bidirectional communication in the web interface.

5. **Mutex Locks:** Thread-safe operations on shared data (client list) using `threading.Lock()`.

6. **Client-Server Model:** Classic network architecture where the server acts as a central hub routing messages between clients.

---

## 🔮 Future Enhancements

- [ ] End-to-end encryption using AES/RSA
- [ ] File sharing between clients
- [ ] Chat rooms / channels support
- [ ] Message persistence with SQLite database
- [ ] User authentication with passwords
- [ ] Voice message support
- [ ] Deploy as a desktop app using Electron/PyQt

---

## 📄 License

This project is developed as part of the academic curriculum at SRMIST, Ramapuram, Chennai.

---

## 👤 Author

**Riddhi Sahu**  
B.Tech CSE (Cybersecurity), Third Year  
SRM Institute of Science and Technology, Ramapuram, Chennai  
Roll No: RA2311030020069  
Email: riddhi2379@gmail.com | rs0163@srmist.edu.in  
GitHub: [github.com/Riddhi-crypto](https://github.com/Riddhi-crypto)  
LinkedIn: [linkedin.com/in/riddhi-sahu-158276296](https://www.linkedin.com/in/riddhi-sahu-158276296/)
