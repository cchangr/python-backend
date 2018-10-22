import socket

def log(*args, **kwargs):
    print('log', *args, **kwargs)


def page(name):
    with open(name, encoding='utf-8') as f:
        return f.read()


def route_index():
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello World</h1><img src="adventure.jpg"/>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_image():
    with open('adventure.jpg', 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image/jpg\r\n'
        img = header + b'\r\n' + f.read()
        return img


def route_msg():
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = page('basic.html')
    r = header + '\r\n' + body
    return  r.encode(encoding='utf-8')


def error(code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</H1>',
    }
    r = e.get(code, b'')
    return r



def response_for_path(path):
    r = {
        '/': route_index,
        '/adventure.jpg': route_image,
        '/basic.html': route_msg
    }

    response = r.get(path, error)
    return response()


def run(host, port):
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            request = connection.recv(1024)
            log('raw, ', request)
            request = request.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, request))
            try:
                path = request.split()[1]
                response = response_for_path(path)
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            connection.close()


if __name__ == '__main__':
    config = dict(
        host = '',
        port = 5000,
    )
    run(**config)
