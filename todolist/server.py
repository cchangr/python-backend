import socket
import urllib.parse
from todolist.utils import log


class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def add_headers(self, header):
        pass

    def add_cookies(self):
        pass

    def form(self):
        pass


def run(host='', port=3000):
    log('start at: {}, {}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            r = connection.recv(1024)
            r = r.decode('utf-8')
            log('ip and request: {}, {}'.format(address, r))
            if len(r.split()) < 2:
                continue
            path = r.split()[1]

            """
            GET / HTTP/1.1 \r\n
            HOST:.......
            Connection:
            Cookie:
            \r\n\r\n
            body
            """


if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
