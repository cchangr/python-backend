import socket
import urllib

from server1.utils import log

from server1.routes import route_static
from server1.routes import route_dict


class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''

    def form(self):
        """
        change body to a dict and return
        username=g+u%26a%3F&password=
        username=g u&a?&password=
        """
        args = self.body.split('&')
        args = urllib.parse.unquote(args)
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f

request = Request()


def parsed_path(path):
    """
    a pth example: /index.html?message=hello&id=1
    :param path: path
    :return: path + query
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        query = {}
        args = query_string.split('&')
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    """
    :param path: path + query
    :return: response for request
    """
    path, query = parsed_path(path)
    request.path = path
    request.query = query

    r = {
        '/static': route_static
    }

    r.update(route_dict)
    response = r.get(path, error)
    return response(request)



def error(request, code=404):
    e = {
        404:b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')



def run(host, port):
    log('start host and port, {}: {}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))

        while True:
            s.listen(5)
            connection, address = s.accept()
            r = connection.recv(1024)
            r = r.decode('utf-8')
            log('Request', r)

            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            request.method = r.split()[0]
            request.body = r.split('\r\n\r\n')[1]
            response = response_for_path(path)
            connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
