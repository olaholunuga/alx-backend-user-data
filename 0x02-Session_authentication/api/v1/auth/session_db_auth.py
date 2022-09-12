#!/usr/bin/env python3
"""session auth db class
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ session DB Auth
    """

    def 