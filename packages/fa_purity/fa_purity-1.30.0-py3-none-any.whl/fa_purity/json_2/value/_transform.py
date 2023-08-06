from ._core import (
    JsonObj,
    JsonValue,
)
from dataclasses import (
    dataclass,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity.json_2.primitive import (
    JsonPrimitive,
    JsonPrimitiveUnfolder,
    Primitive,
)
from fa_purity.result import (
    Result,
)
from fa_purity.result.core import (
    ResultE,
)
from fa_purity.result.factory import (
    try_get,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_purity.union import (
    UnionFactory,
)
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    TypeVar,
    Union,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class Unfolder:
    @staticmethod
    def to_primitive(item: JsonValue) -> ResultE[JsonPrimitive]:
        fail: ResultE[JsonPrimitive] = Result.failure(
            Exception(
                TypeError("Expected `JsonPrimitive` in unfolded `JsonValue`")
            )
        )
        return item.map(
            lambda x: Result.success(x),
            lambda _: fail,
            lambda _: fail,
        )

    @staticmethod
    def to_list(item: JsonValue) -> ResultE[FrozenList[JsonValue]]:
        fail: ResultE[FrozenList[JsonValue]] = Result.failure(
            Exception(
                TypeError(
                    "Expected `FrozenList[JsonValue]` in unfolded `JsonValue`"
                )
            )
        )
        return item.map(
            lambda _: fail,
            lambda x: Result.success(x),
            lambda _: fail,
        )

    @staticmethod
    def to_json(item: JsonValue) -> ResultE[JsonObj]:
        fail: ResultE[JsonObj] = Result.failure(
            Exception(TypeError("Expected `JsonObj` in unfolded `JsonValue`"))
        )
        return item.map(
            lambda _: fail,
            lambda _: fail,
            lambda x: Result.success(x),
        )

    @staticmethod
    def transform_list(
        items: FrozenList[JsonValue],
        transform: Callable[[JsonValue], ResultE[_T]],
    ) -> ResultE[FrozenList[_T]]:
        return all_ok(tuple(transform(i) for i in items))

    @staticmethod
    def transform_json(
        item: JsonObj, transform: Callable[[JsonValue], ResultE[_T]]
    ) -> ResultE[FrozenDict[str, _T]]:
        key_vals = tuple(
            transform(val).map(lambda p: (key, p)) for key, val in item.items()
        )
        return all_ok(key_vals).map(lambda x: FrozenDict(dict(x)))

    @classmethod
    def get(cls, item: JsonValue, key: str) -> ResultE[JsonValue]:
        return cls.to_json(item).alt(Exception).bind(lambda d: try_get(d, key))

    @classmethod
    def to_list_of(
        cls, item: JsonValue, transform: Callable[[JsonValue], ResultE[_T]]
    ) -> ResultE[FrozenList[_T]]:
        return cls.to_list(item).bind(
            lambda i: cls.transform_list(i, transform)
        )

    @classmethod
    def to_dict_of(
        cls, item: JsonValue, transform: Callable[[JsonValue], ResultE[_T]]
    ) -> ResultE[FrozenDict[str, _T]]:
        return cls.to_json(item).bind(
            lambda i: cls.transform_json(i, transform)
        )

    @classmethod
    def to_optional(
        cls, item: JsonValue, transform: Callable[[JsonValue], ResultE[_T]]
    ) -> ResultE[Optional[_T]]:
        _union: UnionFactory[_T, None] = UnionFactory()
        return (
            cls.to_primitive(item)
            .bind(JsonPrimitiveUnfolder.to_none)
            .map(_union.inr)
            .lash(lambda _: transform(item).map(_union.inl))
        )

    @classmethod
    def to_raw(cls, value: JsonValue) -> Union[Dict[str, Any], List[Any], Primitive]:  # type: ignore[misc]
        def _cast(item: Primitive) -> Primitive:
            # cast used for helping mypy to infer the correct return type
            return item

        return value.map(
            lambda p: p.map(
                lambda x: _cast(x),
                lambda x: _cast(x),
                lambda x: _cast(x),
                lambda x: _cast(x),
                lambda x: _cast(x),
                lambda: _cast(None),
            ),
            lambda items: [cls.to_raw(i) for i in items],  # type: ignore[misc]
            lambda dict_obj: {key: cls.to_raw(val) for key, val in dict_obj.items()},  # type: ignore[misc]
        )
