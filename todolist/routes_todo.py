route_dict = {
    # GET request, 显示页面
    '/todo': index,
    '/todo/edit': edit,
    # POST request, 处理数据
    '/todo/add': login_required(add),
    '/todo/update': update,
    '/todo/delete': delete_todo,
}
