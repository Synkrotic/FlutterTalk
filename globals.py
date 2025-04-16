import json
from typing import Any

from flask import Flask, Response, Request
app = Flask(__name__)
ADMIN = data = {
    "id": 1,
    "account_name": "ADMIN",
    "password": "_",
    "display_name": "ADMIN",
    "bio": "ADMIN",
    "profile_pic": 999999999999999999,
    "location": "ADMIN"
}
ADMIN_TOKEN = "ADMIN"

class Cookie:
    def __init__(self, key, content, httponly=False, duration=None):
        self.content = content
        self.httponly = httponly
        self.duration = duration
        self.key = key
        pass
    
    def add(self, response: Response):
        response.set_cookie(self.key, json.dumps(self.content), httponly=self.httponly, expires=self.duration)
        pass


def addCookie(cookies: list[Cookie], new) -> list[Cookie]:
    if cookies is None:
        cookies = []
    cookies.append(new)
    return cookies


def addCookiesToResponse(cookies: list[Cookie], response: Response) -> Response:
    if cookies is None:
        return response
    for cookie in cookies:
        cookie.add(response)
    
    return response

def getCookie(request: Request, key: str) -> Any | None:
    if request.cookies.get(key) is None:
        return None
    return json.loads(request.cookies.get(key))
