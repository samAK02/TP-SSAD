from flask import Flask, request, render_template, redirect, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, set_access_cookies, unset_jwt_cookies
)
from datetime import timedelta

app = Flask(__name__)

# --- MySQL Config ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'socialsport'
app.config['MYSQL_DB'] = 'ssadtp1'

# --- JWT Config ---
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_SAMESITE"] = "Strict"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

mysql = MySQL(app)
jwt = JWTManager(app)

# === ROUTES ===
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hashed = generate_password_hash(password)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE email = %s", (email,))
    if cur.fetchone():
        cur.close()
        return "User already exists!"
    cur.execute("INSERT INTO user (username, email, password) VALUES (%s,%s,%s)", (username, email, hashed))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    if user and check_password_hash(user[3], password):
        token = create_access_token(identity=username)
        resp = jsonify({"message": "Login successful"})
        set_access_cookies(resp, token)
        return resp
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/messages')
def messages_page():
    return render_template('messages.html')

@app.route('/api/check_token')
@jwt_required()
def check_token():
    user = get_jwt_identity()
    return jsonify({"logged_in_as": user}), 200

# === Envoi message (stockage brut sans chiffrement serveur) ===
@app.route('/api/send_message', methods=['POST'])
@jwt_required()
def send_message():
    current_user = get_jwt_identity()
    data = request.get_json() or {}
    to = data.get('to')
    subject = data.get('subject')
    content = data.get('content')
    meta = data.get('meta')
    timestamp = data.get('timestamp')

    if not to or not content or not timestamp:
        return jsonify({"error": "Missing fields"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM user WHERE username=%s", (current_user,))
    sender = cur.fetchone()
    if not sender:
        cur.close()
        return jsonify({"error": "Sender not found"}), 400
    sender_id = sender[0]

    cur.execute("SELECT id FROM user WHERE username=%s", (to,))
    receiver = cur.fetchone()
    if not receiver:
        cur.close()
        return jsonify({"error": "Receiver not found"}), 404
    receiver_id = receiver[0]

    cur.execute("""
        INSERT INTO messages (sender_id, receiver_id, subject, content, meta, timestamp)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (sender_id, receiver_id, subject, content, meta, timestamp))
    mysql.connection.commit()
    cur.close()
    return jsonify({"msg": "Message stored", "timestamp": timestamp}), 201

# === Récupération messages ===
@app.route('/api/messages', methods=['GET'])
@jwt_required()
def get_messages():
    user = get_jwt_identity()
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM user WHERE username=%s", (user,))
    row = cur.fetchone()
    if not row:
        cur.close()
        return jsonify({"messages": []}), 404
    user_id = row[0]
    cur.execute("""
        SELECT m.id,u.username,m.subject,m.content,m.meta,m.timestamp
        FROM messages m
        JOIN user u ON u.id=m.sender_id
        WHERE m.receiver_id=%s
        ORDER BY m.timestamp DESC
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    msgs = [{
        "id": r[0],
        "sender": r[1],
        "subject": r[2],
        "content": r[3],
        "meta": r[4],
        "timestamp": int(r[5]),
        "receiver_id": user_id
    } for r in rows]
    return jsonify({"messages": msgs})

@app.route('/api/messages/sent')
@jwt_required()
def get_sent():
    user = get_jwt_identity()
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM user WHERE username=%s", (user,))
    row = cur.fetchone()
    if not row:
        cur.close()
        return jsonify({"messages": []}), 404
    user_id = row[0]
    cur.execute("""
        SELECT m.id,u.username,m.subject,m.content,m.timestamp
        FROM messages m
        JOIN user u ON u.id=m.receiver_id
        WHERE m.sender_id=%s
        ORDER BY m.timestamp DESC
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    msgs = [{
        "id": r[0],
        "receiver": r[1],
        "subject": r[2],
        "content": r[3],
        "timestamp": int(r[4])
    } for r in rows]
    return jsonify({"messages": msgs})

# === Récupérer l'ID d'un utilisateur à partir de son username ===
@app.route('/api/user_id/<username>')
@jwt_required()
def get_user_id(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM user WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    if not row:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": row[0]}), 200


@app.route('/api/messages/<int:msg_id>')
@jwt_required()
def get_message_by_id(msg_id):
    user = get_jwt_identity()
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM user WHERE username=%s", (user,))
    row = cur.fetchone()
    if not row:
        cur.close()
        return jsonify({"msg": "User not found"}), 404
    user_id = row[0]
    cur.execute("""
        SELECT m.id,u.username,m.subject,m.content,m.meta,m.timestamp,m.receiver_id
        FROM messages m
        JOIN user u ON u.id=m.sender_id
        WHERE m.id=%s AND m.receiver_id=%s
    """, (msg_id, user_id))
    msg = cur.fetchone()
    cur.close()
    if not msg:
        return jsonify({"msg": "Not found"}), 404
    return jsonify({
        "id": msg[0],
        "sender": msg[1],
        "subject": msg[2],
        "content": msg[3],
        "meta": msg[4],
        "timestamp": int(msg[5]),
        "receiver_id": msg[6]
    })

@app.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(resp)
    return resp, 200

if __name__ == '__main__':
    app.run(debug=True, port=5500)

