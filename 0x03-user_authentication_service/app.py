#!/usr/bin/env python3
"""app module
"""
from flask import Flask, jsonify, request
from auth import Auth
from os import urandom


app = Flask(__name__)
app.config["SECRET_KEY"] = urandom(16)
AUTH = Auth()

@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """app home page
    """
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"], strict_slashes=False)
def creat_user():
    """app user creation method
    """
    try:
        user = AUTH.register_user(request.form.get("email"), request.form.get("password"))
        if user:
            email = request.form.get("email")
            return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
