#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

user = auth.register_user(email, password)

print(auth.create_session(email))
print(user.session_id)
print(auth.create_session("unknown@email.com"))