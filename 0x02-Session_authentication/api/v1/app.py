#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth

auth_env = getenv("AUTH_TYPE", None)
app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = Auth() if auth_env == "auth" else None
if auth_env == "basic_auth":
    auth = BasicAuth()
if auth_env == "session_auth":
    auth = SessionAuth()
if auth_env == "session_exp_auth":
    auth = SessionExpAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before():
    """ test for authentication
    """
    if not auth:
        return
    auth_test = auth.require_auth(request.path, [
        '/api/v1/status/', '/api/v1/unauthorized/',
        '/api/v1/forbidden/', "/api/v1/auth_session/login/"])
    if not auth_test:
        return
    if not auth.authorization_header(request)\
            and not auth.session_cookie(request):
        abort(401)
    current_user = auth.current_user(request)
    request.current_user = current_user
    if current_user is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
