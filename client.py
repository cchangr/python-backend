# coding: utf-8

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s = socket.socket()
# s = ssl.wrap_socket(s)

host = 'google.com'
port = 80

s.connect((host, port))

ip, port = s.getsockname()
print('Host ip address and prot number {} {}'.format(ip, port))

http_request = 'GTE /HTTP/1.1\r\nhost: {}\r\n\r\n'.format(host)
request = http_request.encode('utf-8')
print('request', request)
s.send(request)

response = s.recv(2048)
print('response', response)
print('response', response.decode('utf-8'))
