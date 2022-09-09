#!/usr/bin/env python3
""" BasicAuth odule
"""
from base64 import b64decode
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ base64 ethod
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header.split()[0] != "Basic":
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ base64 decoder
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            header_byte = b64decode(
                base64_authorization_header
                ).decode("utf-8")
        except Exception:
            return None
        else:
            return header_byte

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """ extraction method
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        email_pwd = tuple(decoded_base64_authorization_header.partition(":"))
        return email_pwd[0], email_pwd[2]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """user user by eail or password
        """
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        user_list = User.search({"email": user_email})
        # user = user_list[0]
        # if not user:
        #     return None
        # if not user.is_valid_password(user_pwd):
        #     return None
        for user in user_list:
            if user.is_valid_password(user_pwd):
                user = user
                break
        return user

    def current_user(
            self, request=None) -> TypeVar('User'):
        """GET current user
        """
        header = self.authorization_header(request)
        base64 = self.extract_base64_authorization_header(header)
        decoded = self.decode_base64_authorization_header(base64)
        credential = self.extract_user_credentials(decoded)
        user_object = self.user_object_from_credentials(*credential)
        return user_object
