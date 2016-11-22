#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import io

import pkg_resources


reqs = {pkg.key: pkg for pkg in pkg_resources.working_set}


def get_lines_from_file(filename):
    """Returns the non-blank, non-comment lines from a requirements file."""
    with io.open(filename, encoding='UTF-8') as requirements_file:
        return [
            line.strip() for line in requirements_file
            if line.strip() and not line.startswith('#')
        ]


def get_raw_requirements(requirements_file):
    """Get requirements from a requirements.txt file.  -r is not supported"""
    unparsed_requirements_lines = get_lines_from_file(requirements_file)

    return pkg_resources.parse_requirements(
        '\n'.join(unparsed_requirements_lines)
    )


def print_req(req, depth, specs=''):
    print('{} {}{}{}'.format(
        '  ' * depth + bool(depth) * ' -',
        req.key,
        '[{}]'.format(','.join(req.extras)) if req.extras else '',
        ','.join(''.join(spec) for spec in req.specs))
    )
    installed_req = reqs[req.key]
    for sub_requirement in installed_req.requires(req.extras):
        print_req(sub_requirement, depth + 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('requirements_file')
    args = parser.parse_args()

    raw_requirements = get_raw_requirements(args.requirements_file)
    for requirement in raw_requirements:
        print_req(requirement, 0)


if __name__ == '__main__':
    exit(main())
