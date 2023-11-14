from typing import TypeVar

T = TypeVar('T')


def resolve_type_and_instance(
    type_or_instance: T | None, *,
    base_type: type[T] | None = None,
) -> tuple[type[T], T | None]:
    if base_type is not None and isinstance(type_or_instance, base_type):
        return type(type_or_instance), type_or_instance
    if isinstance(type_or_instance, type):
        if base_type is not None:
            if issubclass(type_or_instance, base_type):
                return type_or_instance, None
        else:
            # noinspection PyTypeChecker
            return type_or_instance, None
    if type_or_instance is None:
        return None, None
    raise TypeError(f"Unexpected {type_or_instance=}")
