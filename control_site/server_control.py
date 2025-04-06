from control_site.ServerController import ServerController
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong random value

server = ServerController()

# --- User Management ---
def load_users():
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            json.dump({}, f)
    with open('users.json', 'r') as f:
        return json.load(f)

users = load_users()

def verify_user(username: str, password: str) -> bool:
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return username in users and users[username] == hashed

# --- Auth Flow ---
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')
    if verify_user(username, password):
        session['username'] = username
        flash('Login successful!', 'success')
    else:
        flash('Invalid username or password.', 'error')
    return redirect(url_for('index'))

# --- Server Action Flow ---
def handle_action():
    action = request.form.get('action')
    if action == 'toggle':
        server.toggle()
        flash(f"Server {'started' if server.status() else 'stopped'}.", 'info')
    elif action == 'logout':
        session.pop('username', None)
        flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not session.get('username'):
            return handle_login()
        else:
            return handle_action()

    return render_template('index.html', server_status=server.status())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
