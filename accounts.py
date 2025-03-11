from flask import Request


def linkOrCreateSession(request: Request) -> str:
    if request.cookies.get("session") is None:
        request.cookies["session"] = secrets.token_hex(16)
    return request.cookies.get("session")