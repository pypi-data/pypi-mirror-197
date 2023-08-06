from typing import Awaitable

from drakaina.middlewares.base import BaseMiddleware
from drakaina.rpc_protocols import BaseRPCProtocol
from drakaina.typing_ import ASGIApplication
from drakaina.typing_ import ASGIReceive
from drakaina.typing_ import ASGIScope
from drakaina.typing_ import ASGISend
from drakaina.typing_ import WSGIApplication
from drakaina.typing_ import WSGIEnvironment
from drakaina.typing_ import WSGIResponse
from drakaina.typing_ import WSGIStartResponse


class ExceptionMiddleware(BaseMiddleware):
    """The middleware for handling unhandled exceptions in the application
    according to the RPC protocol.

    """

    __slots__ = ("handler", "_rpc_content_type")

    def __init__(
        self,
        app: ASGIApplication | WSGIApplication,
        handler: BaseRPCProtocol,
        is_async: bool = False,
    ):
        super().__init__(app=app, is_async=is_async)

        self.handler = handler
        self._rpc_content_type = self.handler.content_type

    def __wsgi_call__(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        try:
            return self.app(environ, start_response)
        except Exception as error:
            response_body = self.handler.get_raw_error(error)
            response_headers = [
                ("Content-Type", self._rpc_content_type),
                ("Content-Length", str(len(response_body))),
            ]
            start_response("200 OK", response_headers)
            return (response_body,)

    async def __asgi_call__(
        self,
        scope: ASGIScope,
        receive: ASGIReceive,
        send: ASGISend,
    ) -> Awaitable:
        try:
            await self.app(scope, receive, send)
        except Exception:
            ...
