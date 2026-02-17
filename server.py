import socket
import threading
import json
import sys
import time
from datetime import datetime


class ChatServer:
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 5000
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}
        self.lock = threading.Lock()
        self.msg_count = 0

    def log(self, msg):
        ts = datetime.now().strftime('%H:%M:%S')
        print(f"  [{ts}] {msg}", flush=True)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        print("=" * 50, flush=True)
        print("      LAN CHATBOT SERVER", flush=True)
        print("      Riddhi Sahu | SRMIST", flush=True)
        print("=" * 50, flush=True)
        print(f"  Running on port {self.port}", flush=True)
        print("  Waiting for clients...", flush=True)
        print("=" * 50, flush=True)

        while True:
            try:
                conn, addr = self.server_socket.accept()
                self.log(f"Connection from {addr[0]}")
                threading.Thread(target=self.handle, args=(conn, addr), daemon=True).start()
            except KeyboardInterrupt:
                self.shutdown()
                break

    def handle(self, conn, addr):
        username = None
        try:
            raw = conn.recv(4096)
            if not raw:
                conn.close()
                return
            data = json.loads(raw.decode('utf-8'))
            if data.get('type') != 'join':
                conn.close()
                return

            username = data.get('username', '').strip()
            if not username:
                conn.sendall(json.dumps({'type': 'error', 'message': 'Empty username'}).encode('utf-8'))
                conn.close()
                return

            with self.lock:
                if username in self.clients.values():
                    conn.sendall(json.dumps({'type': 'error', 'message': f'{username} is taken'}).encode('utf-8'))
                    conn.close()
                    return
                self.clients[conn] = username

            self.log(f"{username} JOINED | Online: {len(self.clients)}")
            time.sleep(0.15)

            conn.sendall(json.dumps({
                'type': 'system',
                'message': f'Welcome {username}!',
                'online_users': list(self.clients.values()),
                'user_count': len(self.clients)
            }).encode('utf-8'))

            self.broadcast({
                'type': 'notification',
                'message': f'{username} joined the chat',
                'online_users': list(self.clients.values()),
                'user_count': len(self.clients)
            }, exclude=conn)

            while True:
                raw = conn.recv(4096)
                if not raw:
                    break
                msg = json.loads(raw.decode('utf-8'))
                self.process(conn, username, msg)

        except (ConnectionResetError, ConnectionAbortedError, json.JSONDecodeError):
            pass
        except Exception as e:
            self.log(f"Error: {e}")
        finally:
            self.remove(conn, username)

    def process(self, conn, username, msg):
        t = msg.get('type', 'chat')

        if t == 'chat':
            self.msg_count += 1
            text = msg.get('message', '')
            ts = datetime.now().strftime('%H:%M:%S')
            self.log(f"{username}: {text}")
            self.broadcast({'type': 'chat', 'username': username, 'message': text, 'timestamp': ts})

        elif t == 'private':
            target = msg.get('target', '')
            text = msg.get('message', '')
            ts = datetime.now().strftime('%H:%M:%S')
            target_conn = None
            with self.lock:
                for s, n in self.clients.items():
                    if n == target:
                        target_conn = s
                        break
            if target_conn:
                self.send(target_conn, {'type': 'private', 'from': username, 'message': text, 'timestamp': ts})
                self.send(conn, {'type': 'private_sent', 'to': target, 'message': text, 'timestamp': ts})
                self.log(f"{username} -> {target} (PM)")
            else:
                self.send(conn, {'type': 'error', 'message': f'{target} not found'})

        elif t == 'command':
            cmd = msg.get('command', '')
            if cmd == '/users':
                users = list(self.clients.values())
                self.send(conn, {'type': 'system', 'message': f"Online ({len(users)}): {', '.join(users)}"})
            elif cmd == '/help':
                self.send(conn, {'type': 'system', 'message': "/users /pm @user msg /stats /clear /quit"})
            elif cmd == '/stats':
                self.send(conn, {'type': 'system', 'message': f"Users: {len(self.clients)} | Messages: {self.msg_count}"})

    def send(self, conn, msg):
        try:
            conn.sendall(json.dumps(msg).encode('utf-8'))
        except:
            pass

    def broadcast(self, msg, exclude=None):
        data = json.dumps(msg).encode('utf-8')
        with self.lock:
            for conn in list(self.clients.keys()):
                if conn != exclude:
                    try:
                        conn.sendall(data)
                    except:
                        pass

    def remove(self, conn, username):
        with self.lock:
            self.clients.pop(conn, None)
        try:
            conn.close()
        except:
            pass
        if username:
            self.log(f"{username} LEFT | Online: {len(self.clients)}")
            self.broadcast({
                'type': 'notification',
                'message': f'{username} left the chat',
                'online_users': list(self.clients.values()),
                'user_count': len(self.clients)
            })

    def shutdown(self):
        print("\n  Shutting down...", flush=True)
        self.broadcast({'type': 'system', 'message': 'Server shutting down'})
        with self.lock:
            for s in list(self.clients.keys()):
                try: s.close()
                except: pass
        self.server_socket.close()
        sys.exit(0)


if __name__ == '__main__':
    ChatServer().start()
