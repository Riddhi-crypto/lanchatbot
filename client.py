import socket
import threading
import json
import sys
import os
import time


class ChatClient:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.running = True

    def connect(self):
        print("=" * 50)
        print("     LAN CHATBOT CLIENT")
        print("     Riddhi Sahu | SRMIST")
        print("=" * 50)

        try:
            self.sock.connect((self.host, self.port))
            print(f"  Connected to {self.host}:{self.port}")
        except ConnectionRefusedError:
            print("  ERROR: Server not running")
            input("  Press Enter to exit...")
            sys.exit(1)
        except Exception as e:
            print(f"  ERROR: {e}")
            input("  Press Enter to exit...")
            sys.exit(1)

        print()
        self.username = input("  Enter username: ").strip()
        if not self.username:
            self.username = "User" + str(int(time.time()) % 10000)
            print(f"  Using: {self.username}")

        self.sock.sendall(json.dumps({'type': 'join', 'username': self.username}).encode('utf-8'))
        time.sleep(0.3)

        threading.Thread(target=self.receive, daemon=True).start()

        print()
        print("  Type /help for commands")
        print("-" * 50)
        print()

        self.loop()

    def receive(self):
        buf = ""
        while self.running:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                buf += data.decode('utf-8')
                while buf:
                    try:
                        msg, idx = json.JSONDecoder().raw_decode(buf)
                        buf = buf[idx:].lstrip()
                        self.show(msg)
                    except json.JSONDecodeError:
                        break
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                break
        if self.running:
            print("\n  Disconnected from server", flush=True)
            self.running = False

    def show(self, msg):
        t = msg.get('type', '')
        if t == 'chat':
            u = msg['username']
            m = msg['message']
            ts = msg.get('timestamp', '')
            if u == self.username:
                print(f"  [{ts}] You: {m}", flush=True)
            else:
                print(f"  [{ts}] {u}: {m}", flush=True)
        elif t == 'private':
            print(f"  [PM from {msg['from']}]: {msg['message']}", flush=True)
        elif t == 'private_sent':
            print(f"  [PM to {msg['to']}]: {msg['message']}", flush=True)
        elif t == 'notification':
            print(f"  *** {msg['message']} ***", flush=True)
        elif t == 'system':
            print(f"  [SERVER] {msg['message']}", flush=True)
        elif t == 'error':
            print(f"  ERROR: {msg['message']}", flush=True)

    def loop(self):
        while self.running:
            try:
                text = input("  > ").strip()
                if not text:
                    continue

                if text.lower() in ('/quit', '/exit'):
                    self.running = False
                    self.sock.close()
                    sys.exit(0)

                elif text.lower() == '/clear':
                    os.system('cls' if os.name == 'nt' else 'clear')

                elif text.lower().startswith('/pm @'):
                    rest = text[5:]
                    space = rest.find(' ')
                    if space > 0:
                        self.sock.sendall(json.dumps({
                            'type': 'private',
                            'target': rest[:space],
                            'message': rest[space+1:]
                        }).encode('utf-8'))
                    else:
                        print("  Usage: /pm @username message")

                elif text.startswith('/'):
                    self.sock.sendall(json.dumps({'type': 'command', 'command': text}).encode('utf-8'))

                else:
                    self.sock.sendall(json.dumps({'type': 'chat', 'message': text}).encode('utf-8'))

            except (KeyboardInterrupt, EOFError):
                self.running = False
                self.sock.close()
                sys.exit(0)
            except (BrokenPipeError, OSError):
                print("  Connection lost", flush=True)
                self.running = False
                sys.exit(1)


if __name__ == '__main__':
    ChatClient().connect()
