#!/usr/bin/env python
import argparse
import contextlib
import os
import pipes
import shutil
import subprocess
import sys
import tempfile

from pkg_resources import Requirement
from pkg_resources import working_set


installed_things = {pkg.key: pkg for pkg in working_set}


class NeedsMoreInstalledError(RuntimeError):
    pass


def color(s, color):
    if sys.stdout.isatty():
        return '{}{}{}'.format(color, s, '\033[m')
    else:
        return s


def fmt_cmd(cmd):
    ret = '>>> {}'.format(' '.join(pipes.quote(x) for x in cmd))
    return color(ret, '\033[32m')


def print_call(*cmd, **kwargs):
    print(fmt_cmd(cmd))
    subprocess.check_call(cmd, **kwargs)


def reexec(*cmd, **kwargs):
    reason = kwargs.pop('reason')
    assert not kwargs, kwargs
    print(color('*** exec-ing: {}'.format(reason), '\033[33m'))
    print(fmt_cmd(cmd))
    # Never returns
    os.execv(cmd[0], cmd)


def requirements(requirements_filename):
    with open(requirements_filename) as requirements_file:
        for line in requirements_file:
            if line.strip() and not line.startswith(('#', '-e')):
                yield Requirement.parse(line.strip())


def installed(requirements_file):
    expected_pinned = set()
    requirements_to_parse = list(requirements(requirements_file))
    already_parsed = {(req.key, req.extras) for req in requirements_to_parse}
    unmet = set()

    while requirements_to_parse:
        req = requirements_to_parse.pop()
        installed_req = installed_things[req.key]
        expected_pinned.add('{}=={}'.format(
            installed_req.project_name, installed_req.version,
        ))
        for sub in installed_req.requires(req.extras):
            if sub.key not in installed_things:
                unmet.add('{}{}'.format(sub.key, ','.join(sub.specifier)))
            elif (sub.key, sub.extras) not in already_parsed:
                requirements_to_parse.append(sub)
                already_parsed.add((sub.key, sub.extras))

    if unmet:
        raise NeedsMoreInstalledError(unmet)
    else:
        return expected_pinned


def dirs(tmp):
    dirnames = ('venv', 'venv/bin/python', 'venv/bin/pip')
    return tuple(os.path.join(tmp, d) for d in dirnames)


@contextlib.contextmanager
def cleanup_dir(dirname):
    try:
        yield dirname
    finally:
        shutil.rmtree(dirname)


def make_virtualenv(args):
    with cleanup_dir(tempfile.mkdtemp()) as tempdir:
        venv, python, pip = dirs(tempdir)
        print_call('virtualenv', venv, '-p', args.python, '--never-download')

        def pip_install(*argv):
            print_call(pip, 'install', '-i', args.index_url, *argv)

        # Latest pip installs python3.5 wheels
        pip_install('pip', 'setuptools', '--upgrade')
        pip_install('-r', 'requirements-minimal.txt')
        pip_install('-r', 'requirements-dev-minimal.txt')

        reexec(
            python, __file__.rstrip('c'),
            '--tempdir', tempdir,
            # Pass along existing args
            '--index-url', args.index_url,
            '--exec-count', str(args.exec_count),
            '--exec-limit', str(args.exec_limit),
            reason='to use the virtualenv python',
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--python',
        default='python' + '.'.join(str(x) for x in sys.version_info[:2]),
    )
    parser.add_argument(
        '-i', '--index-url', default='https://pypi.python.org/simple',
    )
    parser.add_argument(
        '--exec-limit', type=int, default=10, help=argparse.SUPPRESS,
    )
    parser.add_argument(
        '--exec-count', type=int, default=0, help=argparse.SUPPRESS,
    )
    parser.add_argument('--tempdir', help=argparse.SUPPRESS)
    args = parser.parse_args()

    assert os.path.exists('requirements-minimal.txt')
    assert os.path.exists('requirements-dev-minimal.txt')

    if args.tempdir is None:
        make_virtualenv(args)  # Never returns

    venv, python, pip = dirs(args.tempdir)

    with cleanup_dir(args.tempdir):
        try:
            reqs = installed('requirements-minimal.txt')
            reqs_dev = installed('requirements-dev-minimal.txt')
        except NeedsMoreInstalledError as e:
            print(color('Installing unmet requirements!', '\033[31m'))
            print('Probably due to https://github.com/pypa/pip/issues/3903')
            new_exec_count = args.exec_count + 1
            if new_exec_count > args.exec_limit:
                raise AssertionError('--exec-limit depth limit exceeded')
            unmet, = e.args
            print_call(pip, 'install', '-i', args.index_url, *unmet)
            reexec(
                python, __file__.rstrip('c'),
                '--exec-count', str(new_exec_count),
                # Pass along existing args
                '--index-url', args.index_url,
                '--tempdir', args.tempdir,
                '--exec-limit', str(args.exec_limit),
                reason='Unmet dependencies',
            )

        with open('requirements.txt', 'w') as f:
            f.write('\n'.join(reqs) + '\n')
        with open('requirements-dev.txt', 'w') as f:
            f.write('\n'.join(reqs_dev - reqs) + '\n')

        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(
                (pip, 'install', 'pre-commit-hooks'),
                stdout=devnull, stderr=devnull,
            )
        subprocess.call((
            os.path.join(venv, 'bin', 'requirements-txt-fixer'),
            'requirements.txt', 'requirements-dev.txt',
        ))

if __name__ == '__main__':
    exit(main())
