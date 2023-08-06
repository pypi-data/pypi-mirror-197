from collections.abc import Iterable, Mapping, MutableMapping, MutableSequence, MutableSet, Sequence, Set
from functools import wraps
from types import UnionType
from typing import Any, Literal, TypeGuard, TypeVar, get_args, get_origin, is_typeddict

from toolz import curry

from .cached import cached
from .registry import Registry
from .types import TypeGuardFactory, TypeGuardFnc

P = TypeVar("P")
T = TypeVar("T")
user_types = Registry()
user_generic = Registry()


def cast_to_type(data: Any, t: type[T], strict: bool = False) -> T:
    if is_type(data, t, strict):
        return data
    else:
        raise TypeError(f"{data} is not of type {t}")


def is_type(data: Any, t: type[T], strict: bool = False) -> TypeGuard[T]:
    return _guard(t, False, strict)(data)


def is_mutable_collection(t: type[T]) -> bool:
    if issubclass(t, Mapping):
        return issubclass(t, MutableMapping)
    elif issubclass(t, Sequence):
        return issubclass(t, MutableSequence)
    elif issubclass(t, Set):
        return issubclass(t, MutableSet)
    else:
        return False


def get_super_type(t: type) -> type | None:
    return getattr(t, "__supertype__", None)


def _arg_hash(t: type[T], invariant: bool, strict: bool) -> int:
    return hash((t, invariant, strict))


@cached(_arg_hash)
def _guard(t: type[T], invariant: bool, strict: bool) -> TypeGuardFnc[Any, T]:
    origin = get_origin(t)
    supertype = get_super_type(t)

    if t in user_types.keys():
        return user_types[t](t, invariant, strict)

    elif origin and origin in user_generic.keys():
        return user_generic[origin](t, invariant, strict)

    elif is_typeddict(t):
        gg = _guard(dict, invariant, strict)
        invariant = is_mutable_collection(dict)
        kg = _guard(str, False, strict)
        vgs = {k: _guard(v, False, strict) for k, v in t.__annotations__.items()}
        required = t.__required_keys__  # type: ignore[attr-defined]
        optional = t.__optional_keys__  # type: ignore[attr-defined]

        def inner(data: Any) -> TypeGuard[T]:
            return (
                gg(data)
                and required <= set(data.keys())
                and set(data.keys()) <= required | optional
                and all(kg(x) for x in data.keys())
                and all(vgs[x](data[x]) for x in data.keys())
            )

    elif origin is tuple:
        gg = _guard(origin, invariant, strict)
        vgs2 = [_guard(x, invariant, strict) for x in get_args(t)]

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and len(data) == len(vgs2) and all(vg(x) for vg, x in zip(vgs2, data))

    elif origin is Literal:
        literals = set(get_args(t))

        def inner(data: Any) -> TypeGuard[T]:
            return data in literals

    elif origin and issubclass(origin, Mapping):
        gg = _guard(origin, invariant, strict)
        invariant = is_mutable_collection(origin)
        kg, vg = (_guard(x, invariant, strict) for x in get_args(t))

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and all(kg(x) for x in data.keys()) and all(vg(x) for x in data.values())

    elif origin and issubclass(origin, Iterable):
        gg = _guard(origin, invariant, strict)
        invariant = is_mutable_collection(origin)
        vt = get_args(t)[0]
        vg = _guard(vt, invariant, strict)

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and all(vg(x) for x in data)

    elif origin is type:
        gg = _guard(origin, invariant, strict)
        vt = get_args(t)[0]

        def inner(data: Any) -> TypeGuard[T]:
            return gg(data) and data is vt

    elif origin is UnionType:
        vgs2 = [_guard(x, invariant, strict) for x in get_args(t)]

        def inner(data: Any) -> TypeGuard[T]:
            return False if (strict and invariant) else any(v(data) for v in vgs2)

    elif supertype:
        gg = _guard(supertype, invariant, strict)

        def inner(data: Any) -> TypeGuard[T]:
            return False if strict else gg(data)

    elif t is Any:

        def inner(data: Any) -> TypeGuard[T]:
            return not (strict and invariant)

    else:

        def inner(data: Any) -> TypeGuard[T]:
            return type(data) is t if (strict and invariant) else isinstance(data, t)

    return inner


@curry
def register_type(t: type[T], fnc: TypeGuardFactory[Any, T]) -> TypeGuardFactory[Any, T]:
    user_types[t] = fnc
    return fnc


@curry
def register_generic(t: type[T], fnc: TypeGuardFactory[Any, T]) -> TypeGuardFactory[Any, T]:
    user_generic[t] = fnc
    return fnc


@curry
def subtype(parent: type[P], fnc: TypeGuardFactory[P, T]) -> TypeGuardFactory[Any, T]:
    def outer(t: type[T], invariant: bool, strict: bool) -> TypeGuardFnc[Any, T]:
        pg = _guard(parent, invariant, strict)
        fg = fnc(t, invariant, strict)

        def inner(data: Any) -> TypeGuard[T]:
            return pg(data) and fg(data)

        return inner

    return outer


def nongeneric(fnc: TypeGuardFnc[P, T]) -> TypeGuardFactory[P, T]:
    def outer(t: type[P], invariant: bool, strict: bool) -> TypeGuardFnc[P, T]:
        @wraps(fnc)
        def inner(data: P) -> TypeGuard[T]:
            return type(data) is t if strict and invariant else fnc(data)

        return inner

    return outer  # type: ignore[return-value]
