from typing import Any, TypeVar

from .types import TypeGuardFactory

T = TypeVar("T")


class Registry(dict):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def __getitem__(self, __key: type[T]) -> TypeGuardFactory[Any, T]:
        return super().__getitem__(__key)

    def __setitem__(self, __key: type[T], __value: TypeGuardFactory[Any, T]) -> None:
        return super().__setitem__(__key, __value)
