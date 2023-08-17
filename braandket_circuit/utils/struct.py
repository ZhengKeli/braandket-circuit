from typing import Callable, Iterable, TypeVar, Union

Atom = TypeVar('Atom')
Struct = Union[Atom, Iterable['Struct']]


def iter_struct(
    struct: Struct, *,
    atom_typ: Union[type, Iterable[type]] = (),
    strict: bool = False,
) -> Iterable[Atom]:
    atom_typ = atom_typ if isinstance(atom_typ, type) else tuple(atom_typ)
    if isinstance(struct, atom_typ):
        yield struct
    else:
        try:
            for item in struct:
                yield from iter_struct(item, atom_typ=atom_typ, strict=strict)
        except TypeError:  # not iterable
            if strict:
                raise TypeError(f"Found item of unexpected type: {struct}")
            yield struct


def freeze_struct(
    struct: Struct, *,
    atom_typ: Union[type, Iterable[type]] = (),
    strict: bool = False,
) -> Union[Atom, tuple]:
    atom_typ = atom_typ if isinstance(atom_typ, type) else tuple(atom_typ)
    if isinstance(struct, atom_typ):
        return struct
    else:
        try:
            return tuple(freeze_struct(item, atom_typ=atom_typ, strict=strict) for item in struct)
        except TypeError:  # not iterable
            if strict:
                raise TypeError(f"Found item of unexpected type: {struct}")
            return struct


def map_struct(
    func: Callable,
    struct: Struct, *,
    atom_typ: Union[type, Iterable[type]] = (),
    strict: bool = False,
) -> Union[Atom, tuple]:
    atom_typ = atom_typ if isinstance(atom_typ, type) else tuple(atom_typ)
    if isinstance(struct, atom_typ):
        return func(struct)
    else:
        try:
            return tuple(map_struct(func, item, atom_typ=atom_typ, strict=strict) for item in struct)
        except TypeError:  # not iterable
            if strict:
                raise TypeError(f"Found item of unexpected type: {struct}")
            return func(struct)
