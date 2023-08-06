from __future__ import annotations

from typing import Any, Generic, Iterable, Mapping, Type, TypeVar, Union, cast

from marshmallow import Schema, post_load
from typing_extensions import is_typeddict

LoadType = TypeVar('LoadType')


class TypedSchema(Schema, Generic[LoadType]):
    __post_load_type__: Type[LoadType]
    def typed_load(self, data: Mapping[str, Any] | Iterable[Mapping[str, Any]], *, many: bool | None = None,
    ) -> LoadType | list[LoadType] | None:
        return cast(Union[LoadType, list[LoadType], None], super().load(data, many=many))

    def typed_loads(self, json_data: str, *, many: bool | None = None, **kwargs: Any) -> LoadType | list[LoadType] | None:
        return cast(LoadType, super().loads(json_data, many=many, **kwargs))

    def typed_load_one(self, data: Mapping[str, Any]) -> LoadType | None:
        return cast(LoadType, super().load(data, many=False))

    def typed_loads_one(self, json_data: str, **kwargs: Any) -> LoadType | None:
        return cast(LoadType, super().loads(json_data, many=False, **kwargs))

    def typed_load_many(self, data: Iterable[Mapping[str, Any]]) -> list[LoadType]:
        return cast(list[LoadType], super().load(data, many=True))

    def typed_loads_many(self, json_data: str, **kwargs: Any) -> list[LoadType]:
        return cast(list[LoadType], super().loads(json_data, many=True, **kwargs))

    @post_load
    def make_object(
        self, data: Mapping[str, Any] | Iterable[Mapping[str, Any]],
        **kwargs: Any,
    ) -> Mapping[str, Any] | Iterable[Mapping[str, Any]] | LoadType:
        if data is None or is_typeddict(self.__post_load_type__):
            return data
        return self.__post_load_type__(**data)
