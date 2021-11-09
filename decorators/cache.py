from typing import Optional, Callable
from collections import OrderedDict


def lru_cache(maxsize: Optional[int] = None):
    def decorator(fn: Callable):
        cache = OrderedDict()

        def wrapper(*args):
            if args not in cache:
                if len(cache) == maxsize:
                    cache.popitem(last=False)

                result = fn(*args)
                cache[args] = result

            return cache[args]

        wrapper.cache = cache

        return wrapper
    return decorator


@lru_cache(maxsize=2)
def _test_function(n: int):
    return n


if __name__ == '__main__':
    print(_test_function(1))
    print(_test_function.cache)

    print(_test_function(2))
    print(_test_function.cache)

    print(_test_function(3))
    print(_test_function.cache)
