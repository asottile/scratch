class cached_class_property(object):
    def __init__(self, fget):
        self.fget = classmethod(fget)

    def __get__(self, obj, owner):
        val = self.fget.__get__(None, owner)()
        setattr(owner, self.fget.__name__, val)
        return val


class Test(object):
    @cached_class_property
    def class_property(cls):
        print('Called class_property')
        return object()


assert Test.class_property is Test.class_property


class cached_static_property(object):
    def __init__(self, fget):
        self.fget = staticmethod(fget)

    def __get__(self, obj, owner):
        val = self.fget.__get__(None, owner)()
        setattr(owner, self.fget.__name__, val)
        return val


class Test2(object):
    @cached_static_property
    def static_property():
        print('Called static_property')
        return object()


assert Test2.static_property is Test2.static_property
