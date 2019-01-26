import re
from unidecode import unidecode


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def split_tags(string, delimiter=','):
    """
    Split tags by comma an return them as a list
    """
    return string.strip().split(delimiter)


def join_tags(list, delimiter=','):
    """
    Join tags and return them as a string
    """
    return delimiter.join(list)


def slugify(string, delim=u'-'):
    """
    Generates an ASCII-only slug.
    http://flask.pocoo.org/snippets/5/
    """
    result = []
    for word in _punct_re.split(string.lower()):
        result.extend(unidecode(word).split())
    return unidecode(delim.join(result))
