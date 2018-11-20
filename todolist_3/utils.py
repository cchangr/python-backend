import time
import os
import jinja2

def log(*args, **kwargs):
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


path = '{}/templates/'.format(os.path.dirname(__file__))
loader = jinja2.FileSystemLoader(path)
env = jinja2.Environment(loader=loader)


def template(path, **kwargs):
    """
    receive path and arguments
    render template and return
    """
    t = env.get_template(path)
    return t.render(**kwargs)


def response_with_headers(headers, status_code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    return header


def redirect(location):
    headers = {
        'Content-Type': 'text/html',
    }
    headers['Location'] = location
    # 301 永久重定向 302 普通定向
    # 302 状态码的含义, Location 的作用
    header = response_with_headers(headers, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')


def error(request, code=404):
    """
    404
    """
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def http_response(body, headers=None):
    """
    headers HTTP
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v)
                            for k, v in headers.items()])
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')
