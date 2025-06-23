import time

from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Send, Message
from core.utils import random_str
from fastapi import FastAPI

from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from config import settings


class MyMiddleware:
    """
    中间件
    """
    def __init__(
            self,
            app: ASGIApp
    ) -> None:
        self.app = app

    async def __call__(self, scope: dict, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return
        start_time = time.time()
        req = Request(scope, receive, send)
        if not req.session.get("session"):
            req.session.setdefault("session", random_str())

        async def send_wrapper(message: Message) -> None:
            process_time = time.time() - start_time
            if message["type"] == "http.request.start":
                headers = MutableHeaders(scope=message)
                headers.append("X-Process-Time", str(process_time))
            await send(message)
        await self.app(scope, receive, send_wrapper)


def add_middleware_handler(app: FastAPI) -> None:
    # application.add_middleware(MyMiddleware)  # type: ignore
    app.add_middleware(
        SessionMiddleware,  # type: ignore
        secret_key=settings.SESSION_SECRET_KEY,
        session_cookie=settings.SESSION_SESSION_COOKIE,
        max_age=settings.SESSION_MAX_AGE
    )
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )





