from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

T = TypeVar("T")
K = TypeVar("K")
P = ParamSpec("P")


def cached(hash_fnc: Callable[P, K]):
    def outer(fnc: Callable[P, T]) -> Callable[P, T]:
        store: dict[K, T] = {}

        @wraps(fnc)
        def inner(*args: P.args, **kwargs: P.kwargs) -> T:
            k = hash_fnc(*args, **kwargs)
            if k not in store:
                store[k] = fnc(*args, **kwargs)
            return store[k]

        return inner

    return outer
