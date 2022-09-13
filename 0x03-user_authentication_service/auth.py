#!/usr/bin/env python3
""" Authentication module
"""
import bcrypt
from db import DB


def _hash_password(password: str = "") -> bytes:
    """password hashing method
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()