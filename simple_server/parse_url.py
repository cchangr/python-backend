import socket
import ssl


def parsed_url(url):
    """
    this function parse the url and slice it
    :param url
    :return: protocol host port path
    """

    # http://example.com:8080/hello
    # check protocol

    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    # check path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # check port
    port_dict = {
        'http': 80,
        'https': 443,
    }
    port = port_dict[protocol]
    if ':' in host:
        h = host.split(':')
        host = h[0]
        port = h[1]

    return protocol, host, port, path


def socket_by_protocol(protocol):
    # according protocol return a socket
    if protocol == 'http':
        s = socket.socket()
    else:
        s = ssl.wrap_socket(socket.socket())

    return s


def response_by_socket(s):
    """
    :param s: a socket
    :return: response socket sata
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r

    return response


def parsed_response(r):
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)
    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v

    return status_code, headers, body


def get(url):
    """
    request url and return response
    :param url:
    :return:
    """
    protocol, host, port, path = parsed_url(url)
    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GTE {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n'.format(host, port)
    coding = 'utf-8'
    s.send(request.encode(coding))

    response = response_by_socket(s)
    print('get response: ', response)
    response = response.decode(coding)

    status_code, headers, body = parsed_response(response)
    if status_code in [301, 302]:
        url = headers['location']
        return get(url)

    return status_code, headers, body


def main():
    url = 'http://movie.douban.com/top250'
    status_code, headers, body = get(url)
    print('main', status_code)
    print('main headers ({})'.format(headers))
    print('main body', body)


def test_parsed_url():
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn/', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/', (http, host, 90, path)),
        #
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path)),
    ]
    for t in test_items:
        url, expected = t
        u = parsed_url(url)
        e = "parsed_url ERROR, ({}) ({}) ({})".format(url, u, expected)
        assert u == expected, e
        print('success')


def test_parsed_response():
    response = 'HTTP/1.1 301 Moved Permanently\r\n' \
        'Content-Type: text/html\r\n' \
        'Location: https://movie.douban.com/top250\r\n' \
        'Content-Length: 178\r\n\r\n' \
        'test body'
    status_code, header, body = parsed_response(response)
    assert status_code == 301
    assert len(list(header.keys())) == 3
    assert body == 'test body'



def test_get():
    urls = [
        'http://movie.douban.com/top250',
        'https://movie.douban.com/top250',
    ]
    for u in urls:
        get(u)

def test():
    test_get()
    test_parsed_url()
    test_parsed_response()


if __name__ == '__main__':
    test()
