from dataclasses import dataclass


import functools

# https://stackoverflow.com/questions/5929107/decorators-with-parameters


def event_handler(method=None, name=None):
    print("event_handler", method, name)
    assert callable(method) or method is None

    def _decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if "__event_handlers" not in self.__dict__:
                self.__dict__["__event_handlers"] = {}
            self.__dict__["__event_handlers"][name or func.__name__] = func
            print("event_handler wrapper", func.__name__, name)
            assert method is not None
            return method(self, *args, **kwargs)

        return wrapper

    return _decorator(method) if callable(method) else _decorator


def event_handler2(method):
    def wrapper(self, *args, **kwargs):
        print("event_handler", method.__name__)
        self.__dict__["__event_handlers"] = method.__name__
        return method(self, *args, **kwargs)

    return wrapper


@dataclass
class User:
    name: str
    age: int

    @event_handler
    def add(self, v: int) -> int:
        self.age += v
        return self.age

    @event_handler(name="decrement")
    def minus(self, v: int) -> int:
        self.age -= v
        return self.age


class A:
    def __init__(self):
        self.a = 1

    def add(self, v: int) -> int:
        self.a += v
        return self.a


if __name__ == "__main__":
    u = User("a", 1)
    print(u.add(1))
    print(u.__dict__)
