class cached_class_property:
    def __init__(self, fget):
        self.fget = classmethod(fget)

    def __get__(self, obj, owner):
        val = self.fget.__get__(None, owner)()
        setattr(owner, self.fget.__name__, val)
        return val


class Test:
    @cached_class_property
    def class_property(cls):
        print('Called class_property')
        return object()


assert Test.class_property is Test.class_property


class cached_static_property:
    def __init__(self, fget):
        self.fget = staticmethod(fget)

    def __get__(self, obj, owner):
        val = self.fget.__get__(None, owner)()
        setattr(owner, self.fget.__name__, val)
        return val


class Test2:
    @cached_static_property
    def static_property():  # type: ignore
        print('Called static_property')
        return object()


assert Test2.static_property is Test2.static_property
