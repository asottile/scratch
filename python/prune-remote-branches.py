#!/usr/bin/env python3.6
import argparse
import json
import os.path
import subprocess

HERE = os.path.dirname(os.path.realpath(__file__))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--remote', default='')
    parser.add_argument('--upstream', default='')
    args = parser.parse_args()

    cmd = (
        os.path.join(HERE, '_git-remote-upstream'),
        '--remote', args.remote, '--upstream', args.upstream,
    )
    remote, upstream = json.loads(subprocess.check_output(cmd))

    if args.dry_run:
        dry_run = 'echo '
    else:
        dry_run = ''

    subprocess.check_call((
        'bash', '-c',
        f'git fetch --all --prune && '
        f'git branch --remote --merged {upstream}/master | '
        f'grep {remote}/ | '
        f"cut -d'/' -f2-999 | "
        f"grep -Ev '^(PLACEHOLDER|master|stage|production)' | "
        f"grep -v '>' | "
        f"xargs --replace -P 8 {dry_run}git push {remote} :{{}}",
    ))
    subprocess.check_call((
        'bash', '-c',
        f'git branch --merged {upstream}/master | '
        f"grep -Ev '(\*|master)' | "
        f'xargs --no-run-if-empty {dry_run}git branch --delete',
    ))


if __name__ == '__main__':
    exit(main())
