from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar, Union

L = TypeVar("L")
R = TypeVar("R")
T = TypeVar("T")


class Either(ABC, Generic[L, R]):

    _value: Union[L, R]
    __match_args__ = "_value"
    __slots__ = "_value"

    def __init__(self, value: Union[L, R]):
        super().__init__()
        self._value = value

    def map(self, f: Callable[[R], T]) -> Either[L, T]:
        return Right(f(self._value)) if self._is_right() else self

    def flat_map(self, f: Callable[[R], Either[L, T]]) -> Either[L, T]:
        return f(self._value) if self._is_right() else self

    def fold(self, fl: Callable[[L], T], fr: Callable[[R], T]) -> T:
        return fr(self._value) if self._is_right() else fl(self._value)

    def swap(self) -> Either[R, L]:
        return Left(self._value) if self._is_right() else Right(self._value)

    @abstractmethod
    def _is_right(self) -> bool:
        pass

    def _is_left(self) -> bool:
        return not self._is_right()

    def __str__(self) -> str:
        return f"Either is {'Right' if self._is_right() else 'Left'}, with value: {self._value.__repr__()} of type {type(self._value)}"

    def __repr__(self) -> str:
        return f"algae.Either({self._value.__repr__()})"

    def __eq__(self, other: Either[L, R]) -> bool:
        if self._is_left():
            return other._is_left() and self._value == other._value
        elif other._is_left():
            return False
        else:
            return self._value == other._value

    def __ne__(self, other: Either[L, R]) -> bool:
        return not self == other


class Right(Either):
    def _is_right(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"algae.Right({self._value})"


class Left(Either):
    def _is_right(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"algae.Left({self._value})"
