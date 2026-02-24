import json
import os
import hashlib
import hmac
from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
USERS_FILE = os.path.join(BASE_DIR, "users.json")

JWT_SECRET = "change_this_secret"
JWT_ALG = "HS256"
JWT_EXP_MINUTES = 60


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        return {}

    return data


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def password_is_valid(password):
    if len(password) < 8:
        return False

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    return has_upper and has_lower and has_symbol


def hash_password(password, salt):
    combo = (salt + password).encode("utf-8")
    return hashlib.sha256(combo).hexdigest()


@app.route("/register", methods=["POST"])
def register():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing username or password"}), 400

    if not password_is_valid(password):
        return jsonify({"status": "error", "message": "Password does not meet requirements"}), 400

    users = load_users()

    if username in users:
        return jsonify({"status": "error", "message": "Username already exists"}), 400

    salt = os.urandom(16).hex()
    pw_hash = hash_password(password, salt)

    users[username] = {"salt": salt, "pw_hash": pw_hash}
    save_users(users)

    return jsonify({"status": "success", "message": "User registered"}), 201


@app.route("/login", methods=["POST"])
def login():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing username or password"}), 400

    users = load_users()

    if username not in users:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    salt = users[username]["salt"]
    expected_hash = users[username]["pw_hash"]
    given_hash = hash_password(password, salt)

    if not hmac.compare_digest(given_hash, expected_hash):
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXP_MINUTES)
    token = jwt.encode({"username": username, "exp": exp}, JWT_SECRET, algorithm=JWT_ALG)

    return jsonify({"status": "success", "token": token}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)