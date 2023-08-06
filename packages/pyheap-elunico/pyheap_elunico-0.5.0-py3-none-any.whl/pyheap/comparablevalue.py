from typing import Self


class ComparableValue:
    """
    Classes that are to be considered ComparableValues must conform to the following:
        1. Have a total ordering by implementing the methods below
        2. Have a strong sense of value equality and inequality which is exactly logically opposite of equality
        3. Function as a "value" type meaning that if 2 instances compare == equal, they are completely interchangeable
           for one another in *all* instances.

    A class that satisfies these rules does not need to be a part of this class's hierarchy, however, classes
    can choose to inherit this class. This class only requires subclasses to implement __eq__ and __lt__ and they
    can get the rest of the methods for free, or they choose to implement them as well. A class could also
    implement these methods without inheriting or use @functools.total_ordering

    Examples of built-in types that act this way include: int, float, str, and bool. Two int's or str's—being
    immutable—are functionally identical if they are equal in value, for example
    """

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError("Class must implement __eq__")

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __lt__(self, other: Self) -> bool:
        raise NotImplementedError("Class must implement __lt__")

    def __gt__(self, other: Self) -> bool:
        return not (self < other) and not (self == other)

    def __le__(self, other: Self) -> bool:
        return (self < other) or (self == other)

    def __ge__(self, other: Self) -> bool:
        return (self > other) or (self == other)
