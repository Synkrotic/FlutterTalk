from flask import Flask, Response

app = Flask(__name__)


class Cookie:
    def __init__(self, content, httponly=False, duration=None):
        self.content = content
        self.httponly = httponly
        self.duration = duration
        pass

    def add(self, response: Response):
        response.set_cookie('token', self.content, httponly=self.httponly, expires=self.duration)
        pass

def addCookie(cookies: list[Cookie], new) -> list[Cookie]:
    if cookies is None:
        cookies = []
    cookies.append(new)
    return cookies

def addCookiesToResponse(cookies: list[Cookie], response: Response):
    if cookies is None:
        return
    for cookie in cookies:
        cookie.add(response)