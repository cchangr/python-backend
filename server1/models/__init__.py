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
    pass
