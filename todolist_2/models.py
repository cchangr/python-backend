import json
from todolist_2.utils import log
import time


def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


class Model(object):
    """
    The base class for all model
    """

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def find_by(cls, **kwargs):
        """
        u = User.find_by(username='gua')
        """
        log('kwargs, ', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            # getattr(m, k) 等价于 m.__dict__[k]
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):
        """
        u = User.find_by(username='gua')
        """
        log('kwargs, ', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        data = []
        for m in all:
            # getattr(m, k) 等价于 m.__dict__[k]
            if v == m.__dict__[k]:
                data.append(m)
        return data

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

    def save(self):
        log('debug save')
        models = self.all()
        log('models', models)
        first_index = 0
        if self.__dict__.get('id') is None:
            if len(models) > 0:
                self.id = models[-1].id + 1
            else:
                self.id = first_index
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            if index > -1:
                models[index] = self

        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def remove(self):
        models = self.all()
        if self.__dict__.get('id') is not None:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            if index > -1:
                del models[index]

        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = int(form.get('role', 10))

    def validate_login(self):
        # return self.username == 'gua' and self.password == '123'
        u = User.find_by(username=self.username)
        # us = User.all()
        # for u in us:
        #     if u.username == self.username and u.password == self.password:
        #         return True
        # return False
        return u is not None and u.password == self.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

    def todos(self):
        ts = []
        for t in Todo.all():
            if t.user_id == self.id:
                ts.append(t)
        return ts


class Todo(Model):
    @classmethod
    def new(cls, form, user_id=-1):
        """
        :param form: a dict contains Todo_data
        :param user_id:
        :return: todo_instance
        """

        t = cls(form, user_id)
        t.save()
        return t

    @classmethod
    def update(cls, form, id):
        t = cls.find(id)
        valid_names = [
            'task',
            'completed'
        ]

        for key in form:
            if key in valid_names:
                setattr(t, key, form[key])
        t.updated_time = int(time.time())
        t.save()

    @classmethod
    def complete(cls, id, completed):

        t = cls.find(id)
        t.completed = completed
        t.save()
        return t

    def is_owner(self, id):
        return self.user_id == id

    def ct(self):
        format = '%H:%M:%S'
        value = time.localtime(self.created_time)
        dt = time.strftime(format, value)
        return dt

    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.task = form.get('task', '')
        self.completed = False
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        # 添加创建和修改时间
        self.created_time = form.get('created_time', None)
        self.updated_time = form.get('updated_time', None)
        if self.created_time is None:
            self.created_time = int(time.time())
            self.updated_time = self.created_time





















class Message(Model):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')
