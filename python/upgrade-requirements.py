#!/usr/bin/env python
import argparse
import contextlib
import io
import os
import shutil
import subprocess
import sys
import tempfile


@contextlib.contextmanager
def tempdir():
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


EXCLUDE = ('pip', 'wsgiref')


@contextlib.contextmanager
def upgraded_pip(pip):
    # Latest pip understands py35 wheels
    subprocess.check_call((pip, 'install', 'pip', '--upgrade'))
    try:
        yield
    finally:
        # pip 1.5.6 shows all packages with `pip list`
        subprocess.check_call((pip, 'install', 'pip==1.5.6'))


def parse_pip_list(pip):
    out = subprocess.check_output((pip, 'list')).decode('UTF-8')
    return {
        line.replace(' (', '==').replace(')', '') for line in out.splitlines()
        if not any(
            line.startswith(excluded + ' (') for excluded in EXCLUDE
        )
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--python',
        default='python' + '.'.join(str(x) for x in sys.version_info[:2]),
    )
    parser.add_argument(
        '-i', '--index-url', default='https://pypi.python.org/simple',
    )
    args = parser.parse_args()

    assert os.path.exists('setup.py')
    assert os.path.exists('requirements-dev-minimal.txt')

    with tempdir() as tmpdir:
        venv = os.path.join(tmpdir, 'venv')
        pip = os.path.join(venv, 'bin', 'pip')
        python = os.path.join(venv, 'bin', 'python')

        subprocess.check_call(('virtualenv', venv, '-p', args.python))

        # Use latest setuptools
        subprocess.check_call((
            pip, 'install', 'setuptools', '--upgrade', '-i', args.index_url,
        ))

        pkg_name = subprocess.check_output((
            python, 'setup.py', '--name',
        )).decode('UTF-8').strip()

        with upgraded_pip(pip):
            subprocess.check_call((
                pip, 'install', '-e', '.', '-i', args.index_url,
            ))

        # Uninstall us so we don't end up in the list
        subprocess.check_call((pip, 'uninstall', '-y', pkg_name))

        requirements = parse_pip_list(pip)

        with upgraded_pip(pip):
            subprocess.check_call((
                pip, 'install', '-r', 'requirements-dev-minimal.txt',
                '-i', args.index_url,
            ))

        requirements_dev = parse_pip_list(pip) - requirements

        with io.open('requirements.txt', 'w') as f:
            f.write('\n'.join(requirements) + '\n')
        with io.open('requirements-dev.txt', 'w') as f:
            f.write('\n'.join(requirements_dev) + '\n')

        subprocess.check_call((pip, 'install', 'pre-commit-hooks'))
        subprocess.call((
            os.path.join(venv, 'bin', 'requirements-txt-fixer'),
            'requirements.txt', 'requirements-dev.txt',
        ))

if __name__ == '__main__':
    exit(main())
