"""
╔══════════════════════════════════════════════════════════════╗
║          LAN CHATBOT — Web-Based GUI                         ║
║          Flask + Socket.IO                                   ║
║          Author: Riddhi Sahu | RA2311030020069               ║
╚══════════════════════════════════════════════════════════════╝

Usage:
    pip install flask flask-socketio
    python web_app.py
    Open http://localhost:8080
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'lan-chatbot-riddhi-2026'
socketio = SocketIO(app, cors_allowed_origins="*")

online_users = {}
chat_history = []
message_count = 0

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    print(f"[+] Client connected: {request.sid}")

@socketio.on('join')
def on_join(data):
    global message_count
    username = data.get('username','').strip()
    if not username:
        emit('error', {'message': 'Username cannot be empty'}); return
    if username in online_users.values():
        emit('error', {'message': f'"{username}" is taken'}); return
    online_users[request.sid] = username
    join_room('chat')
    emit('history', {'messages': chat_history[-50:]})
    emit('system', {'message': f'Welcome, {username}!', 'online_users': list(online_users.values()), 'user_count': len(online_users)})
    emit('user_joined', {'username': username, 'online_users': list(online_users.values()), 'user_count': len(online_users), 'timestamp': datetime.now().strftime('%H:%M:%S')}, room='chat', include_self=False)
    print(f"[+] {username} joined | Online: {len(online_users)}")

@socketio.on('message')
def on_message(data):
    global message_count
    username = online_users.get(request.sid, 'Anon')
    text = data.get('message','').strip()
    if not text: return
    message_count += 1
    msg = {'type':'chat','username':username,'message':text,'timestamp':datetime.now().strftime('%H:%M:%S'),'msg_id':message_count}
    chat_history.append(msg)
    if len(chat_history) > 200: del chat_history[:100]
    emit('new_message', msg, room='chat')
    print(f"[msg] {username}: {text}")

@socketio.on('private_message')
def on_private(data):
    sender = online_users.get(request.sid, 'Anon')
    target = data.get('target','')
    text = data.get('message','')
    target_sid = next((sid for sid, name in online_users.items() if name == target), None)
    if target_sid:
        ts = datetime.now().strftime('%H:%M:%S')
        emit('private_msg', {'from': sender, 'message': text, 'timestamp': ts}, room=target_sid)
        emit('private_sent', {'to': target, 'message': text, 'timestamp': ts})
    else:
        emit('error', {'message': f'User "{target}" not found'})

@socketio.on('typing')
def on_typing(data):
    username = online_users.get(request.sid,'')
    if username:
        emit('user_typing', {'username': username}, room='chat', include_self=False)

@socketio.on('disconnect')
def on_disconnect():
    username = online_users.pop(request.sid, None)
    if username:
        leave_room('chat')
        emit('user_left', {'username': username, 'online_users': list(online_users.values()), 'user_count': len(online_users)}, room='chat')
        print(f"[-] {username} left | Online: {len(online_users)}")

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════╗
║         LAN CHATBOT — Web Interface                      ║
║         Open http://localhost:8080 in browser            ║
╚══════════════════════════════════════════════════════════╝""")
    socketio.run(app, host='0.0.0.0', port=8080, debug=False, allow_unsafe_werkzeug=True)
