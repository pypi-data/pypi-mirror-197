from typing import Protocol, TypeGuard, TypeVar

Tin = TypeVar("Tin", contravariant=True)
Tout = TypeVar("Tout", covariant=True)
Tout2 = TypeVar("Tout2")


class TypeGuardFnc(Protocol[Tin, Tout]):
    def __call__(self, data: Tin) -> TypeGuard[Tout]:
        ...


class TypeGuardFactory(Protocol[Tin, Tout2]):
    def __call__(self, t: type[Tout2], invariant: bool, strict: bool) -> TypeGuardFnc[Tin, Tout2]:
        ...
