#!/usr/bin/env python
import argparse
import contextlib
import os.path
import shutil
import subprocess
import sys
import tempfile


def out(*cmd, **kwargs):
    return subprocess.check_output(cmd, **kwargs).decode('UTF-8')


@contextlib.contextmanager
def tmpdir():
    tempdir = tempfile.mkdtemp()
    try:
        yield tempdir
    finally:
        shutil.rmtree(tempdir)


def get_shared_objects(pkg):
    try:
        return out('dpkg', '-L', pkg).splitlines()
    except subprocess.CalledProcessError:
        return


def get_uninteresting_links():
    # This is auto-linked always
    uninteresting = {'linux-vdso.so.1'}
    for pkg in ('libc6', 'libstdc++6'):
        uninteresting.update(get_shared_objects(pkg))
    return uninteresting


def parse_ldd_output(output):
    for line in output.splitlines():
        line = line.strip()
        before, _, after = line.partition('=>')
        before, after = before.strip(), after.strip()
        before, _, _ = before.partition('(')
        before = before.strip()
        after, _, _ = after.partition('(')
        after = after.strip()
        yield after or before


def get_shared_object_filenames(dirname):
    for dirpath, _, filenames in os.walk(dirname):
        for filename in filenames:
            if filename.endswith('.so'):
                yield os.path.join(dirpath, filename)


def from_where(filename):
    try:
        output = out('dpkg', '-S', os.path.realpath(filename)).strip()
        return output.split(':')[0]
    except subprocess.CalledProcessError:
        return '<<unknown>>'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--python', default=sys.executable)
    parser.add_argument(
        '-i', '--index-url', default='https://pypi.python.org/simple',
    )
    parser.add_argument('package')
    args = parser.parse_args()

    uninteresting_links = get_uninteresting_links()

    with tmpdir() as tempdir:
        venv = os.path.join(tempdir, 'venv')
        pip = os.path.join(venv, 'bin', 'pip')
        download = os.path.join(tempdir, 'download')
        os.makedirs(download)
        out('virtualenv', venv, '-p', args.python)
        out(pip, 'install', 'pip', '--upgrade')
        out(
            pip, 'download',
            '--no-deps',
            '--dest', download,
            '--only-binary', 'all',
            '--index-url', args.index_url,
            args.package,
        )
        out('unzip', os.listdir(download)[0], cwd=download)

        for filename in get_shared_object_filenames(download):
            print(os.path.relpath(filename, download))
            ldd_output = out('ldd', filename)
            linked = set(parse_ldd_output(ldd_output)) - uninteresting_links
            if not linked:
                print('(nothing interesting)')
            else:
                for pkg in sorted(linked):
                    print('- {} ({})'.format(pkg, from_where(pkg)))


if __name__ == '__main__':
    exit(main())
