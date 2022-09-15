#!/usr/bin/env python3
"""authentication service integration testing module
"""
import requests


def register_user(email: str, password: str) -> None:
    """ user registration test
    """
    data = {"email": email, "password": password}
    r = requests.post("http://0.0.0.0:5000/users", data=data)
    assert r.status_code == 200
    assert r.json() == {"email": f"{email}", "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """user login with wrong details test
    """
    data = {"email": email, "password": password}
    r = requests.post("http://0.0.0.0:5000/sessions", data=data)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """ user login test
    """
    data = {"email": email, "password": password}
    r = requests.post("http://0.0.0.0:5000/sessions", data=data)
    assert r.status_code == 200
    assert r.json() == {"email": f"{email}", "message": "logged in"}
    return r.cookies.get("session_id")


def profile_unlogged() -> None:
    """profile loging function
    """
    r = requests.get("http://0.0.0.0:5000/profile", cookies=None)
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """profile login test
    """
    cookie = {"session_id": session_id}
    r = requests.get("http://0.0.0.0:5000/profile", cookies=cookie)
    assert r.status_code == 200
    assert "email" in (r.json()).keys()


def log_out(session_id: str) -> None:
    """logout test
    """
    cookie = {"session_id": session_id}
    r = requests.delete(
            "http://0.0.0.0:5000/sessions",
            cookies=cookie,
            allow_redirects=True)
    assert r.history[-1].is_redirect is True
    assert r.history[-1].status_code == 302
    assert r.url == "http://0.0.0.0:5000/"
    # assert r.is_redirect == True
    # assert r.status_code == 302


def reset_password_token(email: str) -> str:
    """reset password test
    """
    data = {"email": email}
    r = requests.post("http://0.0.0.0:5000/reset_password", data=data)
    assert r.status_code == 200
    return (r.json()).get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password test
    """
    data = {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password}
    r = requests.put("http://0.0.0.0:5000/reset_password", data=data)
    assert r.status_code == 200
    assert r.json() == {"email": f"{email}", "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
