from ._core import (
    JsonValue,
)
from dataclasses import (
    dataclass,
)
from decimal import (
    Decimal,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveFactory,
    JsonPrimitiveUnfolder,
    Primitive,
)
from fa_purity.result import (
    Result,
)
from fa_purity.result.core import (
    ResultE,
)
from fa_purity.utils import (
    raise_exception,
)
from typing import (
    Dict,
    List,
    Optional,
    TypeVar,
    Union,
)

_T = TypeVar("_T")


class _HandledException(Exception):
    pass


@dataclass(frozen=True)
class JsonValueFactory:
    @staticmethod
    def from_list(
        raw: Union[List[Primitive], FrozenList[Primitive]]
    ) -> JsonValue:
        return JsonValue.from_list(
            tuple(
                JsonValue.from_primitive(JsonPrimitiveFactory.from_raw(item))
                for item in raw
            )
        )

    @staticmethod
    def from_dict(
        raw: Union[Dict[str, Primitive], FrozenDict[str, Primitive]]
    ) -> JsonValue:
        return JsonValue.from_json(
            FrozenDict(
                {
                    key: JsonValue.from_primitive(
                        JsonPrimitiveFactory.from_raw(val)
                    )
                    for key, val in raw.items()
                }
            )
        )

    @classmethod
    def from_any(cls, raw: Optional[_T]) -> ResultE[JsonValue]:
        if isinstance(raw, (FrozenDict, dict)):
            try:
                json_dict = FrozenDict(
                    {
                        JsonPrimitiveFactory.from_any(key)
                        .bind(JsonPrimitiveUnfolder.to_str)
                        .alt(_HandledException)
                        .alt(raise_exception)
                        .unwrap(): cls.from_any(val)
                        .alt(_HandledException)
                        .alt(raise_exception)
                        .unwrap()
                        for key, val in raw.items()
                    }
                )
                return Result.success(JsonValue.from_json(json_dict))
            except _HandledException as err:
                return Result.failure(Exception(err))
        if isinstance(raw, (list, tuple)):
            try:
                json_list = tuple(
                    cls.from_any(item)
                    .alt(_HandledException)
                    .alt(raise_exception)
                    .unwrap()
                    for item in raw
                )
                return Result.success(JsonValue.from_list(json_list))
            except _HandledException as err:
                return Result.failure(Exception(err))
        return JsonPrimitiveFactory.from_any(raw).map(JsonValue.from_primitive)
