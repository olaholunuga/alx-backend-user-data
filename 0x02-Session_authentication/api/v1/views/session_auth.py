#!/usr/bin/env python3
"""session login odule
"""
from os import getenv
from flask import jsonify, request
from itsdangerous import json
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", strict_slashes=False)
def auth_session():
    """app authentication
    """
    email = request.form.get("email")
    pwd = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pwd:
        return jsonify({"error": "password missing"}), 400
    user_list = User.search({"email": email})
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404
    for user in user_list:
        if user.is_valid_password(pwd):
            user = user
            break
    if not user:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response
