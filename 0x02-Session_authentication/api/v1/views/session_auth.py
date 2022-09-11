#!/usr/bin/env python3
"""session login odule
"""
from os import getenv
from flask import jsonify, request, abort
from itsdangerous import json
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
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
        if not user.is_valid_password(pwd):
            return jsonify({"error": "wrong password"}), 401
    user = user_list[0]
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response


@app_views.route(
                    "/auth_session/logout",
                    methods=["DELETE"], strict_slashes=False)
def logout():
    """session logout ethod
    """
    from api.v1.app import auth
    destroyer = auth.destroy_session(request)
    if not destroyer:
        abort(404)
    return jsonify({}), 200
