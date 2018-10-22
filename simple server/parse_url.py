import socket
import ssl


def parsed_url(url):
    """
    :param url:
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
    pass


def response_by_socket(s):
    pass


def parsed_response(r):
    pass


def get(url):
    pass


def main():
    url = 'http://movie.douban.com/top250'


def test():
    pass


if __name__ == '__main__':
    test()
