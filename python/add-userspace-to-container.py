import argparse
import contextlib
import os.path
import subprocess
import tempfile
from typing import Generator


@contextlib.contextmanager
def create_container(img: str) -> Generator[str, None, None]:
    cmd = ('docker', 'create', img)
    container = subprocess.check_output(cmd).strip().decode()
    try:
        yield container
    finally:
        subprocess.check_call(('docker', 'rm', container))


def _docker_export(container_id: str, tar: str) -> None:
    subprocess.check_call(('docker', 'export', '-o', tar, container_id))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default='ubuntu:xenial')
    parser.add_argument('container')
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        with create_container(args.src) as container_id:
            tar_filename = os.path.join(tmpdir, 'tar.gz')
            _docker_export(container_id, tar_filename)

        with open(tar_filename, 'rb') as f:
            cmd = ('docker', 'cp', '--extract', '-', f'{args.container}:/')
            return subprocess.call(cmd, stdin=f)


if __name__ == '__main__':
    exit(main())
