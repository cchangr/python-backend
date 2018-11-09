import socket
import urllib.parse

# a class to save the request information
from todolist_2.utils import log

from todolist_2.routes_static import route_dict
from todolist_2.routers_simpletodo import route_dict as simpletodo_routes
from todolist_2.routers_user import route_dict as user_routes


class Request(object):
    def __init__(self):
        self.method = "GET"
        self.path = ''
        self.query = {}
        self.body = {}
        self.headers = {}
        self.cookies = {}

    # form save the body information and transfer it to a dict
    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f

    def add_headers(self, header):
        """
        [
            'Accept-Language: zh-CN,zh;q=0.8'
            'Cookie: height=169; user=gua'
        ]
        """
        self.headers = {}
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        self.cookies = {}
        self.add_cookies()

    def add_cookies(self):
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        log('cookie', kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v


request = Request()


def parsed_path(path):
    """
    message=hello&author=gua
    {
        'message': 'hello',
        'author': 'gua',
    }
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def error(request, code=404):
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)
    r = {
        '/static': route_dict
    }

    r.update(simpletodo_routes)
    r.update(user_routes)
    response = r.get(path, error)
    return response(request)


# main program
def run(host, port):
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))

        while True:
            s.listen(5)
            connection, address = s.accept()
            r = connection.recv(1024)
            r = r.decode(encoding='utf-8')
            log('ip and request: {}\n{}'.format(address, r))
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            request.method = r.split()[0]
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
            request.body = r.split('\r\n\r\n', 1)[1]
            response = response_for_path(path)
            log('**debug', 'send all')
            connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    config = dict(
        host = '',
        port = 5000,
    )
    run(**config)
