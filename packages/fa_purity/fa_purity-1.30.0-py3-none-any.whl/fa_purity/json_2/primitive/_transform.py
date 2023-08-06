from ._core import (
    JsonPrimitive,
)
from dataclasses import (
    dataclass,
)
from decimal import (
    Decimal,
)
from fa_purity.result import (
    ResultE,
)
from fa_purity.result.core import (
    Result,
)
from fa_purity.union import (
    UnionFactory,
)
from typing import (
    Optional,
)


@dataclass(frozen=True)
class JsonPrimitiveUnfolder:
    @staticmethod
    def to_str(item: JsonPrimitive) -> ResultE[str]:
        fail: ResultE[str] = Result.failure(
            TypeError("Unfolded JsonPrimitive is not `str`"), str
        ).alt(Exception)
        return item.map(
            lambda x: Result.success(x),
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda: fail,
        )

    @staticmethod
    def to_int(item: JsonPrimitive) -> ResultE[int]:
        fail: ResultE[int] = Result.failure(
            TypeError("Unfolded JsonPrimitive is not `int`"), int
        ).alt(Exception)
        return item.map(
            lambda _: fail,
            lambda x: Result.success(x),
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda: fail,
        )

    @staticmethod
    def to_float(item: JsonPrimitive) -> ResultE[float]:
        fail: ResultE[float] = Result.failure(
            TypeError("Unfolded JsonPrimitive is not `float`"), float
        ).alt(Exception)
        return item.map(
            lambda _: fail,
            lambda _: fail,
            lambda x: Result.success(x),
            lambda _: fail,
            lambda _: fail,
            lambda: fail,
        )

    @staticmethod
    def to_decimal(item: JsonPrimitive) -> ResultE[Decimal]:
        fail: ResultE[Decimal] = Result.failure(
            TypeError("Unfolded JsonPrimitive is not `Decimal`"), Decimal
        ).alt(Exception)
        return item.map(
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda x: Result.success(x),
            lambda _: fail,
            lambda: fail,
        )

    @staticmethod
    def to_bool(item: JsonPrimitive) -> ResultE[bool]:
        fail: ResultE[bool] = Result.failure(
            TypeError("Unfolded JsonPrimitive is not `bool`"), bool
        ).alt(Exception)
        return item.map(
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda x: Result.success(x),
            lambda: fail,
        )

    @staticmethod
    def to_none(item: JsonPrimitive) -> ResultE[None]:
        fail: ResultE[None] = Result.failure(
            TypeError("Unfolded JsonPrimitive is not `None`"), type(None)
        ).alt(Exception)
        return item.map(
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda _: fail,
            lambda: Result.success(None),
        )

    @classmethod
    def to_opt_str(cls, item: JsonPrimitive) -> ResultE[Optional[str]]:
        factory: UnionFactory[str, None] = UnionFactory()
        return (
            cls.to_str(item)
            .map(factory.inl)
            .lash(lambda _: cls.to_none(item).map(factory.inr))
        )

    @classmethod
    def to_opt_int(cls, item: JsonPrimitive) -> ResultE[Optional[int]]:
        factory: UnionFactory[int, None] = UnionFactory()
        return (
            cls.to_int(item)
            .map(factory.inl)
            .lash(lambda _: cls.to_none(item).map(factory.inr))
        )

    @classmethod
    def to_opt_float(cls, item: JsonPrimitive) -> ResultE[Optional[float]]:
        factory: UnionFactory[float, None] = UnionFactory()
        return (
            cls.to_float(item)
            .map(factory.inl)
            .lash(lambda _: cls.to_none(item).map(factory.inr))
        )

    @classmethod
    def to_opt_decimal(cls, item: JsonPrimitive) -> ResultE[Optional[Decimal]]:
        factory: UnionFactory[Decimal, None] = UnionFactory()
        return (
            cls.to_decimal(item)
            .map(factory.inl)
            .lash(lambda _: cls.to_none(item).map(factory.inr))
        )

    @classmethod
    def to_opt_bool(cls, item: JsonPrimitive) -> ResultE[Optional[bool]]:
        factory: UnionFactory[bool, None] = UnionFactory()
        return (
            cls.to_bool(item)
            .map(factory.inl)
            .lash(lambda _: cls.to_none(item).map(factory.inr))
        )
