import collections


def tabulate(items):
    if not items:
        return ''
    field_count = len(items[0])
    columns = items[0]._fields
    widths = [
        max(
            len(str(x))
            for x in [item[idx] for item in items] + [columns[idx]]
        )
        for idx in range(field_count)
    ]

    total_width = sum(widths) + field_count + 1
    line = '-' * total_width + '\n'
    fmt = '|' + '|'.join('{{: >{}}}'.format(width) for width in widths) + '|\n'
    lines = [fmt.format(*[str(x) for x in item]) for item in items] + ['']
    header_line = '=' * total_width + '\n'
    header = header_line + fmt.format(*columns) + header_line
    return header + line.join(lines)


if __name__ == '__main__':
    C = collections.namedtuple('C', ('foo', 'bar', 'baz'))
    print(tabulate((
        C('herp', 'derp', 'derp'),
        C('herploooooooooooooooong', 'derp', 'derp'),
        C('herp', 'derp', 'derp'),
        C('herp', 'derp', 'derp'),
    )))
