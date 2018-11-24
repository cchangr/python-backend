from todolist_3.models import User, Weibo
from todolist_3.utils import redirect, error
from todolist_3.utils import log
from todolist_3.utils import template
from todolist_3.utils import http_response
from todolist_3.session import session


def login_required(route_fuction):
    def func(request):
        uid = current_user(request)
        log('log in vertification', uid)
        if uid == -1:
            return redirect('/login')
        else:
            return route_fuction(request)
    return func

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
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id, -1)
    return user_id


def new(request):
    uid = current_user(request)
    user = User.find(uid)
    body = template('weibo_new.html')
    return http_response(body)


def edit(request):
    weibo_id = request.query.get('id', -1)
    weibo_id = int(weibo_id)
    w = Weibo.find(weibo_id)
    if w is None:
        return error(request)
    # 生成一个 edit 页面
    body = template('weibo_edit.html',
                    weibo_id=w.id,
                    weibo_content=w.content)
    return http_response(body)


def add(request):
    uid = current_user(request)
    user = User.find(uid)

    form = request.form()
    w = Weibo(form)
    w.user_id = user.id
    w.save()
    return redirect('/weibo/index?user_id={}'.format(user.id))


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
