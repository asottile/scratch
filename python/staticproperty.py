class staticproperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, owner):
        return staticmethod(self.fget).__get__(None, owner)()


class Foo:
    @staticproperty
    def bar():  # type: ignore
        print('hai')
        return 9001


print(Foo.bar)

output = '''
hai
9001
'''
