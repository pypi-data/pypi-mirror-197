from __future__ import annotations

from typing import NoReturn, Generic, Callable, Generator

from .types import Iterable, T, R


class Iterator(Generic[T]):
    def __init__(self, iterable: Iterable[T]):
        self.iterable = iterable
        self.__instructions = []

    def __iter__(self) -> Generator[T, None, None]:
        return self.collect()

    def __next__(self) -> NoReturn:
        raise TypeError(
            f"`{self.__class__.__name__}` must be collected first, add a `.{self.collect.__name__}()` call to it."
        )

    def __getitem__(self, item: int) -> T:
        raise TypeError("Iterators cannot be indexed, use `list()` to convert it to a list.")

    def collect(self) -> Generator[T, None, None]:
        """
        Collects the iterable and executes all instructions.
        """
        for item in self.iterable:
            for instruction in self.__instructions:
                item = instruction(item)

                if item is None:
                    break

            if item is not None:
                yield item

    def map(self, func: Callable[[T], R]) -> Iterator[R]:
        """
        Maps the iterable to a new iterable by the given function.

        # Example

        We want to format a list of numbers to a list of strings, and suffix them with " is even" if they are even.

        ```py
        >>> even_formatted = Iterator(range(10)).map(lambda x: f"{x}={'even' if x % 2 == 0 else 'odd'}").collect()
        >>> print("Even/odd:", list(even_formatted))
        Even/odd: ['0=even', '1=odd', '2=even', '3=odd', '4=even', '5=odd', '6=even', '7=odd', '8=even', '9=odd']
        ```

        :param func:
        :return:
        """
        self.__instructions.append(func)
        return self

    def filter(self, func: Callable[[T], bool]) -> Iterator[T]:
        """
        Filters the iterable by the given function.

        # Example

        We want to filter out all even numbers from a list.

        ```py
        >>> data = Iterator(range(10)).filter(lambda x: x % 2 == 0).collect()
        >>> print("Even numbers:", list(data))
        Even numbers: [0, 2, 4, 6, 8]
        ```

        :param func: The function to filter the iterable with.
        :return: A filtered iterator.
        """

        def wrapper(item: T) -> T:
            if func(item):
                return item

        self.__instructions.append(wrapper)
        return self

    def skip(self, count: int) -> Iterator[T]:
        """
        Ignores the first `count` items in the iterable.

        :param count: The amount of items to skip.
        :return: An iterator with the first `count` items skipped.
        """

        def wrapper(item: T) -> T:
            nonlocal count

            if count > 0:
                count -= 1
                return

            return item

        self.__instructions.append(wrapper)
        return self

    def take(self, count: int) -> Iterator[T]:
        """
        Stops the iterator after the given amount of items.

        :param count: The amount of items to take.
        :return: An iterator with the first `count` items.
        """

        def wrapper(item: T) -> T:
            nonlocal count

            if count > 0:
                count -= 1
                return item

        self.__instructions.append(wrapper)
        return self

    def for_each(self, func: Callable[[T], None]) -> NoReturn:
        """
        Executes the given function for each item in the iterable.

        :param func: The function to execute for each item.
        """

        def wrapper(item: T) -> NoReturn:
            func(item)

        self.__instructions.append(wrapper)

        # Go through the iterator to execute the instructions
        for _ in self.collect():
            pass

    def reduce(self, func: Callable[[R, T], R], accumulator: R = None) -> R:
        """
        Reduces the iterable to a single value.

        # Example

        We want to calculate the average age of all people in a list.

        ```py
        >>> people = [
        >>>     {"name": "John", "age": 30},
        >>>     {"name": "Jane", "age": 25},
        >>>     {"name": "Bob", "age": 40},
        >>>     {"name": "Alice", "age": 35},
        >>> ]
        >>>
        >>> average_age = Iterator(people).reduce(lambda x, y: x + y["age"], 0) / len(people)
        >>> print("Average age:", average_age)
        Average age: 32.5
        ```

        :param func: The function to reduce the iterable with.
        :param accumulator: Base value for the accumulator, if not provided, the first item in the iterable will be used.
        :return: A single value, which was the accumulated result of the function.
        """

        def wrapper(item: T) -> T:
            nonlocal accumulator

            if accumulator is None:
                accumulator = item
                return

            accumulator = func(accumulator, item)
            return accumulator

        self.for_each(wrapper)
        return accumulator

    def rev(self) -> Iterator[T]:
        """
        Reverses the iterable.

        :return:
        """
        self.iterable = reversed(self.iterable)
        return self

