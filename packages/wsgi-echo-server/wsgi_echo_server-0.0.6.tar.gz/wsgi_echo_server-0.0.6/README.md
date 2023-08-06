# wsgi-echo-server

A wsgi and http echo server.


## How to use

```shell
pip install wsgi-echo-server

# Running with wsgi socket
UWSGI_SOCKET=:9000 uwsgi --module wsgi_echo_server

# Running with http socket
UWSGI_HTTP_SOCKET=:9001 uwsgi --module wsgi_echo_server

# Running with wsgi and http socket
UWSGI_SOCKET=:9000 UWSGI_HTTP_SOCKET=:9001 uwsgi --module wsgi_echo_server
```
There is a docker image ready to use:

```shell
docker run -e "UWSGI_SOCKET=:9000" ghcr.io/buserbrasil/wsgi-echo-server
```

## Response

```
{
    "environment": {
        "PATH_INFO": "/",
        "QUERY_STRING": "",
        "RAW_URI": "/",
        "REMOTE_ADDR": "127.0.0.1",
        "REQUEST_METHOD": "GET",
        "REQUEST_URI": "/",
        "SCRIPT_NAME": "",
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "80",
        "SERVER_PROTOCOL": "HTTP/1.1"
    },
    "host": {
        "hostname": "mockedhostname"
    },
    "http": {
        "method": "GET"
    },
    "request": {
        "body": "",
        "cookies": {},
        "headers": {
            "host": "localhost",
            "user-agent": "werkzeug/2.2.3"
        },
        "query": {}
    }
}
```
