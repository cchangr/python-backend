import json

from server1.utils import log

def save(data, path):
    """
    :param data: received data
    :param path: received path to store data
    :return: null
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'W+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    """
    :param path: path to load files
    :return: a dict or list
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.load(s)


# Model is the base clas to store data
class Model(object):

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'db/{}.text'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]

    def save(self):
        """
        save all instance in models
        """
        models = self.all()
        log('models', models)
        models.append(self)
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{}>\n'.format(classname, s)
