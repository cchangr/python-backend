# log 函数
def log(*args, **kwargs):
    print(*args, **kwargs)


# 实现函数
def path_with_query(path, query):
    '''
    path: a string
    query: a dict
    :return a concat url
    '''
    result_list = []
    for k, v in query.items():
        if(result_list):
            result_list.append('&')
        result_list.append('{key}={value}'.format(key=k, value=v))
    # ['{key}={value}', '&', '{key}={value}', '&', '{key}={value}']
    if result_list:
        result_list = [path, '?'] + result_list
    # [path, '?', '{key}={value}', '&', '{key}={value}', '&', '{key}={value}']
    else:
        result_list.append(path)
    log('result_list: {}'.format(result_list))
    return ''.join(result_list)


def test_path_with_query():
    # 注意 height 是一个数字
    path = '/'
    query = {
        'name': 'gua',
        'height': 169,
    }
    expected = [
        '/?name=gua&height=169',
        '/?height=169&name=gua',
    ]
    # NOTE, 字典是无序的, 不知道哪个参数在前面, 所以这样测试
    assert path_with_query(path, query) in expected


# query: a dict
# url: a string


def get(url, query):
    pass


# 实现函数
def header_from_dict(headers):
    '''
    headers 是一个字典
    范例如下
    对于
    {
    	'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    返回如下 str
    'Content-Type: text/html\r\nContent-Length: 127\r\n'
    '''
    result_list = ['{key}: {value}\r\n'.format(key=k, value = v) for k, v in headers.items()]
    return ''.join(result_list)



