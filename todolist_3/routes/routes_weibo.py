from todolist_3.models import User, Weibo
from todolist_3.utils import redirect, template, http_response


def login_required(route_fuction):
    pass


def index(request):
    user_id = request.query.get('id', -1)
    user_id = int(user_id)
    user = User.find(user_id)
    if user is None:
        return redirect('/login')
    weibos = Weibo.find_all(user_id=user_id)
    body = template('weibo_index.html', weibos=weibos, user=user)
    return http_response(body)


def current_user(request):
    pass


def new(request):
    uid = current_user(request)
    user = User.find(uid)
    body = template('weibo_new.html')
    return http_response(body)


def edit(request):
    pass


def add(request):
    pass


def update(request):
    pass


def delete(request):
    pass


def comment_add(request):
    pass


route_dict = {
    '/weibo/index': index,
    '/weibo/new': login_required(new),
    '/weibo/edit': login_required(edit),
    '/weibo/add': login_required(add),
    '/weibo/update': login_required(update),
    '/weibo/delete': login_required(delete),
    '/comment/add': login_required(comment_add),
}
