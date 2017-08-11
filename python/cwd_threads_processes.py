import concurrent.futures
import itertools
import os
import tempfile
import time


def f(x, tmpdir):
    dirname = os.path.join(tmpdir, str(x))
    os.makedirs(dirname, exist_ok=True)
    os.chdir(dirname)
    time.sleep(x / 10)
    print(f'{x} {os.getcwd()}')


def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        print('Threads share cwd')
        with concurrent.futures.ThreadPoolExecutor(4) as ex:
            tuple(ex.map(f, range(10), itertools.repeat(tmpdir)))

        print('Processes do not')
        with concurrent.futures.ProcessPoolExecutor(4) as ex:
            tuple(ex.map(f, range(10), itertools.repeat(tmpdir)))


if __name__ == '__main__':
    exit(main())
