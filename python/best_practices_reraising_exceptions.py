import functools
import sys
import traceback

import six


class MyCustomError(RuntimeError):
    pass


def g():
    raise AssertionError('hi')


def f():
    g()


def simulate_running(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            traceback.print_exc()
    return wrapper


@simulate_running
def test1():
    try:
        f()
    except AssertionError as e:
        raise MyCustomError(e)


@simulate_running
def test2():
    try:
        f()
    except AssertionError as e:
        exc_info = sys.exc_info()
        six.reraise(MyCustomError, MyCustomError(e), exc_info[2])


def main():
    print('*' * 79)
    test1()
    print('*' * 79)
    print('Notice how the stacktrace does not contain f() or g() at all')
    print('You can fix that however')
    print('*' * 79)
    test2()
    print('*' * 79)


if __name__ == '__main__':
    exit(main())


OUTPUT = """\
$ python test.py
*******************************************************************************
Traceback (most recent call last):
  File "test.py", line 24, in wrapper
    return func(*args, **kwargs)
  File "test.py", line 35, in test1
    raise MyCustomError(e)
MyCustomError: hi
*******************************************************************************
Notice how the stacktrace does not contain f() or g() at all
You can fix that however
*******************************************************************************
Traceback (most recent call last):
  File "test.py", line 24, in wrapper
    return func(*args, **kwargs)
  File "test.py", line 44, in test2
    six.reraise(MyCustomError, MyCustomError(e), exc_info[2])
  File "test.py", line 41, in test2
    f()
  File "test.py", line 17, in f
    g()
  File "test.py", line 13, in g
    raise AssertionError('hi')
MyCustomError: hi
*******************************************************************************
"""
