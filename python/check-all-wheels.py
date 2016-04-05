#!/usr/bin/env python
import argparse
import contextlib
import os
import shutil
import subprocess
import sys


def silent(*cmd):
    with open(os.devnull, 'w') as devnull:
        subprocess.check_call(cmd, stdout=devnull)


@contextlib.contextmanager
def upgraded_pip(pip):
    # Latest pip understands py35 wheels
    silent(pip, 'install', 'pip', '--upgrade')
    try:
        yield
    finally:
        # pip 1.5.6 shows all packages with `pip list`
        silent(pip, 'install', 'pip==1.5.6')


DISTS_DIR = 'downloaded_dists'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--index-url', default='https://pypi.python.org/simple',
    )
    args = parser.parse_args()

    assert os.path.exists('requirements.txt')
    assert os.path.exists('requirements-dev.txt')

    if os.path.exists(DISTS_DIR):
        shutil.rmtree(DISTS_DIR)
    os.makedirs(DISTS_DIR)

    with upgraded_pip('pip'):
        silent(
            'pip', 'install', '--download', DISTS_DIR,
            '-r', 'requirements.txt', '-r', 'requirements-dev.txt',
            '-i', args.index_url,
        )
    ret = 0
    for filename in os.listdir(DISTS_DIR):
        if not filename.endswith('.whl'):
            ret = 1
            print(os.path.join(DISTS_DIR, filename))
    return ret


if __name__ == '__main__':
    exit(main())
