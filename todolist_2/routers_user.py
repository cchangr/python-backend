from todolist_2.utils import log
from todolist_2.utils import template
from todolist_2.utils import redirect
from todolist_2.utils import http_response

from todolist_2.models import User

import random

session = {}


def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = int(session.get(session_id, '-1'))
    u = User.find_by(id=user_id)
    return u


def route_login(request):

    headers = {}
    log('login, cookies', request.cookies)

    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            user = User.find_by(username=u.username)
            session_id = random_str()
            session[session_id] = user.id
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            log('headers response', headers)
            return redirect('/', headers)

    body = template('login.html')
    return http_response(body, headers=headers)

#
# def route_register(request):
#     header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
#     if request.method == 'POST':
#         form = request.form()
#         u = User.new(form)
#         if u.validate_register():
#             u.save()
#             result = '注册成功<br> <pre>{}</pre>'.format(User.all())
#         else:
#             result = '用户名或者密码长度必须大于2'
#     else:
#         result = ''
#     body = template('register.html')
#     body = body.replace('{{result}}', result)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


def route_register(request):

    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            log('register success')
            return redirect('/login')
        else:
            return redirect('/register')
    body = template('register.html')
    return http_response(body)


def route_admin_users(request):
    u = current_user(request)
    log('admin users', u)
    if u is not None and u.is_admin():
        us = User.all()
        body = template('admin_users.html', users=us)
        return http_response(body)
    else:
        return redirect('/login')

def route_admin_user_update(request):
    form = request.form()
    user_id = int(form.get('id', -1))
    new_password = form.get('password', '')
    u = User.find_by(id=user_id)
    if u is not None:
        u.password = new_password
        u.save()
    return redirect('/admin/users')


def route_static(request):

    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


# 路由字典
route_dict = {
    '/login': route_login,
    '/register': route_register,
    '/admin/users': route_admin_users,
    '/admin/user/update': route_admin_user_update,
}
