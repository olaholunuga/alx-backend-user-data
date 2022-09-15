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

    def get_user_from_session_id(self, session_id: str) -> User:
        """ get the user object of a given session id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """ destroy the session id of a given user_id
        """
        try:
            user = self._db.find_user_by(id=int(user_id))
            self._db.update_user(user.id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ get the reset password token to change password
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_token = _generate_uuid()
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ auth password reset method
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                hashed_password = _hash_password(password)
                self._db.update_user(
                                        user.id,
                                        hashed_password=hashed_password,
                                        reset_token=None)
            else:
                raise ValueError
        except NoResultFound:
            raise ValueError
