from todolist.utils import log
from todolist.todo import Todo
from todolist.models import User
from todolist.routes import current_user

def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    read file in templates and return
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def response_with_headers(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    return header


def redirect(url):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    headers = {
        'Location': url,
    }
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意, 没有 HTTP body 部分
    r = response_with_headers(headers, 302) + '\r\n'
    return r.encode('utf-8')

def index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username = uname)
    if u is None:
        return redirect('/login')
    todo_list = Todo.find_all(user_id = u.id)
    todo_html = ''.join(['<h3>{} : {} </h3>'.format(t.id, t.title)
                         for t in todo_list])
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)
    headers = response_with_headers(headers)
    r = headers + '\r\n' + body
    return r.encode(encoding='utf-8')


def edit(request):
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    body = body.replace('{{todo_title}}', str(t.title))
    # 下面 3 行可以改写为一条函数, 还把 headers 也放进函数中
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def add(request):
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if request.method == 'POST':
        # 'title=aaa'
        # {'title': 'aaa'}
        form = request.form()
        t = Todo.new(form)
        t.user_id = u.id
        t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


def update(request):
    """
    用于增加新todo的路由函数
    """
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        # 修改并且保存todo
        form = request.form()
        print('debug update', form)
        todo_id = int(form.get('id', -1))
        t = Todo.find_by(id=todo_id)
        t.title = form.get('title', t.title)
        t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


def delete_todo(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 得到当前编辑的todo的id
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    if t is not None:
        t.remove()
    return redirect('/todo')


def login_required(route_function):
    def f(request):
        uname = current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            return redirect('/login')
        return route_function(request)

    return f




route_dict = {
    # GET request, 显示页面
    '/todo': index,
    '/todo/edit': edit,
    # POST request, 处理数据
    '/todo/add': login_required(add),
    '/todo/update': update,
    '/todo/delete': delete_todo,
}
