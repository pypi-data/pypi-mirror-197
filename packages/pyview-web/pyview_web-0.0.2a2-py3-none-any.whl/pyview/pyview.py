from starlette.applications import Starlette
from fastapi import WebSocket
from fastapi.responses import HTMLResponse
from starlette.routing import Route
import uuid
from urllib.parse import parse_qs

from pyview.live_socket import UnconnectedSocket
from .ws_handler import LiveSocketHandler
from .live_view import LiveView
from .live_routes import LiveViewLookup
from typing import Callable, Optional

RootTemplate = Callable[[str, str, Optional[str]], str]


class PyView(Starlette):
    rootTemplate: RootTemplate

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rootTemplate = defaultRootTemplate("")
        self.view_lookup = LiveViewLookup()
        self.live_handler = LiveSocketHandler(self.view_lookup)

        async def live_websocket_endpoint(websocket: WebSocket):
            await self.live_handler.handle(websocket)

        self.add_websocket_route("/live/websocket", live_websocket_endpoint)

    def add_live_view(self, path: str, view: Callable[[], LiveView]):
        async def lv(request):
            return await liveview_container(
                self.rootTemplate, self.view_lookup, request
            )

        self.view_lookup.add(path, view)
        self.routes.append(Route(path, lv, methods=["GET"]))


async def liveview_container(
    template: RootTemplate, view_lookup: LiveViewLookup, request
):
    url = request.url
    path = url.path
    lv: LiveView = view_lookup.get(path)
    s = UnconnectedSocket()
    await lv.mount(s)
    await lv.handle_params(url, parse_qs(url.query), s)
    r = await lv.render(s.context)

    return HTMLResponse(template(str(uuid.uuid4()), r.text(), s.live_title))


def defaultRootTemplate(css: str) -> RootTemplate:
    def template(
        id: str,
        content: str,
        title: Optional[str],
    ) -> str:
        return _defaultRootTemplate(id, content, title, css)

    return template


def _defaultRootTemplate(id: str, content: str, title: Optional[str], css: str) -> str:
    suffix = " | LiveView"
    render_title = title + suffix if title else "LiveView"
    return f"""
<!DOCTYPE html>
<html>
    <head>
      <title data-suffix="{suffix}">{render_title}</title>
      <meta name="csrf-token" content="TEST_TOKEN" />
      <meta charset="utf-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <script type="text/javascript" src="/static/assets/app.js"></script>
      {css}
    </head>
    <body>
    <div>
      <a href="/">Home</a>
      <div
        data-phx-main="true"
        data-phx-session=""
        data-phx-static=""
        id="phx-{id}"
        >
        {content}
    </div>
    </div>
    </body>
</html>
"""
