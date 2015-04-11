
class NonDataDescriptor(object):
    def __get__(self, obj, owner):
        return '__get__ from {0!r}'.format(obj)


class DataDescriptor(object):
    def __get__(self, obj, owner):
        return '__get__ from {0!r}'.format(obj)

    def __set__(self, value):
        print('got __set__ for value')


class Foo(object):
    x = NonDataDescriptor()


class Bar(object):
    x = DataDescriptor()


x = Foo()
print('x.x before {0}'.format(x.x))
x.__dict__['x'] = 'lololol'
print('x.x after {0}'.format(x.x))
y = Bar()
print('y.x before {0}'.format(y.x))
y.__dict__['x'] = 'lololol'
print('y.x after {0}'.format(y.x))
