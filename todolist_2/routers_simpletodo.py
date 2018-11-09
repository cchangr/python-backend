from todolist_2.utils import log
from todolist_2.utils import template
from todolist_2.utils import redirect
from todolist_2.utils import http_response
from todolist_2.models import Todo

def index(request):
    todo_list = Todo.all()
    body = template('simple_todo_index.html', todos = todo_list)
    return http_response(body)


def add(request):
    form = request.form
    Todo.new(form)
    return redirect('/')


def edit(request):
    todo_id = int(request.form.get('id', -1))
    t = Todo.find_by(id=todo_id)
    body = template('simple_todo_edit.html', todo=t)
    return http_response(body)


def update(request):
    todo_id = int(request.form.get('id'))
    t = Todo.find_by(id = todo_id)
    t.task = request.form.get('task')
    t.save()
    return redirect('/')


def delete(request):
    todo_id = int(request.form.get('id', -1))
    Todo.delete(id=todo_id)
    return redirect('/')



route_dict = {
    '/': index,
    '/add': add,
    '/edit': edit,
    '/update': update,
    '/delete': delete,
}