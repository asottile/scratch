from __future__ import annotations

import string
from typing import Any


def print_sheet(sheet: list[list[Any]]) -> None:
    widths = [1] * len(sheet[0])
    for row in sheet:
        for i, d in enumerate(row):
            widths[i] = max(widths[i], len(repr(d)))

    print('=' * (sum(widths) + len(widths) * 2 + 1))
    print('|', end='')
    for i, width in zip(range(len(sheet[0])), widths):
        print('{: >{}} |'.format(string.ascii_uppercase[i], width), end='')
    print()
    print('-' * (sum(widths) + len(widths) * 2 + 1))
    for row in sheet:
        print('|', end='')
        for d, width in zip(row, widths):
            print('{!r: >{}} |'.format(d, width), end='')
        print()
    print('=' * (sum(widths) + len(widths) * 2 + 1))


def main() -> int:
    sheet = [
        [1, 2, 'C', 4, 5],
        [1, 4, 'B', 6, 7],
        [1, 2, 'A', 9001, 9],
        [2, 2, 'A', 5, 6],
        [1, 2, 'A', 5, 6],
    ]
    print_sheet(sheet)
    return 0


if __name__ == '__main__':
    exit(main())
