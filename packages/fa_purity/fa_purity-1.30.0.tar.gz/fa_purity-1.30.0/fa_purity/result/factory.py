from .core import (
    Result,
    ResultE,
)
from dataclasses import (
    dataclass,
)
from fa_purity.frozen import (
    FrozenDict,
)
from typing import (
    Generic,
    TypeVar,
)

_K = TypeVar("_K")
_V = TypeVar("_V")
_S = TypeVar("_S")
_F = TypeVar("_F")


@dataclass(frozen=True)
class ResultFactory(Generic[_S, _F]):
    def success(self, value: _S) -> Result[_S, _F]:
        return Result.success(value)

    def failure(self, value: _F) -> Result[_S, _F]:
        return Result.failure(value)


def try_get(data: FrozenDict[_K, _V], key: _K) -> ResultE[_V]:
    factory: ResultFactory[_V, Exception] = ResultFactory()
    if key in data:
        return factory.success(data[key])
    return factory.failure(KeyError(key)).alt(Exception)
