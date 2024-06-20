import sys

if (3, 5) < sys.version_info < (3, 11):
    from typing import Any, final, TypeVar

    Self = TypeVar("Self")
else:
    from typing import Self, Any, final


class Attrdict:
    """
    A class that allows you to access dictionary values as attributes.
    """

    __slot__: tuple = ()
    __content: dict[str, Any]

    def __init__(self: Self, *args: list[Any], **kargs: dict[str, Any]) -> None:
        self.__content = dict(*args, **kargs)

        for key, value in self.__content.items():
            if key.startswith("__"):
                raise AttributeError(f"Key {key} cannot start with '__'")
            if isinstance(value, dict):
                self.__content[key] = Attrdict(value)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                for i, v in enumerate(value):
                    if isinstance(v, dict):
                        value[i] = Attrdict(v)

    def __getattr__(self: Self, key: str) -> Any:
        return self.__content.get(key, AttrdictNone)

    def __getitem__(self: Self, key: str) -> Any:
        return self.__content.get(key, AttrdictNone)

    def __str__(self: Self) -> str:
        return self.__content.__str__()

    def __repr__(self: Self) -> str:
        return self.__content.__repr__()


@final
class AttrdictNoneType:
    """
    A class that represents that a key does not exist in the dictionary.
    """

    __slot__: tuple = ()
    __instance = None

    def __new__(cls: Self) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __getattribute__(self: Self, key: str) -> Any:
        return self

    def __getitem__(self: Self, key: str) -> Any:
        return self

    def __call__(self: Self, *args: list[Any], **kwds: dict[str, Any]) -> Any:
        return self

    def __str__(self: Self) -> str:
        return "AttrdictNone"

    def __repr__(self: Self) -> str:
        return "AttrdictNone"

    def __bool__(self: Self) -> False:
        return False

    def __setattr__(self, name: str, value: Any) -> None:
        raise SyntaxError("Cannot set attribute on AttrdictNone")


class AttrdictSubSymbol:
    __slot__: tuple = ()
    __path: list

    def __init__(self: Self, name: str, parent: Self = None) -> None:
        if name.startswith("__"):
            raise AttributeError(f"Key {name} cannot start with '__'")

        if parent is None:
            self.__path = [name]
        else:
            self.__path = parent.__path
            self.__path.append(name)

    def __getattr__(self: Self, name: str) -> Self:
        return AttrdictSubSymbol(name, self)

    def __matmul__(self: Self, target: Attrdict) -> Self:
        end = len(self.__path) - 1
        for i, key in enumerate(self.__path):
            target = target[key]

            if target is AttrdictNone:
                return AttrdictNone
            if not isinstance(target, Attrdict) and i != end:
                return AttrdictNone
        return target

    def __call__(self, target: Attrdict) -> Any:
        return self @ target


@final
class AttrdictSymbolType:
    __slot__: tuple = ()
    __instance: Self = None

    def __new__(cls: Self) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __getattr__(cls: Self, name: str) -> AttrdictSubSymbol:
        return AttrdictSubSymbol(name)


AttrdictSymbol = AttrdictSymbolType()
AttrdictNone = AttrdictNoneType()
