import json
import platform

import flask
from werkzeug.wrappers import Request, Response

"""
Response based on [ealen/echo-server](https://hub.docker.com/r/ealen/echo-server).

It is not fully compatible, but it similar.

{
    "host": {
      "hostname": "localhost",
      "ip": "::ffff:172.17.0.1",
      "ips":[]
    },
    "http": {
        "method": "GET",
        "baseUrl": "",
        "originalUrl": "/",
        "protocol": "http"
    },
    "request": {
        "params": {
            "0": "/"
        },
        "query": {},
        "cookies": {},
        "body": {},
        "headers": {
            "host": "localhost:7000",
            "user-agent": "curl/7.81.0",
            "accept": "*/*"
        }
    },
    "environment": {
        "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "HOSTNAME": "aa72f2763b35",
        "NODE_VERSION": "16.16.0",
        "YARN_VERSION": "1.22.19",
        "HOME": "/root"
}
"""


class EchoMiddleware:
    def __init__(
        self, app, environment_ignore_prefixes=("wsgi.", "uwsgi.", "werkzeug.")
    ):
        self.app = app
        self.environment_ignore_prefixes = environment_ignore_prefixes

    def __call__(self, environ, start_response):
        request = Request(environ)
        response_dict = {
            "host": {
                "hostname": platform.node(),
            },
            "http": {
                "method": request.method,
            },
            "request": {
                "query": {key: value for key, value in request.args.lists()},
                "cookies": {key: value for key, value in request.cookies.lists()},
                "body": request.data.decode(),
                "headers": {
                    header.lower(): value for header, value in request.headers.items()
                },
            },
            "environment": {
                key: value
                for key, value in request.environ.items()
                if not key.startswith(self.environment_ignore_prefixes)
            },
        }
        response = Response(json.dumps(response_dict), mimetype="application/json")
        return response(environ, start_response)


def create_app():
    app = flask.Flask(__name__)
    app.wsgi_app = EchoMiddleware(app.wsgi_app)
    return app


application = create_app()

if __name__ == "__main__":  # pragma: no cover
    application.run()
