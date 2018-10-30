from server1.utils import log
from server1.models.message import Message
from server1.models.user import User

import random



message_list = []

session = {
    'session id': {
        'username': 'gua',
        '过期时间': '2.22 21:00:00'
    }
}


def random_str():
    """
    生成一个随机的字符串
    """
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 是因为我懒得去翻文档来确定边界了
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '【游客】')
    # username = request.cookies.get('user', '【游客】')
    return username


def route_index(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    username = current_user(request)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def response_with_headers(headers):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 210 VERY OK\r\n'
    header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    return header


def route_login(request):
        headers = {
            'Content-Type': 'text/html',
            # 'Set-Cookie': 'height=169; gua=1; pwd=2; Path=/',
        }
        # log('login, headers', request.headers)
        log('login, cookies', request.cookies)
        username = current_user(request)
        if request.method == 'POST':
            form = request.form()
            u = User.new(form)
            if u.validate_login():
                # 设置一个随机字符串来当令牌使用
                session_id = random_str()
                session[session_id] = u.username
                headers['Set-Cookie'] = 'user={}'.format(session_id)
                # 下面是把用户名存入 cookie 中
                # headers['Set-Cookie'] = 'user={}'.format(u.username)
                result = '登录成功'
            else:
                result = '用户名或者密码错误'
        else:
            result = ''
        body = template('login.html')
        body = body.replace('{{result}}', result)
        body = body.replace('{{username}}', username)
        header = response_with_headers(headers)
        r = header + '\r\n' + body
        log('login 的响应', r)
        return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        # HTTP BODY 如下
        # username=gw123&password=123
        # 经过 request.form() 函数之后会变成一个字典
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message(request):
    """
       消息页面的路由函数
    """
    username = current_user(request)
    if username == '【游客】':
        log("**debug, route msg 未登录")
        pass
    log('本次请求的 method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        log('post', form)
        message_list.append(msg)
        # 应该在这里保存 message_list
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    # body = '<h1>消息版</h1>'
    body = template('html_basic.html')
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    <img src="/static?file=doge.gif"/>
    GET /static?file=doge.gif
    path, query = response_for_path('/static?file=doge.gif')
    path  '/static'
    query = {
        'file', 'doge.gif',
    }
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n'+ f.read()
        return img


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
}
