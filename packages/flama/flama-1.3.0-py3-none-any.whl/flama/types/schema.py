import inspect
import sys
import typing as t

if sys.version_info < (3, 10):  # PORT: Remove when stop supporting 3.9 # pragma: no cover
    from typing_extensions import TypeGuard

    t.TypeGuard = TypeGuard

__all__ = ["JSONField", "JSONSchema", "Schema", "is_schema", "is_schema"]

_T_Field = t.TypeVar("_T_Field")
_T_Schema = t.TypeVar("_T_Schema")


def is_schema(obj: t.Any) -> t.TypeGuard[t.Type["Schema"]]:
    return inspect.isclass(obj) and issubclass(obj, Schema)


class _SchemaMeta(type):
    def __eq__(self, other) -> bool:
        return is_schema(other) and self.schema == other.schema  # type: ignore[attr-defined]

    def __hash__(self) -> int:
        return id(self)


class Schema(dict, metaclass=_SchemaMeta):  # type: ignore[misc]
    schema: t.ClassVar[t.Any] = None

    def __class_getitem__(cls, schema_cls: _T_Schema) -> "Schema":  # type: ignore[override]
        return _SchemaMeta("_SchemaAlias", (Schema,), {"schema": schema_cls})  # type: ignore[return-value]


JSONField = t.Union[str, int, float, bool, None, t.List["JSONField"], t.Dict[str, "JSONField"]]
JSONSchema = t.Dict[str, JSONField]
