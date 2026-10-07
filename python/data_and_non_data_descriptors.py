class NonDataDescriptor:
    def __get__(self, obj, owner):
        return f'__get__ from {obj!r}'


class DataDescriptor:
    def __get__(self, obj, owner):
        return f'__get__ from {obj!r}'

    def __set__(self, value):
        print('got __set__ for value')


class AlsoDataDescriptor:
    def __get__(self, obj, owner):
        return f'__get__ from {obj!r}'

    def __delete__(self, obj):
        print(f'got __delete__ from {obj}')


class Foo:
    x = NonDataDescriptor()


class Bar:
    x = DataDescriptor()


class Baz:
    x = AlsoDataDescriptor()


x = Foo()
print(f'x.x before {x.x}')
x.__dict__['x'] = 'lololol'
print(f'x.x after {x.x}')

y = Bar()
print(f'y.x before {y.x}')
y.__dict__['x'] = 'lololol'
print(f'y.x after {y.x}')

z = Baz()
print(f'z.x before {z.x}')
z.__dict__['x'] = 'lololol'
print(f'z.x after {z.x}')
