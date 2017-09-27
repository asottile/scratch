#!/usr/bin/env python3.6
import argparse
import getpass
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--remote')
    parser.add_argument('--upstream')
    args = parser.parse_args()

    remotes = subprocess.check_output(
        ('git', 'remote')
    ).decode('UTF-8').splitlines()
    if args.upstream:
        upstream = args.upstream
    elif 'upstream' in remotes:
        upstream = 'upstream'
    elif 'origin' in remotes:
        upstream = 'origin'
    else:
        raise AssertionError(f'Which upstream? {remotes}')

    if args.dry_run:
        dry_run = 'echo '
    else:
        dry_run = ''

    if args.remote:
        remote = args.remote
    elif getpass.getuser() in remotes:
        remote = getpass.getuser()
    elif 'origin' in remotes:
        remote = 'origin'
    else:
        raise AssertionError(f'Which remote? {remotes}')

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
