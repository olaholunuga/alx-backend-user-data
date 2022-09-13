#!/usr/bin/env python3
""" Authentication module
"""
from bcrypt import checkpw, hashpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str = "") -> bytes:
    """password hashing method
    """
    return hashpw(password.encode("utf-8"), gensalt())

def _generate_uuid() -> str:
    """ uuid generator function
    """
    return uuid4().__str__()

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """create new user
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            pass

        if not user:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
        else:
            raise ValueError(f"User {email} already exists")

        return user

    def valid_login(self, email, password):
        """check for valid password
        """
        try:
            user = self._db.find_user_by(email=email)
            chk = checkpw(password.encode("utf-8"), user.hashed_password)
            if chk:
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """session creation method
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
