import sys
import weakref

if sys.version_info < (3, 5):
    raise ValueError("This module requires at least Python 3.5")
elif sys.version_info < (3, 11):
    from typing import Any, final, TypeVar

    Self = TypeVar("Self")
else:
    from typing import Self, Any, final


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

    def __str__(self: Self) -> str:
        return "AttrdictNone"

    def __repr__(self: Self) -> str:
        return "AttrdictNone"


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

    def __matmul__(self: Self, target: dict) -> Self:
        for key in self.__path:
            if isinstance(target, dict):
                target = target.get(key, AttrdictNone)
            else:
                return AttrdictNone
        return target

    def __call__(self, target: dict) -> Any:
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
