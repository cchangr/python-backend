def index(request):
    pass


def edit(request):
    pass


def add(request):
    pass


def update(request):
    pass


def delete_todo(request):
    pass


def login_required(route_function):
    pass


route_dict = {
    # GET request, 显示页面
    '/todo': index,
    '/todo/edit': edit,
    # POST request, 处理数据
    '/todo/add': login_required(add),
    '/todo/update': update,
    '/todo/delete': delete_todo,
}
