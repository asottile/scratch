import os
import random


def garbage_unicode():
    return os.urandom(10).encode('hex').decode('UTF-8')


def garbage_bytes():
    return os.urandom(10)


def garbage_int():
    return random.randrange(0, 1000)


def garbage_float():
    return random.randrange(0, 1000) + random.random()


def make_anon(obj):
    if type(obj) is int:
        return garbage_int()
    elif type(obj) is float:
        return garbage_float()
    elif type(obj) is unicode:
        return garbage_unicode()
    elif type(obj) is bytes:
        return garbage_bytes()
    elif type(obj) is tuple:
        return tuple(make_anon(o) for o in obj)
    elif type(obj) is list:
        return list(make_anon(o) for o in obj)
    elif type(obj) is dict:
        return dict((make_anon(k), make_anon(v)) for k, v in obj.items())
    elif obj is None:
        return None
    else:
        assert False, type(obj)


if __name__ == '__main__':
    from city_hoods import x
    print(repr(make_anon(x)))
