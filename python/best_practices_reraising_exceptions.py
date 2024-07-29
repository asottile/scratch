from __future__ import annotations

import contextlib
import sys
import traceback
from typing import Generator
from typing import NoReturn


class MyCustomError(RuntimeError):
    pass


def g() -> NoReturn:
    raise AssertionError('hi')


def f() -> NoReturn:
    g()


@contextlib.contextmanager
def simulate_running() -> Generator[None]:
    try:
        yield
    except Exception:
        traceback.print_exc()


def test1():
    try:
        f()
    except AssertionError as e:
        raise MyCustomError(e)


def test2():
    try:
        f()
    except AssertionError as e:
        exc_info = sys.exc_info()
        raise MyCustomError(e).with_traceback(exc_info[2])


def main():
    print('*' * 79)
    with simulate_running():
        test1()
    print('*' * 79)
    print('Notice how the stacktrace does not contain f() or g() at all')
    print('You can fix that however')
    print('*' * 79)
    with simulate_running():
        test2()
    print('*' * 79)


if __name__ == '__main__':
    raise SystemExit(main())


OUTPUT = """\
*******************************************************************************
Traceback (most recent call last):
  File "python/best_practices_reraising_exceptions.py", line 31, in test1
    f()
  File "python/best_practices_reraising_exceptions.py", line 18, in f
    g()
  File "python/best_practices_reraising_exceptions.py", line 14, in g
    raise AssertionError('hi')
AssertionError: hi

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "python/best_practices_reraising_exceptions.py", line 24, in simulate_running
    yield
  File "python/best_practices_reraising_exceptions.py", line 47, in main
    test1()
  File "python/best_practices_reraising_exceptions.py", line 33, in test1
    raise MyCustomError(e)
MyCustomError: hi
*******************************************************************************
Notice how the stacktrace does not contain f() or g() at all
You can fix that however
*******************************************************************************
Traceback (most recent call last):
  File "python/best_practices_reraising_exceptions.py", line 38, in test2
    f()
  File "python/best_practices_reraising_exceptions.py", line 18, in f
    g()
  File "python/best_practices_reraising_exceptions.py", line 14, in g
    raise AssertionError('hi')
AssertionError: hi

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "python/best_practices_reraising_exceptions.py", line 24, in simulate_running
    yield
  File "python/best_practices_reraising_exceptions.py", line 53, in main
    test2()
  File "python/best_practices_reraising_exceptions.py", line 41, in test2
    raise MyCustomError(e).with_traceback(exc_info[2])
  File "python/best_practices_reraising_exceptions.py", line 38, in test2
    f()
  File "python/best_practices_reraising_exceptions.py", line 18, in f
    g()
  File "python/best_practices_reraising_exceptions.py", line 14, in g
    raise AssertionError('hi')
MyCustomError: hi
******************************************************************************
"""  # noqa: E501
