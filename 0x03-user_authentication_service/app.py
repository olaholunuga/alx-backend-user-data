#!/usr/bin/env python3
"""app module
"""
import email
import re
from flask import Flask, abort, jsonify, make_response, request, session
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

@app.route("/sessions", methods=["POST"], strict_slashes=False)
def sessions():
    """ session login method
    """
    password = request.form.get("password")
    email = request.form.get("email")
    login = AUTH.valid_login(email, password)
    if login:
        session_id = AUTH.create_session(email)
        resp = make_response(jsonify({"email": f"{email}", "message": "logged in"}))
        resp.set_cookie("session_id", session_id)
        return resp
    else:
        abort(401)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
