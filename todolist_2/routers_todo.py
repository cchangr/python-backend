from todolist_2.utils import log
from todolist_2.todo import Todo
from todolist_2.models import User
from todolist_2.routes import current_user
from todolist_2.routes import template
from todolist_2.routes import response_with_headers
from todolist_2.routes import redirect


def index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    # find user, or redirect to /login
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_list = Todo.find_all(user_id=u.id)
    todo_html = ''.join(['<h3>{} : {} </h3>'.format(t.id, t.title)
                         for t in todo_list])
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def edit(request):
    headers = {
        'Content-Type': 'text/html',
    }
    # find user, or redirect to /login
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # get_todo id
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    body = body.replace('{{todo_title}}', str(t.title))
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def login_required(route_function):
    def f(request):
        uname = current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            return redirect('/login')
        return route_function(request)

    return f


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
    return redirect('/todo')


def update(request):
    """
    add new_todo
    """
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        # update_todo
        form = request.form()
        print('debug update', form)
        todo_id = int(form.get('id', -1))
        t = Todo.find_by(id=todo_id)
        t.title = form.get('title', t.title)
        t.save()
    return redirect('/todo')


def delete_todo(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    if t is not None:
        t.remove()
    return redirect('/todo')


route_dict = {
    # GET request, display page
    '/todo': index,
    '/todo/edit': edit,
    # POST request, deal data
    '/todo/add': login_required(add),
    '/todo/update': update,
    '/todo/delete': delete_todo,
}
