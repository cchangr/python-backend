import json
from todolist_3.utils import log


def save(data, path):
    """dumps: Serialize ``obj`` to a JSON formatted ``str``"""
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'W+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    '''json.loads: Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
       containing a JSON document) to a Python object'''
    with open(path, 'r', encoding = 'utf-8') as f:
        s = f.read()
        return json.loads(s)


# Model is a ORM(object relation mapper）
class Model(object):

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def all(cls):
       path = cls.db_path()
       models = load(path)
       ms = [cls(m) for m in models]
       return ms

    @classmethod
    def find_all(cls, **kwargs):
        pass

    @classmethod
    def find_by(cls, **kwargs):
        pass

    @classmethod
    def find(cls, id):
        pass

    @classmethod
    def delete(cls, id):
        pass

    def __repr__(self):
        pass

    def save(self):
        pass


