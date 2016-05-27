#!/usr/bin/env python3.5
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
    elif 'canon' in remotes:
        upstream = 'canon'
    elif 'upstream' in remotes:
        upstream = 'upstream'
    elif 'origin' in remotes:
        upstream = 'origin'
    else:
        raise AssertionError('Which upstream? {}'.format(remotes))

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
        raise AssertionError('Which remote? {}'.format(remotes))

    subprocess.check_call((
        'bash', '-c',
        'git fetch --all --prune && '
        'git branch --remote --merged {upstream}/master | '
        'grep {remote}/ | '
        "cut -d'/' -f2-999 | "
        "grep -Ev '^(PLACEHOLDER|master|stage|production)' | "
        "grep -v '>' | "
        "xargs --replace -P 8 {dry_run}git push {remote} :{{}}".format(
            upstream=upstream, dry_run=dry_run, remote=remote,
        )
    ))
    subprocess.check_call((
        'bash', '-c',
        'git branch --merged {upstream}/master | '
        'grep -v master | '
        'xargs --no-run-if-empty {dry_run}git branch --delete'.format(
            upstream=upstream, dry_run=dry_run,
        ),
    ))

if __name__ == '__main__':
    exit(main())
