"""Greedily find an environment subset which allows a command to pass."""
from __future__ import absolute_import

import os
import subprocess


def try_run(env):
    try:
        subprocess.check_output(
            [r'C:\Python27\python.exe', '-c', 'import random'],
            env=env,
            stderr=subprocess.STDOUT,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def test_with_subset_of_env(env):
    for key in env:
        print('Trying key {0}'.format(key))
        new_env = env.copy()
        del new_env[key]

        if try_run(new_env):
            return test_with_subset_of_env(new_env)
        else:
            print('Needs key {0}'.format(key))
    else:
        return env


if __name__ == '__main__':
    minimal_env = test_with_subset_of_env(os.environ)
    print(sorted(minimal_env))
