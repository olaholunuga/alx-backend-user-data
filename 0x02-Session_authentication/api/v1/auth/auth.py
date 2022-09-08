#!/usr/bin/env python3
"""auth class module
"""
from os import getenv
from flask import request
from typing import List, TypeVar


class Auth():
    """auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ method to test if authenticated
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        if path[:-1] in excluded_paths:
            return False
        if path + "/" in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ request: flask request object
        return: None
        """
        auth_key = request.headers.get("Authorization")
        if request is None:
            return None
        if auth_key is None:
            return None
        return auth_key

    def current_user(self, request=None) -> TypeVar('User'):
        """ request: flask request object
        return: None
        """
        return None

    def session_cookie(self, request=None) -> str:
        """ return session cookie from request object
        """
        if not request:
            return None
        cookie_id = getenv("SESSION_NAME", None)
        if not cookie_id:
            return None
        return request.cookies.get(cookie_id)
