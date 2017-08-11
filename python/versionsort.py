#!/usr/bin/env python3.5
import argparse
import sys


def to_key(version_string):
    return tuple(map(int, version_string.split('.')))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--reversed', action='store_true', default=False)
    args = parser.parse_args()

    modifier = reversed if args.reversed else list

    lines = [x.strip() for x in sys.stdin]
    for v in modifier(sorted(lines, key=to_key)):
        print(v)


if __name__ == '__main__':
    exit(main())
