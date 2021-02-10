from __future__ import annotations

import concurrent.futures
import itertools
import os
import tempfile
import time


def f(x: int, tmpdir: str) -> None:
    dirname = os.path.join(tmpdir, str(x))
    os.makedirs(dirname, exist_ok=True)
    os.chdir(dirname)
    time.sleep(x / 10)
    print(f'{x} {os.getcwd()}')


def main() -> int:
    with tempfile.TemporaryDirectory() as tmpdir:
        print('Threads share cwd')
        with concurrent.futures.ThreadPoolExecutor(4) as t_ex:
            tuple(t_ex.map(f, range(10), itertools.repeat(tmpdir)))

        print('Processes do not')
        with concurrent.futures.ProcessPoolExecutor(4) as p_ex:
            tuple(p_ex.map(f, range(10), itertools.repeat(tmpdir)))
    return 0


if __name__ == '__main__':
    exit(main())
