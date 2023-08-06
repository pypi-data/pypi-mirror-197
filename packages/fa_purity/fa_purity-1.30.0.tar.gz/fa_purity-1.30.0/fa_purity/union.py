from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from deprecated import (
    deprecated,
)
from typing import (
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
)

_A = TypeVar("_A")
_B = TypeVar("_B")
_C = TypeVar("_C")
_L = TypeVar("_L")
_R = TypeVar("_R")
_T = TypeVar("_T")


@deprecated("NEW API: use `UnionFactory` instead")  # type: ignore[misc]
def inr(val: _R, _left: Optional[Type[_L]] = None) -> Union[_L, _R]:
    return val


@deprecated("NEW API: use `UnionFactory` instead")  # type: ignore[misc]
def inl(val: _L, _right: Optional[Type[_R]] = None) -> Union[_L, _R]:
    return val


@dataclass(frozen=True)
class UnionFactory(Generic[_L, _R]):
    def inl(self, value: _L) -> Union[_L, _R]:
        return value

    def inr(self, value: _R) -> Union[_L, _R]:
        return value


@dataclass(frozen=True)
class _Empty:
    pass


@dataclass(frozen=True)
class _Coproduct(Generic[_L, _R]):
    left: Union[_L, _Empty]
    right: Union[_R, _Empty]
    left_val: bool

    @staticmethod
    def assert_non_empty(item: Union[_A, _Empty]) -> _A:
        if isinstance(item, _Empty):
            raise Exception(
                "This should be not possible. Raise an issue to the fa_purity project."
            )
        return item


@dataclass(frozen=True)
class Coproduct(Generic[_L, _R]):
    _inner: _Coproduct[_L, _R]

    @staticmethod
    def inl(value: _L) -> Coproduct[_L, _R]:
        return Coproduct(_Coproduct(value, _Empty(), True))

    @staticmethod
    def inr(value: _R) -> Coproduct[_L, _R]:
        return Coproduct(_Coproduct(_Empty(), value, False))

    def map(
        self, transform_1: Callable[[_L], _T], transform_2: Callable[[_R], _T]
    ) -> _T:
        if self._inner.left_val:
            return transform_1(_Coproduct.assert_non_empty(self._inner.left))
        return transform_2(_Coproduct.assert_non_empty(self._inner.right))


@dataclass(frozen=True)
class CoproductFactory(Generic[_L, _R]):
    def inl(self, value: _L) -> Coproduct[_L, _R]:
        return Coproduct.inl(value)

    def inr(self, value: _R) -> Coproduct[_L, _R]:
        return Coproduct.inr(value)


@dataclass(frozen=True)
class CoproductTransform(Generic[_L, _R]):
    _value: Coproduct[_L, _R]

    def swap(self) -> Coproduct[_R, _L]:
        def _right(item: _R) -> Coproduct[_R, _L]:
            return Coproduct.inl(item)

        def _left(item: _L) -> Coproduct[_R, _L]:
            return Coproduct.inr(item)

        return self._value.map(_left, _right)

    def to_union(self) -> Union[_L, _R]:
        factory: UnionFactory[_L, _R] = UnionFactory()
        return self._value.map(
            lambda l: factory.inl(l),
            lambda r: factory.inr(r),
        )

    @staticmethod
    def permutate(
        item: Coproduct[_A, Coproduct[_B, _C]]
    ) -> Coproduct[Coproduct[_A, _B], _C]:
        factory: CoproductFactory[Coproduct[_A, _B], _C] = CoproductFactory()
        return item.map(
            lambda a: factory.inl(Coproduct.inl(a)),
            lambda bc: bc.map(
                lambda b: factory.inl(Coproduct.inr(b)),
                lambda c: Coproduct.inr(c),
            ),
        )
