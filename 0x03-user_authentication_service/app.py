#!/usr/bin/env python3
"""app module
"""
import re
from flask import Flask, abort, jsonify, make_response, redirect, request
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
def login():
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

@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """session logout method
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        redirect("/")
    else:
        abort(403)

@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """ profile renderer
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    else:
        abort(403)

@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """ user passwort reset route
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({
            "email": f"{email}",
            "reset_token": f"{reset_token}"
        }), 200
    except ValueError:
        return abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
