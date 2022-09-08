#!/usr/bin/env python3
""" session auth module
"""
from os import getenv
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """session ethod
        """
        if not user_id or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[str(session_id)] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ethod to get user_id for the current session_id
        """
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    # def session_cookie(self, request=None) -> str:
    #     """ return session cookie from request object
    #     """
    #     if not request:
    #         return None
    #     cookie_id = getenv("SESSION_NAME", None)
    #     if not cookie_id:
    #         return None
    #     return request.cookies.get(cookie_id)