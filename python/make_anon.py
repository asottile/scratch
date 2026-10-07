import codecs
import os
import random
from typing import Any


def garbage_unicode() -> str:
    return codecs.encode(os.urandom(10), 'hex').decode()


def garbage_bytes() -> bytes:
    return os.urandom(10)


def garbage_int() -> int:
    return random.randrange(0, 1000)


def garbage_float() -> float:
    return random.randrange(0, 1000) + random.random()


def make_anon(obj: Any) -> Any:
    if type(obj) is int:
        return garbage_int()
    elif type(obj) is float:
        return garbage_float()
    elif type(obj) is str:
        return garbage_unicode()
    elif type(obj) is bytes:
        return garbage_bytes()
    elif type(obj) is tuple:
        return tuple(make_anon(o) for o in obj)
    elif type(obj) is list:
        return list(make_anon(o) for o in obj)
    elif type(obj) is dict:
        return {make_anon(k): make_anon(v) for k, v in obj.items()}
    elif obj is None:
        return None
    else:
        assert False, type(obj)


if __name__ == '__main__':
    from city_hoods import x
    print(repr(make_anon(x)))
