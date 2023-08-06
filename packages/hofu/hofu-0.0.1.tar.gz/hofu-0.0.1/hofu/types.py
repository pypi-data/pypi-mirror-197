from abc import ABCMeta, abstractmethod
from typing import TypeVar, runtime_checkable, Protocol, Reversible, Generator

T = TypeVar('T')
R = TypeVar('R')


@runtime_checkable
class Iterable(Protocol[T], Reversible[T], metaclass=ABCMeta):
    @abstractmethod
    def __iter__(self) -> Generator[T, None, None]:
        ...

    @abstractmethod
    def __next__(self) -> T:
        ...
