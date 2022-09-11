#!/usr/bin/env python3
"""session exp authentication odule
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session Exp Auth Class
    """

    def __init__(self):
        """class init ethod
        """
        session_duration_env = getenv("SESSION_DURATION", None)
        if session_duration_env:
            try:
                self.session_duration = int(session_duration_env)
            except Exception:
                self.session_duration = 0
        else:
            self.session_duration = 0

    def create_session(self, user_id = None):
        """create session overload 
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id = None):
        """ overloaded user id for session id
        """
        user_id = super().user_id_for_session_id(session_id)
        if not session_id:
            return None
        if not user_id:
            return None
        session_cache = self.user_id_by_session_id.get(session_id)
        if not session_cache:
            return None
        user_d = session_cache.get("user_id")
        if self.session_duration <= 0:
            return user_d
        created = session_cache.get("created_at")
        if not created:
            return None
        if created + timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return user_d
