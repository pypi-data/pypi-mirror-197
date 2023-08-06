from threading import Thread
from typing import Optional

from flask import Flask, Response

import pynanto
from pynanto import Webserver
from pynanto.routes import Route


class WsFlask(Webserver):
    def __init__(self):
        super().__init__()
        self.app = Flask(__name__)
        self.thread: Optional[Thread] = None

    def _setup_route(self, route: Route):
        def func() -> Response:
            return self.to_native_response(route.callback())

        self.app.add_url_rule(route.path, route.path, func)

    def to_native_response(self, pn_response: pynanto.Response) -> Response:
        return Response(pn_response.content, status=200, content_type=pn_response.content_type)

    def _start_listen(self):
        def flask_run():
            self.app.run(host=self.host, port=self.port)

        self.thread = Thread(target=flask_run, daemon=True)
        self.thread.start()
