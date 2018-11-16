import _thread
import socket
import urllib.parse

from todolist_3.utils import log


class Request(object):
    def __init__(self):
        self.method = "GET"
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def form(self):
        """
        parse the body information
        and convert it to a dict
        :return:
        """
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        log('form debug', args, len(args))
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f

    def add_headers(self, header):
        lines = header
        for line in lines:
            k, v = line.split(': ')
            self.headers[k] = v
        self.add_cookies()

    def add_cookies(self):
        """
        height=169; user=gua
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        log('cookie', kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v


def error(request, code=404):
    """
    according code return response
    """
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    """
    example.com?message=hello&author=gua
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



def response_for_path(path, request):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)
    # according path to call route
    r = {
        '/static': route_static,
    }
    #
    r.update(simpletodo_routes)
    r.update(user_routes)
    r.update(todo_routes)
    r.update(weibo_routes)
    #
    response = r.get(path, error)
    return response(request)


def process_request(connection):
    r = connection.recv(1024)
    r = r.decode('utf-8')
    log('complete request', r)
    # check if receive the none request
    if len(r.split()) < 2:
        connection.close()

    path = r.split()[1]
    request = Request()
    request.method = r.split()[0]
    request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
    request.body = r.split('\r\n\r\n', 1)[1]

    response = response_for_path(path, request)
    connection.sendall(response)
    print('complete request send!')
    try:
        log(response.decode('utf-8').replace('\r\n', '\n'))
    except Exception as e:
        log('Exception', e)
    # 处理完请求, 关闭连接
    connection.close()
    print('close')



def run(host='', port=2000):
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(5)
        while True:
            connection, address = s.accept()
            print('connection success, use multithread to address the request', address)
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    config = dict(
        host='',
        port=2000,
    )
    run(**config)
