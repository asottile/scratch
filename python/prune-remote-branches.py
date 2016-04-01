#!/usr/bin/env python3.4
import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--remote', default='origin')
    args = parser.parse_args()

    remotes = subprocess.check_output(
        ('git', 'remote')
    ).decode('UTF-8').splitlines()
    if 'canon' in remotes:
        upstream = 'canon'
    elif 'upstream' in remotes:
        upstream = 'upstream'
    elif 'origin' in remotes:
        upstream = 'origin'
    else:
        raise AssertionError('Which remote? {}'.format(remotes))

    if args.dry_run:
        dry_run = 'echo '
    else:
        dry_run = ''

    subprocess.check_call((
        'bash', '-c',
        'git fetch --all --prune && '
        'git branch --remote --merged {upstream}/master | '
        'grep {remote}/ | '
        "cut -d'/' -f2-999 | "
        "grep -Ev '^(PLACEHOLDER|master|stage|production)' | "
        "grep -v '>' | "
        "xargs --replace -P 8 {dryrun}git push {remote} :{{}}".format(
            upstream=upstream, dryrun=dry_run, remote=args.remote,
        )
    ))

if __name__ == '__main__':
    exit(main())
