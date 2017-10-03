#!/usr/bin/env python3
import argparse
import contextlib
import os.path
import subprocess
import tarfile
import tempfile


@contextlib.contextmanager
def create_container(img):
    container = subprocess.check_output(('docker', 'create', img))
    container = container.strip().decode()
    try:
        yield container
    finally:
        subprocess.check_call(('docker', 'rm', container))


def _docker_export(container_id, tar):
    subprocess.check_call(('docker', 'export', '-o', tar, container_id))


def _docker_cp(src, dest):
    subprocess.check_call(('docker', 'cp', src, dest))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default='ubuntu:xenial')
    parser.add_argument('container')
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        with create_container(args.src) as container_id:
            tar_filename = os.path.join(tmpdir, 'tar.gz')
            _docker_export(container_id, tar_filename)

        with tarfile.open(tar_filename) as tar:
            tar.extractall(tmpdir)
        os.remove(tar_filename)

        # these don't copy cleanly for some reason
        os.remove(os.path.join(tmpdir, 'etc/hostname'))
        os.remove(os.path.join(tmpdir, 'etc/hosts'))
        os.remove(os.path.join(tmpdir, 'etc/resolv.conf'))

        for filename in os.listdir(tmpdir):
            _docker_cp(os.path.join(tmpdir, filename), args.container + ':/')


if __name__ == '__main__':
    exit(main())
